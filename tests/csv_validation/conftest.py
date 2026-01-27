"""
Pytest fixtures for CSV data validation.

Design for CI/CD efficiency:
- Session-scoped fixtures load CSVs once per test run
- In-memory validation only (no DB/API calls)
- Estimated runtime: <5 seconds for full validation
"""

import csv
from pathlib import Path
from typing import Any

import pytest

from .game_config import GAME_CONFIGS, GameConfig

CSV_DIR = Path(__file__).parent.parent.parent / "data" / "v2" / "csv"


def load_csv(filename: str) -> list[dict[str, Any]]:
    filepath = CSV_DIR / filename
    if not filepath.exists():
        pytest.fail(f"CSV file not found: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


@pytest.fixture(scope="session")
def encounters_data() -> list[dict[str, Any]]:
    return load_csv("encounters.csv")


@pytest.fixture(scope="session")
def encounter_slots_data() -> list[dict[str, Any]]:
    return load_csv("encounter_slots.csv")


@pytest.fixture(scope="session")
def encounter_methods_data() -> list[dict[str, Any]]:
    return load_csv("encounter_methods.csv")


@pytest.fixture(scope="session")
def location_areas_data() -> list[dict[str, Any]]:
    return load_csv("location_areas.csv")


@pytest.fixture(scope="session")
def encounter_methods_lookup(encounter_methods_data) -> dict[str, dict]:
    return {row["id"]: row for row in encounter_methods_data}


@pytest.fixture(scope="session")
def encounter_slots_lookup(encounter_slots_data) -> dict[str, dict]:
    return {row["id"]: row for row in encounter_slots_data}


@pytest.fixture(scope="session")
def location_areas_lookup(location_areas_data) -> dict[str, dict]:
    return {row["id"]: row for row in location_areas_data}


def get_encounters_for_version_group(
    encounters: list[dict],
    slots: dict[str, dict],
    version_group_id: int,
) -> list[dict]:
    valid_slot_ids = {
        slot_id
        for slot_id, slot in slots.items()
        if slot.get("version_group_id") == str(version_group_id)
    }
    return [enc for enc in encounters if enc.get("encounter_slot_id") in valid_slot_ids]


@pytest.fixture(
    scope="session",
    params=list(GAME_CONFIGS.values()),
    ids=list(GAME_CONFIGS.keys()),
)
def game_config(request) -> GameConfig:
    """Parametrized fixture that yields each game config once per session."""
    return request.param


@pytest.fixture(scope="session")
def game_encounters(game_config, encounters_data, encounter_slots_lookup) -> list[dict]:
    """Encounters filtered to the current game's version group."""
    return get_encounters_for_version_group(
        encounters_data, encounter_slots_lookup, game_config.version_group_id
    )
