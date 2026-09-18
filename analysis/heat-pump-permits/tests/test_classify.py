"""Offline tests for the permit description classifier.

Descriptions below are modelled on real permit text styles from Accela,
Socrata and ArcGIS permit exports (terse, all caps, abbreviations, typos).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pipeline.classify import classify  # noqa: E402


@pytest.mark.parametrize(
    "text",
    [
        "INSTALL 3 TON HEAT PUMP SPLIT SYSTEM",
        "Replace existing heatpump with new 16 SEER heat-pump",
        "HVAC CHANGEOUT - 4 TON HP SPLIT SYSTEM",
        "Install Mitsubishi Hyper Heat mini split, 3 zones",
        "ductless mini-split single zone bedroom",
        "Install new 2.5 ton 15.2 SEER2 8.1 HSPF system",  # HSPF implies heat pump
        "GEOTHERMAL GROUND SOURCE HEAT PUMP INSTALL",
        "Replace furnace and install heat pump (dual fuel)",
        "New Bosch IDS 2.0 heat pump with air handler",
        "Install Daikin Fit heat pump system",
    ],
)
def test_heat_pump_positive(text):
    assert classify(text).is_heat_pump is True


@pytest.mark.parametrize(
    "text",
    [
        "REPLACE GAS FURNACE 80% 60K BTU",
        "Install 50 gal heat pump water heater",
        "HPWH replacement garage",
        "Pool heat pump install",
        "Replace boiler, oil to gas conversion",
        "Straight cool 3 ton condenser and coil",
        "Water heater replacement 40 gal gas",
        "Install range hood and bath fans",
        "GAS LINE FOR NEW RANGE",
        "Water softener install",
        "Furnace only replacement 96% two stage",
    ],
)
def test_heat_pump_negative(text):
    assert classify(text).is_heat_pump is False


@pytest.mark.parametrize(
    "text",
    [
        "REPLACE 3 TON CONDENSER AND COIL",
        "HVAC changeout like for like",
        "Install split system 4 ton 14 SEER",
        "Replace air handler",
        "AC replacement",
        "Package unit changeout rooftop",
    ],
)
def test_ambiguous_hvac_is_none(text):
    assert classify(text).is_heat_pump is None


def test_empty_and_none():
    assert classify(None).is_heat_pump is None
    assert classify("").is_heat_pump is None
    assert classify("   ").is_heat_pump is None


@pytest.mark.parametrize(
    "text,expected",
    [
        ("Install Mitsubishi mini split 2 zone", "ductless"),
        ("ductless heat pump wall mount", "ductless"),
        ("Fujitsu Halcyon single zone", "ductless"),
        ("Replace furnace and add heat pump, dual fuel", "dual_fuel"),
        ("Heat pump with gas backup", "dual_fuel"),
        ("Hybrid heat system: 96% furnace + 3 ton HP", "dual_fuel"),
        ("Install 3 ton heat pump split system with air handler", "ducted"),
        ("PACKAGE HEAT PUMP CHANGEOUT 4 TON", "ducted"),
        ("Heat pump", "unknown"),
        ("Install Daikin heat pump", "unknown"),  # Daikin makes both; no config given
    ],
)
def test_system_type(text, expected):
    c = classify(text)
    assert c.is_heat_pump is True
    assert c.system_type == expected


def test_system_type_not_set_for_non_heat_pump():
    assert classify("Replace gas furnace").system_type is None
    assert classify("Replace 3 ton condenser").system_type is None


@pytest.mark.parametrize(
    "text,expected",
    [
        ("Install 3 ton heat pump", 3.0),
        ("2.5-ton HP split system", 2.5),
        ("Heat pump replacement", None),
        ("Install 40 ton rooftop heat pump", None),  # out of residential range
    ],
)
def test_tonnage(text, expected):
    assert classify(text).tonnage == expected


def test_hpwh_plus_space_heat_pump_counts_as_heat_pump():
    c = classify("Install heat pump water heater and 3 ton heat pump split system")
    assert c.is_heat_pump is True
    assert c.system_type == "ducted"


def test_matched_fragment_recorded():
    c = classify("INSTALL 3 TON HEAT PUMP")
    assert c.matched.lower().replace("-", " ") in "install 3 ton heat pump"
