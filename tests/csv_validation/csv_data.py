"""
CSV data loading helpers for encounter validation tests.

Design for CI/CD efficiency:
- Module-level caching loads CSVs once per import
- In-memory validation only (no DB/API calls)
"""

import csv
from pathlib import Path
from typing import Any

from .game_config import GAME_CONFIGS

CSV_DIR = Path(__file__).parent.parent.parent / "data" / "v2" / "csv"


def load_csv(filename: str) -> list[dict[str, Any]]:
    filepath = CSV_DIR / filename
    if not filepath.exists():
        raise FileNotFoundError(f"CSV file not found: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


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


# Module-level cached data (loaded once on import)
encounters_data = load_csv("encounters.csv")
encounter_slots_data = load_csv("encounter_slots.csv")
encounter_methods_data = load_csv("encounter_methods.csv")
location_areas_data = load_csv("location_areas.csv")

encounter_methods_lookup = {row["id"]: row for row in encounter_methods_data}
encounter_slots_lookup = {row["id"]: row for row in encounter_slots_data}
location_areas_lookup = {row["id"]: row for row in location_areas_data}

game_configs = list(GAME_CONFIGS.values())
