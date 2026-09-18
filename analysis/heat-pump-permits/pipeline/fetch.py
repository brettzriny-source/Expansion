"""Fetchers for the three open-data API styles used by US permitting portals.

* Socrata (SODA 2.x)      e.g. data.mesaaz.gov, information.stpaul.gov, data.nj.gov
* ArcGIS FeatureServer    e.g. opendata.minneapolismn.gov, Mecklenburg County GIS
* Static CSV / CKAN       e.g. phoenixopendata.com

Every fetcher returns a pandas DataFrame with the portal's native columns.
Column mapping to the pipeline's canonical schema happens in ``run.py`` using
``sources.yaml``. All fetchers paginate and are resumable via ``cache_dir``.

Network access in the Claude Code session that wrote this was blocked for
all government hosts, so these fetchers are written against the documented
APIs but have not been run against the live endpoints. Expect to adjust
``where`` clauses and field names on first run; the ``--probe`` flag in
``run.py`` prints the schema of each endpoint for that purpose.
"""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Iterable, Optional

import pandas as pd
import requests

USER_AGENT = "jetson-expansion-heat-pump-permits/0.1 (+https://jetsonhome.com)"
DEFAULT_TIMEOUT = 60
PAGE_SLEEP_SECONDS = 0.25

# When True, fetchers serve only from cache and raise FetchError instead of
# touching the network. Set by run.py --offline.
OFFLINE = False


class FetchError(RuntimeError):
    pass


def _session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": USER_AGENT, "Accept": "application/json"})
    return s


def _cache_path(cache_dir: Optional[Path], key: str) -> Optional[Path]:
    if cache_dir is None:
        return None
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir / (hashlib.sha1(key.encode()).hexdigest()[:16] + ".parquet")


def _get(session: requests.Session, url: str, params: dict, retries: int = 4) -> requests.Response:
    if OFFLINE:
        raise FetchError(f"offline mode and not cached: {url}")
    delay = 2.0
    for attempt in range(retries):
        try:
            r = session.get(url, params=params, timeout=DEFAULT_TIMEOUT)
            if r.status_code == 429 or r.status_code >= 500:
                raise FetchError(f"{r.status_code} from {url}")
            r.raise_for_status()
            return r
        except (requests.RequestException, FetchError) as exc:
            if attempt == retries - 1:
                raise FetchError(f"giving up on {url}: {exc}") from exc
            time.sleep(delay)
            delay *= 2
    raise FetchError("unreachable")


# ---------------------------------------------------------------------------
# Socrata
# ---------------------------------------------------------------------------

def fetch_socrata(
    domain: str,
    dataset_id: str,
    where: Optional[str] = None,
    select: Optional[Iterable[str]] = None,
    app_token: Optional[str] = None,
    page_size: int = 50_000,
    cache_dir: Optional[Path] = None,
) -> pd.DataFrame:
    """Pull a Socrata dataset with SoQL paging. ``where`` is a SoQL predicate."""
    key = f"socrata|{domain}|{dataset_id}|{where}|{','.join(select or [])}"
    cached = _cache_path(cache_dir, key)
    if cached and cached.exists():
        return pd.read_parquet(cached)

    url = f"https://{domain}/resource/{dataset_id}.json"
    session = _session()
    if app_token:
        session.headers["X-App-Token"] = app_token

    frames = []
    offset = 0
    while True:
        params = {"$limit": page_size, "$offset": offset, "$order": ":id"}
        if where:
            params["$where"] = where
        if select:
            params["$select"] = ",".join(select)
        rows = _get(session, url, params).json()
        if not rows:
            break
        frames.append(pd.DataFrame(rows))
        if len(rows) < page_size:
            break
        offset += page_size
        time.sleep(PAGE_SLEEP_SECONDS)

    df = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    if cached:
        df.to_parquet(cached)
    return df


def probe_socrata(domain: str, dataset_id: str) -> dict:
    """Return column metadata for a Socrata dataset (names, types, descriptions)."""
    url = f"https://{domain}/api/views/{dataset_id}.json"
    meta = _get(_session(), url, {}).json()
    return {
        "name": meta.get("name"),
        "rows": meta.get("rowsUpdatedAt"),
        "columns": [
            {"field": c.get("fieldName"), "type": c.get("dataTypeName"), "desc": c.get("description")}
            for c in meta.get("columns", [])
        ],
    }


# ---------------------------------------------------------------------------
# ArcGIS FeatureServer / MapServer
# ---------------------------------------------------------------------------

def fetch_arcgis(
    layer_url: str,
    where: str = "1=1",
    out_fields: str = "*",
    page_size: int = 2000,
    cache_dir: Optional[Path] = None,
) -> pd.DataFrame:
    """Pull all features from an ArcGIS REST layer (…/FeatureServer/0)."""
    key = f"arcgis|{layer_url}|{where}|{out_fields}"
    cached = _cache_path(cache_dir, key)
    if cached and cached.exists():
        return pd.read_parquet(cached)

    session = _session()
    query_url = layer_url.rstrip("/") + "/query"

    # Respect the server's advertised max record count.
    try:
        info = _get(session, layer_url.rstrip("/"), {"f": "json"}).json()
        page_size = min(page_size, int(info.get("maxRecordCount", page_size)))
    except Exception:  # noqa: BLE001 - metadata is optional
        pass

    frames = []
    offset = 0
    while True:
        params = {
            "where": where,
            "outFields": out_fields,
            "returnGeometry": "false",
            "resultOffset": offset,
            "resultRecordCount": page_size,
            "orderByFields": "OBJECTID",
            "f": "json",
        }
        payload = _get(session, query_url, params).json()
        if "error" in payload:
            raise FetchError(f"ArcGIS error from {layer_url}: {payload['error']}")
        feats = payload.get("features", [])
        if not feats:
            break
        frames.append(pd.DataFrame([f["attributes"] for f in feats]))
        if not payload.get("exceededTransferLimit", False) and len(feats) < page_size:
            break
        offset += len(feats)
        time.sleep(PAGE_SLEEP_SECONDS)

    df = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

    # ArcGIS dates are epoch milliseconds.
    for col in df.columns:
        if col.lower().endswith(("date", "_dt", "issued", "applied", "finaled")) and pd.api.types.is_numeric_dtype(df[col]):
            df[col] = pd.to_datetime(df[col], unit="ms", errors="coerce")

    if cached:
        df.to_parquet(cached)
    return df


def probe_arcgis(layer_url: str) -> dict:
    info = _get(_session(), layer_url.rstrip("/"), {"f": "json"}).json()
    return {
        "name": info.get("name"),
        "maxRecordCount": info.get("maxRecordCount"),
        "fields": [{"field": f["name"], "type": f["type"], "alias": f.get("alias")} for f in info.get("fields", [])],
    }


# ---------------------------------------------------------------------------
# Static CSV (CKAN resources, direct downloads)
# ---------------------------------------------------------------------------

def fetch_csv(url: str, cache_dir: Optional[Path] = None, **read_csv_kwargs) -> pd.DataFrame:
    key = f"csv|{url}"
    cached = _cache_path(cache_dir, key)
    if cached and cached.exists():
        return pd.read_parquet(cached)
    r = _get(_session(), url, {})
    from io import StringIO

    df = pd.read_csv(StringIO(r.text), low_memory=False, **read_csv_kwargs)
    if cached:
        df.to_parquet(cached)
    return df


def probe_ckan(portal: str, dataset: str) -> dict:
    """List resources (files) on a CKAN dataset, e.g. phoenixopendata.com."""
    url = f"https://{portal}/api/3/action/package_show"
    payload = _get(_session(), url, {"id": dataset}).json()
    res = payload.get("result", {})
    return {
        "title": res.get("title"),
        "resources": [
            {"name": r.get("name"), "format": r.get("format"), "url": r.get("url"), "modified": r.get("last_modified")}
            for r in res.get("resources", [])
        ],
    }


def dump_probe(result: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, default=str))
