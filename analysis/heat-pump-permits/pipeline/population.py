"""Population and housing-unit denominators from the Census API.

Uses ACS 1-year estimates (B01003 population, B25001 housing units, and
B25024 units-in-structure for the 1-unit detached + attached share that is
the real addressable base for residential HVAC). Falls back to the static
table in ``sources.yaml`` when the API is unreachable, and flags which one
was used so the report never silently mixes vintages.

Get a free key at https://api.census.gov/data/key_signup.html and export it
as CENSUS_API_KEY. Requests work without a key at a low rate limit.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

import requests

ACS_YEAR = 2023  # latest 1-year vintage available as of the pipeline's authoring
VARS = {
    "B01003_001E": "population",
    "B25001_001E": "housing_units",
    "B25024_002E": "units_1_detached",
    "B25024_003E": "units_1_attached",
}


@dataclass
class Denominator:
    geo_name: str
    population: int
    housing_units: int
    single_family_units: int
    source: str  # "acs1-2023" or "fallback"


def fetch_denominator(state_fips: str, geo_type: str, geo_fips: str, session: Optional[requests.Session] = None) -> Denominator:
    """geo_type is 'place' or 'county'."""
    session = session or requests.Session()
    params = {"get": "NAME," + ",".join(VARS), "for": f"{geo_type}:{geo_fips}", "in": f"state:{state_fips}"}
    key = os.environ.get("CENSUS_API_KEY")
    if key:
        params["key"] = key
    r = session.get(f"https://api.census.gov/data/{ACS_YEAR}/acs/acs1", params=params, timeout=60)
    r.raise_for_status()
    header, row = r.json()
    rec = dict(zip(header, row))
    return Denominator(
        geo_name=rec["NAME"],
        population=int(rec["B01003_001E"]),
        housing_units=int(rec["B25001_001E"]),
        single_family_units=int(rec["B25024_002E"]) + int(rec["B25024_003E"]),
        source=f"acs1-{ACS_YEAR}",
    )


def fallback_denominator(cfg: dict) -> Denominator:
    fb = cfg["population_fallback"]
    return Denominator(
        geo_name=cfg["name"],
        population=int(fb["population"]),
        housing_units=int(fb.get("housing_units", 0)),
        single_family_units=int(fb.get("single_family_units", 0)),
        source="fallback:" + fb.get("note", "sources.yaml"),
    )
