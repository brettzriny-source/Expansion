"""Classify mechanical permit descriptions for heat pump work and system type.

Permit descriptions are free text written by contractors and permit clerks.
This module is a rules-based classifier tuned for high precision on
"is this a heat pump" and honest uncertainty on system type. It is not
machine learning; every rule is readable and auditable.

Two outputs per permit:

1. ``is_heat_pump``: True / False / None. None means the description is an
   HVAC permit that does not say what equipment is installed (e.g. "replace
   3 ton condenser"). These are reported separately as "ambiguous HVAC"
   rather than silently dropped, because the ambiguous bucket is often larger
   than the confirmed bucket and its size is the single most important
   accuracy caveat.

2. ``system_type``: one of
     - ``ductless``   mini-split / ductless / multi-zone wall units
     - ``dual_fuel``  heat pump paired with a gas or oil furnace
     - ``ducted``     central / split / package heat pump, no furnace mentioned
     - ``unknown``    heat pump confirmed, configuration not stated
   Only populated when ``is_heat_pump`` is True.

Water heaters and pool heaters are excluded explicitly: "heat pump water
heater" is heat pump work but not space conditioning, and pool heat pumps are
common in Phoenix and Charlotte permit data.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

# ---------------------------------------------------------------------------
# Patterns
# ---------------------------------------------------------------------------

_HP_POSITIVE = re.compile(
    r"""
    \bheat[\s\-]*pump\b
    | \bhspf\b                                   # heating efficiency rating only exists for heat pumps
    | \bmini[\s\-]*split\b
    | \bductless\b
    | \bmulti[\s\-]*zone\b
    | \bcold[\s\-]*climate\b
    | \bair[\s\-]*source\b
    | \bgeothermal\b
    | \bground[\s\-]*source\b
    | \bvrf\b | \bvrv\b
    | \bmitsubishi\b | \bfujitsu\b | \bdaikin\b | \bgree\b | \bmr\.?\s*slim\b | \bhyper[\s\-]*heat\b
    | \bbosch\s+ids\b | \bcarrier\s+infinity\s+(?:24|25)\w*\b
    | \bmrcool\b | \bpioneer\s+mini\b | \bsenville\b | \bcooper\s*&?\s*hunter\b
    """,
    re.IGNORECASE | re.VERBOSE,
)

# "HP" / "H/P" as a contractor abbreviation. Only trusted when the rest of the
# text is recognisably HVAC (tonnage, split system, changeout ...), otherwise
# "HP" is as likely to be horsepower on a pool pump permit.
_HP_ABBREV = re.compile(r"\bh/?p\b", re.IGNORECASE)

# Phrases that contain "heat pump" but describe a different appliance. These
# are removed from the text before the positive search runs.
_HP_EXCLUDE = re.compile(
    r"""
    \bheat[\s\-]*pump\s+water\s+heater\b
    | \bhpwh\b
    | \bhybrid\s+water\s+heater\b
    | \bpool\s+heat[\s\-]*pump\b | \bheat[\s\-]*pump\s+pool\s+heater\b
    | \bspa\s+heat[\s\-]*pump\b
    """,
    re.IGNORECASE | re.VERBOSE,
)

# Appliance context that makes a bare "heat pump" mention untrustworthy unless
# a space-conditioning signal is also present.
_NON_SPACE_CONTEXT = re.compile(r"\bpool\b|\bspa\b|\bhot\s*tub\b|\bdryer\b", re.IGNORECASE)
_SPACE_CONDITIONING = re.compile(
    r"\bmini[\s\-]*split\b|\bductless\b|\b\d+(?:\.\d+)?\s*[\-]?\s*ton\b|\bsplit\s+system\b|\bair\s*handler\b"
    r"|\bhspf\b|\bseer2?\b|\bfurnace\b|\bhvac\b|\bcondens\w+\b|\bduct\w*\b|\bthermostat\b",
    re.IGNORECASE,
)

# Explicit non-heat-pump equipment. If one of these appears with no positive
# heat pump signal, the permit is classified False rather than None.
_HP_NEGATIVE = re.compile(
    r"""
    \b(?:gas|propane|oil|lp)\s+(?:furnace|boiler)\b
    | \bboiler\b
    | \bfurnace\s+only\b
    | \bstraight\s+cool\b
    | \ba/?c\s+only\b
    | \bair\s+conditioner\s+only\b
    | \bcooling\s+only\b
    | \bgas\s+pack(?:age)?\b
    | \bwater\s+heater\b
    | \bpool\b | \bspa\b | \bhot\s*tub\b
    | \bduct(?:work)?\s+only\b
    | \bexhaust\s+fan\b | \brange\s+hood\b | \bbath\s+fan\b
    | \bgas\s+(?:line|piping)\b
    | \bfireplace\b
    """,
    re.IGNORECASE | re.VERBOSE,
)

# Generic HVAC language that tells us it is an HVAC permit but not what kind.
_HVAC_GENERIC = re.compile(
    r"""
    \bhvac\b | \bcondens(?:er|ing\s+unit)\b | \bair\s*handler\b | \bsplit\s+system\b
    | \bpackage\s+unit\b | \brooftop\s+unit\b | \brtu\b | \bevaporator\b | \bcoil\b
    | \ba/?c\b | \bair\s+condition\w*\b | \bcooling\b | \bheating\b
    | \b\d+(?:\.\d+)?\s*ton\b | \bseer2?\b | \bchange[\s\-]*out\b | \bchangeout\b
    | \bfurnace\b
    """,
    re.IGNORECASE | re.VERBOSE,
)

_DUCTLESS = re.compile(
    r"\bmini[\s\-]*split\b|\bductless\b|\bmulti[\s\-]*zone\b|\bwall[\s\-]*(?:mount|unit|cassette)\b"
    r"|\bmitsubishi\b|\bfujitsu\b|\bmr\.?\s*slim\b|\bmrcool\b|\bsenville\b|\bpioneer\s+mini\b|\bcooper\s*&?\s*hunter\b"
    r"|\b(?:single|one|two|three|four|1|2|3|4|5)[\s\-]*(?:zone|head)s?\b",
    re.IGNORECASE,
)

_FURNACE = re.compile(
    r"\bfurnace\b|\bdual[\s\-]*fuel\b|\bhybrid\s+(?:heat|system)\b|\bgas\s+(?:back[\s\-]*up|heat)\b|\bfossil\s+fuel\s+kit\b",
    re.IGNORECASE,
)

# Daikin and Gree make both ducted and ductless equipment, so they confirm a
# heat pump but do not by themselves imply ductless.
_DUCTED_HINT = re.compile(
    r"\bsplit\s+system\b|\bpackage\s+unit\b|\bpackage\s+heat\s+pump\b|\bair\s*handler\b|\bducted\b|\bcentral\b|\bcoil\b",
    re.IGNORECASE,
)

_TONNAGE = re.compile(r"\b(\d+(?:\.\d+)?)\s*[\-]?\s*ton\b", re.IGNORECASE)


@dataclass(frozen=True)
class Classification:
    is_heat_pump: Optional[bool]
    system_type: Optional[str]
    tonnage: Optional[float]
    matched: str  # the text fragment that drove the decision, for auditing


def classify(description: Optional[str]) -> Classification:
    """Classify one permit description. Safe on None/empty input."""
    text = (description or "").strip()
    if not text:
        return Classification(None, None, None, "")

    excluded = _HP_EXCLUDE.search(text)
    searchable = _HP_EXCLUDE.sub(" ", text)

    pos = _HP_POSITIVE.search(searchable)
    if pos is None and _HP_ABBREV.search(searchable) and _SPACE_CONDITIONING.search(searchable):
        pos = _HP_ABBREV.search(searchable)

    if pos and _NON_SPACE_CONTEXT.search(searchable) and not _SPACE_CONDITIONING.search(searchable):
        # "pool heat pump", "heat pump for spa": not space conditioning.
        return Classification(False, None, None, _NON_SPACE_CONTEXT.search(searchable).group(0))

    if pos:
        return Classification(True, _system_type(searchable), _tonnage(searchable), pos.group(0))

    if excluded:
        return Classification(False, None, _tonnage(text), excluded.group(0))

    neg = _HP_NEGATIVE.search(text)
    if neg:
        return Classification(False, None, _tonnage(text), neg.group(0))

    generic = _HVAC_GENERIC.search(text)
    if generic:
        return Classification(None, None, _tonnage(text), generic.group(0))

    # Not recognisably HVAC at all (e.g. "water softener", "gas log set").
    return Classification(False, None, None, "")


def _system_type(text: str) -> str:
    if _DUCTLESS.search(text):
        return "ductless"
    if _FURNACE.search(text):
        return "dual_fuel"
    if _DUCTED_HINT.search(text) or _TONNAGE.search(text):
        return "ducted"
    return "unknown"


def _tonnage(text: str) -> Optional[float]:
    m = _TONNAGE.search(text)
    if not m:
        return None
    try:
        value = float(m.group(1))
    except ValueError:
        return None
    # Residential range only; anything else is commercial or a typo.
    return value if 0.5 <= value <= 10 else None


def classify_frame(df, description_col: str = "description"):
    """Vectorised helper for pandas: adds is_heat_pump, system_type, tonnage, matched."""
    results = df[description_col].map(classify)
    df = df.copy()
    df["is_heat_pump"] = results.map(lambda c: c.is_heat_pump)
    df["system_type"] = results.map(lambda c: c.system_type)
    df["tonnage"] = results.map(lambda c: c.tonnage)
    df["matched"] = results.map(lambda c: c.matched)
    return df
