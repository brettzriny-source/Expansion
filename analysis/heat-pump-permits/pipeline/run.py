"""Heat pump permits per capita: fetch, classify, aggregate.

Usage (from analysis/heat-pump-permits/):

    python -m pipeline.run --probe                 # print each endpoint's schema
    python -m pipeline.run                         # full run, all markets
    python -m pipeline.run --market charlotte      # one market
    python -m pipeline.run --offline               # skip network; use cache + fallbacks

Outputs land in ./output/:
    permits_classified.csv    one row per HVAC-ish permit with classification
    market_summary.csv        per-jurisdiction and per-market rates
    market_summary.md         the same, formatted for the report

Design choices that affect the numbers, so they are stated here:

* Window: trailing 12 and 36 months from the run date, on the permit's
  issue date (not application date). Both are reported.
* Denominators: population, total housing units, and single-family units.
  Single-family units is the recommended one for cross-market comparison
  because Newark's 2-4 family stock and Phoenix's SFR stock differ so much.
* Ambiguous HVAC permits (equipment not stated) are counted and reported as
  their own line. The honest "heat pump" rate is a range: confirmed only, to
  confirmed + ambiguous. Both bounds are in the summary.
* A jurisdiction is only in a market total if its fetch succeeded. Coverage
  share (covered population / market population) is printed next to every
  market number.
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import sys
from pathlib import Path

import pandas as pd
import yaml

from . import fetch
from .classify import classify_frame
from .population import Denominator, fallback_denominator, fetch_denominator

ROOT = Path(__file__).resolve().parents[1]
CACHE = Path(os.environ.get("HP_CACHE", ROOT / "cache"))
OUTPUT = Path(os.environ.get("HP_OUTPUT", ROOT / "output"))
SOURCES = Path(os.environ.get("HP_SOURCES", ROOT / "pipeline" / "sources.yaml"))

CANONICAL = ["permit_id", "issued", "permit_type", "work_type", "description", "address", "zip", "valuation"]


def load_sources() -> dict:
    return yaml.safe_load(SOURCES.read_text())


# ---------------------------------------------------------------------------
# Fetch + normalise one jurisdiction
# ---------------------------------------------------------------------------

def fetch_jurisdiction(j: dict, offline: bool) -> pd.DataFrame:
    src = j["source"]
    kind = src["kind"]
    fetch.OFFLINE = offline
    cache_dir = CACHE
    if kind == "arcgis":
        df = fetch.fetch_arcgis(src["layer_url"], where=src.get("where", "1=1"), cache_dir=cache_dir)
    elif kind == "socrata":
        df = fetch.fetch_socrata(src["domain"], src["dataset_id"], where=src.get("where"), cache_dir=cache_dir)
    elif kind == "csv":
        df = fetch.fetch_csv(src["url"], cache_dir=cache_dir)
    elif kind == "csv_file":
        df = pd.read_csv(ROOT / src["path"], low_memory=False)
    elif kind == "manual":
        raise fetch.FetchError(f"{j['name']}: no machine-readable source; see notes")
    else:
        raise ValueError(f"unknown source kind {kind}")
    return normalise(df, j)


def normalise(df: pd.DataFrame, j: dict) -> pd.DataFrame:
    """Rename portal columns to the canonical schema and filter to mechanical permits."""
    fields = j["source"]["fields"]
    out = pd.DataFrame()
    for canon in CANONICAL:
        col = fields.get(canon)
        if col is None:
            out[canon] = None
        elif isinstance(col, list):  # concatenate several text columns into description
            out[canon] = df[col].astype(str).agg(" | ".join, axis=1)
        else:
            out[canon] = df[col] if col in df.columns else None
    out["issued"] = pd.to_datetime(out["issued"], errors="coerce", utc=True).dt.tz_localize(None)
    out["jurisdiction"] = j["name"]
    out["market"] = j["market"]

    # Signal definition: ANY permit whose text mentions heat pump work counts,
    # including electrical service upgrades and building permits. The optional
    # mechanical_filter is only applied when the source asks for it explicitly;
    # otherwise permits with an empty description are dropped (no text, no signal).
    flt = j["source"].get("mechanical_filter")
    if flt and j["source"].get("apply_mechanical_filter", False):
        col, pattern = flt["column"], flt["regex"]
        mask = df[col].astype(str).str.contains(pattern, case=False, regex=True, na=False)
        out = out[mask.values]
    else:
        out = out[out["description"].fillna("").astype(str).str.strip() != ""]
    return out.reset_index(drop=True)


_MECH = r"mechanical|hvac|heating|cooling"
_ELEC = r"electrical|electric|service\s*upgrade|esu|panel"


def permit_type_bucket(permit_type) -> str:
    """Collapse portal-specific permit type labels into mechanical / electrical / other."""
    t = str(permit_type or "")
    if re.search(_MECH, t, re.IGNORECASE):
        return "mechanical"
    if re.search(_ELEC, t, re.IGNORECASE):
        return "electrical"
    return "other"


# ---------------------------------------------------------------------------
# Aggregate
# ---------------------------------------------------------------------------

def window_counts(df: pd.DataFrame, asof: pd.Timestamp, months: int) -> dict:
    start = asof - pd.DateOffset(months=months)
    w = df[(df["issued"] > start) & (df["issued"] <= asof)]
    hp = w[w["is_heat_pump"] == True]  # noqa: E712
    amb = w[w["is_heat_pump"].isna()]
    types = hp["system_type"].value_counts()
    via = hp["permit_type"].map(permit_type_bucket).value_counts()
    return {
        f"permits_with_text_{months}m": len(w),
        f"hvac_permits_{months}m": len(hp) + len(amb),   # permits with any HVAC language
        f"heat_pump_confirmed_{months}m": len(hp),
        f"hvac_ambiguous_{months}m": len(amb),
        f"hp_via_mechanical_{months}m": int(via.get("mechanical", 0)),
        f"hp_via_electrical_{months}m": int(via.get("electrical", 0)),
        f"hp_via_other_permit_{months}m": int(via.get("other", 0)),
        f"ductless_{months}m": int(types.get("ductless", 0)),
        f"dual_fuel_{months}m": int(types.get("dual_fuel", 0)),
        f"ducted_{months}m": int(types.get("ducted", 0)),
        f"type_unknown_{months}m": int(types.get("unknown", 0)),
    }


def per_capita(row: dict, denom: Denominator) -> dict:
    out = dict(row)
    for m in (12, 36):
        conf = row[f"heat_pump_confirmed_{m}m"]
        upper = conf + row[f"hvac_ambiguous_{m}m"]
        annual = 12 / m
        out[f"hp_per_10k_pop_{m}m_annualised_low"] = round(conf * annual / denom.population * 10_000, 2)
        out[f"hp_per_10k_pop_{m}m_annualised_high"] = round(upper * annual / denom.population * 10_000, 2)
        if denom.single_family_units:
            out[f"hp_per_1k_sf_units_{m}m_annualised_low"] = round(conf * annual / denom.single_family_units * 1_000, 2)
            out[f"hp_per_1k_sf_units_{m}m_annualised_high"] = round(upper * annual / denom.single_family_units * 1_000, 2)
    out["population"] = denom.population
    out["single_family_units"] = denom.single_family_units
    out["denominator_source"] = denom.source
    return out


def resolve_denominator(cfg: dict, offline: bool) -> Denominator:
    geo = cfg.get("census")
    if geo and not offline:
        try:
            return fetch_denominator(geo["state"], geo["type"], geo["fips"])
        except Exception as exc:  # noqa: BLE001
            print(f"  census API failed for {cfg['name']}: {exc}; using fallback", file=sys.stderr)
    return fallback_denominator(cfg)


def run(markets_filter: list[str] | None, offline: bool, asof: pd.Timestamp) -> None:
    cfg = load_sources()
    OUTPUT.mkdir(exist_ok=True)
    all_permits, rows = [], []

    for market in cfg["markets"]:
        if markets_filter and market["key"] not in markets_filter:
            continue
        print(f"== {market['name']}")
        market_denom = resolve_denominator(market, offline)
        covered_pop = 0
        market_frames = []

        for j in market["jurisdictions"]:
            j = {**j, "market": market["key"]}
            print(f"  -- {j['name']} ({j['source']['kind']})", end=" ")
            try:
                df = fetch_jurisdiction(j, offline)
            except Exception as exc:  # noqa: BLE001
                print(f"SKIPPED: {exc}")
                rows.append({"market": market["key"], "jurisdiction": j["name"], "status": f"skipped: {exc}"})
                continue
            df = classify_frame(df)
            print(f"{len(df)} HVAC permits, {(df['is_heat_pump'] == True).sum()} heat pump")  # noqa: E712
            all_permits.append(df)
            market_frames.append(df)
            denom = resolve_denominator(j, offline)
            covered_pop += denom.population
            row = {"market": market["key"], "jurisdiction": j["name"], "status": "ok", "verified_source": j["source"].get("verified", False)}
            row.update(window_counts(df, asof, 12))
            row.update(window_counts(df, asof, 36))
            rows.append(per_capita(row, denom))

        if market_frames:
            mdf = pd.concat(market_frames, ignore_index=True)
            row = {"market": market["key"], "jurisdiction": "MARKET TOTAL (covered jurisdictions)", "status": "ok"}
            row.update(window_counts(mdf, asof, 12))
            row.update(window_counts(mdf, asof, 36))
            covered = Denominator(market["name"], covered_pop, 0, 0, "sum of covered jurisdictions")
            row = per_capita(row, covered)
            row["coverage_share_of_market_pop"] = round(covered_pop / market_denom.population, 3)
            rows.append(row)

    summary = pd.DataFrame(rows)
    summary.to_csv(OUTPUT / "market_summary.csv", index=False)
    if all_permits:
        pd.concat(all_permits, ignore_index=True).to_csv(OUTPUT / "permits_classified.csv", index=False)
    (OUTPUT / "market_summary.md").write_text(render_markdown(summary, asof))
    print(f"\nwrote {OUTPUT / 'market_summary.csv'} and market_summary.md")


def render_markdown(summary: pd.DataFrame, asof: pd.Timestamp) -> str:
    cols = [
        "market", "jurisdiction", "status", "population",
        "hvac_permits_12m", "heat_pump_confirmed_12m", "hvac_ambiguous_12m",
        "hp_via_mechanical_12m", "hp_via_electrical_12m", "hp_via_other_permit_12m",
        "ductless_12m", "dual_fuel_12m", "ducted_12m", "type_unknown_12m",
        "hp_per_10k_pop_12m_annualised_low", "hp_per_10k_pop_12m_annualised_high",
        "coverage_share_of_market_pop",
    ]
    present = [c for c in cols if c in summary.columns]
    lines = [f"# Heat pump permits, trailing 12 months to {asof.date()}", ""]
    lines.append("Low = confirmed heat pump permits. High = confirmed + HVAC permits whose equipment is not stated.")
    lines.append("")
    lines.append(summary[present].to_markdown(index=False))
    return "\n".join(lines) + "\n"


def probe() -> None:
    cfg = load_sources()
    for market in cfg["markets"]:
        for j in market["jurisdictions"]:
            src = j["source"]
            print(f"== {market['key']} / {j['name']} ({src['kind']})")
            try:
                if src["kind"] == "arcgis":
                    res = fetch.probe_arcgis(src["layer_url"])
                elif src["kind"] == "socrata":
                    res = fetch.probe_socrata(src["domain"], src["dataset_id"])
                elif src["kind"] == "csv" and src.get("ckan"):
                    res = fetch.probe_ckan(src["ckan"]["portal"], src["ckan"]["dataset"])
                else:
                    print("   (no probe for this kind)")
                    continue
                fetch.dump_probe(res, OUTPUT / "probes" / f"{market['key']}__{j['name'].replace(' ', '_')}.json")
                for f in res.get("fields") or res.get("columns") or res.get("resources") or []:
                    print("   ", f)
            except Exception as exc:  # noqa: BLE001
                print(f"   FAILED: {exc}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--market", action="append", help="market key to run (repeatable)")
    ap.add_argument("--offline", action="store_true", help="no network: cache and fallbacks only")
    ap.add_argument("--probe", action="store_true", help="print endpoint schemas and exit")
    ap.add_argument("--asof", default=dt.date.today().isoformat())
    args = ap.parse_args()
    if args.probe:
        probe()
        return
    run(args.market, args.offline, pd.Timestamp(args.asof))


if __name__ == "__main__":
    main()
