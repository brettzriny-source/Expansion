"""End-to-end offline test of the pipeline on a synthetic permit file."""

import importlib
import os
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def _load_run(tmp_path):
    os.environ["HP_SOURCES"] = str(ROOT / "tests" / "fixtures" / "sources_fixture.yaml")
    os.environ["HP_OUTPUT"] = str(tmp_path / "out")
    os.environ["HP_CACHE"] = str(tmp_path / "cache")
    import pipeline.run as run  # noqa: WPS433

    return importlib.reload(run)


def test_pipeline_offline(tmp_path):
    run = _load_run(tmp_path)
    run.run(None, offline=True, asof=pd.Timestamp("2026-09-18"))

    summary = pd.read_csv(tmp_path / "out" / "market_summary.csv")
    permits = pd.read_csv(tmp_path / "out" / "permits_classified.csv")

    # Only mechanical permits survive the filter: 10 of 12 rows.
    assert len(permits) == 10

    city = summary[summary["jurisdiction"] == "Fixture City"].iloc[0]
    # Trailing 12 months to 2026-09-18 covers 2025-09-18 onward: 8 mechanical permits.
    assert city["hvac_permits_12m"] == 8
    # Confirmed heat pumps in window: M-1001, M-1003, M-1005, M-1007 = 4.
    # Not counted: M-1002 (furnace+AC -> False), M-1004 (ambiguous), M-1006 (HPWH), M-1010 (pool).
    assert city["heat_pump_confirmed_12m"] == 4
    assert city["hvac_ambiguous_12m"] == 1
    assert city["ductless_12m"] == 2
    assert city["dual_fuel_12m"] == 1
    assert city["ducted_12m"] == 1
    # 4 per 100k pop annualised = 0.4 per 10k
    assert city["hp_per_10k_pop_12m_annualised_low"] == 0.4
    assert city["hp_per_10k_pop_12m_annualised_high"] == 0.5
    assert city["denominator_source"].startswith("fallback")

    # 36 month window adds M-1008 (2024-03) but not M-1009 (2023-01).
    assert city["heat_pump_confirmed_36m"] == 5

    town = summary[summary["jurisdiction"] == "Fixture Town (no feed)"].iloc[0]
    assert town["status"].startswith("skipped")

    total = summary[summary["jurisdiction"].str.startswith("MARKET TOTAL")].iloc[0]
    assert total["coverage_share_of_market_pop"] == 0.5
    assert total["heat_pump_confirmed_12m"] == 4

    md = (tmp_path / "out" / "market_summary.md").read_text()
    assert "Fixture City" in md
