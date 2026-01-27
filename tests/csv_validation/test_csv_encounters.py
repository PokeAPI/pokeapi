"""
CSV encounter data validation tests.

Validates encounter CSV data against game-specific rules. Runs in CI/CD
to catch data quality issues before merge.

Validation criteria (from encounter-collection README):
- All Pokemon IDs are valid for the game
- Encounter method IDs are valid for the game's version group
- Version exclusives only appear with correct version_id
- No duplicate encounter entries
- Foreign key references are valid (slots, location_areas exist)

Performance:
- CSVs loaded once per session via fixtures
- In-memory only (no DB/API calls)
- <5s runtime for full validation
"""

import pytest

from .game_config import GameConfig


def parse_int(value, default=0):
    if value is None or value == "":
        return default
    return int(value)


# =============================================================================
# Structural Validation (all data, game-agnostic)
# =============================================================================


class TestCsvStructure:
    """Foreign key integrity and structural checks across all data."""

    def test_encounters_reference_valid_slots(
        self, encounters_data, encounter_slots_lookup
    ):
        invalid = [
            f"id={e['id']} slot={e['encounter_slot_id']}"
            for e in encounters_data
            if e["encounter_slot_id"] not in encounter_slots_lookup
        ]
        assert not invalid, (
            f"{len(invalid)} encounters reference missing slots:\n"
            + "\n".join(invalid[:10])
        )

    def test_encounters_reference_valid_location_areas(
        self, encounters_data, location_areas_lookup
    ):
        invalid = [
            f"id={e['id']} area={e['location_area_id']}"
            for e in encounters_data
            if e["location_area_id"] not in location_areas_lookup
        ]
        assert not invalid, (
            f"{len(invalid)} encounters reference missing location areas:\n"
            + "\n".join(invalid[:10])
        )

    def test_encounter_slots_reference_valid_methods(
        self, encounter_slots_data, encounter_methods_lookup
    ):
        invalid = [
            f"slot={s['id']} method={s['encounter_method_id']}"
            for s in encounter_slots_data
            if s["encounter_method_id"] not in encounter_methods_lookup
        ]
        assert not invalid, (
            f"Slots reference missing methods:\n" + "\n".join(invalid)
        )

    def test_no_duplicate_encounter_ids(self, encounters_data):
        ids = [e["id"] for e in encounters_data]
        seen = set()
        dupes = set()
        for i in ids:
            if i in seen:
                dupes.add(i)
            seen.add(i)
        assert not dupes, f"Duplicate encounter IDs: {sorted(dupes)[:10]}"


# =============================================================================
# Game-Specific Validation (parametrized by game_config fixture)
# =============================================================================


class TestGameEncounters:
    """Per-game encounter validation, parametrized via game_config fixture."""

    def test_has_encounter_data(self, game_config: GameConfig, game_encounters):
        assert game_encounters, f"No encounters found for {game_config.name}"

    def test_pokemon_ids_valid_for_game(
        self, game_config: GameConfig, game_encounters
    ):
        invalid = [
            f"id={e['id']} pokemon={e['pokemon_id']}"
            for e in game_encounters
            if parse_int(e["pokemon_id"]) not in game_config.valid_pokemon
        ]
        assert not invalid, (
            f"Invalid Pokemon for {game_config.name}:\n"
            + "\n".join(invalid[:10])
            + (f"\n... and {len(invalid) - 10} more" if len(invalid) > 10 else "")
        )

    def test_method_ids_valid_for_game(
        self, game_config: GameConfig, game_encounters, encounter_slots_lookup
    ):
        invalid_methods = set()
        for enc in game_encounters:
            slot = encounter_slots_lookup.get(enc["encounter_slot_id"], {})
            method_id = parse_int(slot.get("encounter_method_id"))
            if method_id not in game_config.valid_method_ids:
                invalid_methods.add(method_id)
        assert not invalid_methods, (
            f"Invalid methods for {game_config.name}: {invalid_methods}\n"
            f"Valid: {game_config.valid_method_ids}"
        )

    def test_min_level_not_greater_than_max(
        self, game_config: GameConfig, game_encounters
    ):
        invalid = [
            f"id={e['id']} min={e['min_level']} max={e['max_level']}"
            for e in game_encounters
            if parse_int(e["min_level"]) > parse_int(e["max_level"])
        ]
        assert not invalid, "min_level > max_level:\n" + "\n".join(invalid)

    def test_version_exclusives_correct(
        self, game_config: GameConfig, game_encounters
    ):
        if not game_config.version_exclusives:
            pytest.skip("No version exclusives defined")
        wrong = []
        for e in game_encounters:
            pid = parse_int(e["pokemon_id"])
            vid = parse_int(e["version_id"])
            if pid in game_config.version_exclusives:
                expected = game_config.version_exclusives[pid]
                if vid != expected:
                    wrong.append(
                        f"id={e['id']} pokemon={pid} version={vid} expected={expected}"
                    )
        assert not wrong, (
            f"Wrong version for exclusives:\n"
            + "\n".join(wrong[:10])
            + (f"\n... and {len(wrong) - 10} more" if len(wrong) > 10 else "")
        )

    def test_no_duplicate_encounters(
        self, game_config: GameConfig, game_encounters
    ):
        seen = set()
        dupes = []
        for e in game_encounters:
            key = (
                e["version_id"],
                e["location_area_id"],
                e["encounter_slot_id"],
                e["pokemon_id"],
                e["min_level"],
                e["max_level"],
            )
            if key in seen:
                dupes.append(f"id={e['id']} {key}")
            seen.add(key)
        assert not dupes, (
            f"Duplicates in {game_config.name}:\n"
            + "\n".join(dupes[:10])
            + (f"\n... and {len(dupes) - 10} more" if len(dupes) > 10 else "")
        )

    def test_version_ids_valid_for_game(
        self, game_config: GameConfig, game_encounters
    ):
        invalid_versions = set()
        for e in game_encounters:
            vid = parse_int(e["version_id"])
            if vid not in game_config.version_ids:
                invalid_versions.add(vid)
        assert not invalid_versions, (
            f"Invalid version IDs for {game_config.name}: {invalid_versions}\n"
            f"Valid: {game_config.version_ids}"
        )
