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
"""

from django.test import SimpleTestCase

from .csv_data import (
    encounter_methods_lookup,
    encounter_slots_lookup,
    encounters_data,
    game_configs,
    get_encounters_for_version_group,
    location_areas_lookup,
)
from .game_config import GameConfig


def parse_int(value, default=0):
    if value is None or value == "":
        return default
    return int(value)


# =============================================================================
# Structural Validation (all data, game-agnostic)
# =============================================================================


class TestCsvStructure(SimpleTestCase):
    """Foreign key integrity and structural checks across all data."""

    def test_encounters_reference_valid_slots(self):
        invalid = [
            f"id={e['id']} slot={e['encounter_slot_id']}"
            for e in encounters_data
            if e["encounter_slot_id"] not in encounter_slots_lookup
        ]
        self.assertFalse(
            invalid,
            f"{len(invalid)} encounters reference missing slots:\n"
            + "\n".join(invalid[:10]),
        )

    def test_encounters_reference_valid_location_areas(self):
        invalid = [
            f"id={e['id']} area={e['location_area_id']}"
            for e in encounters_data
            if e["location_area_id"] not in location_areas_lookup
        ]
        self.assertFalse(
            invalid,
            f"{len(invalid)} encounters reference missing location areas:\n"
            + "\n".join(invalid[:10]),
        )

    def test_encounter_slots_reference_valid_methods(self):
        from .csv_data import encounter_slots_data

        invalid = [
            f"slot={s['id']} method={s['encounter_method_id']}"
            for s in encounter_slots_data
            if s["encounter_method_id"] not in encounter_methods_lookup
        ]
        self.assertFalse(
            invalid, "Slots reference missing methods:\n" + "\n".join(invalid)
        )

    def test_no_duplicate_encounter_ids(self):
        ids = [e["id"] for e in encounters_data]
        seen = set()
        dupes = set()
        for i in ids:
            if i in seen:
                dupes.add(i)
            seen.add(i)
        self.assertFalse(dupes, f"Duplicate encounter IDs: {sorted(dupes)[:10]}")


# =============================================================================
# Game-Specific Validation (iterated via subTest per game config)
# =============================================================================


class TestGameEncounters(SimpleTestCase):
    """Per-game encounter validation using subTest for each game config."""

    def _get_game_encounters(self, config: GameConfig) -> list[dict]:
        return get_encounters_for_version_group(
            encounters_data, encounter_slots_lookup, config.version_group_id
        )

    def test_has_encounter_data(self):
        for config in game_configs:
            with self.subTest(game=config.name):
                game_encounters = self._get_game_encounters(config)
                self.assertTrue(
                    game_encounters, f"No encounters found for {config.name}"
                )

    def test_pokemon_ids_valid_for_game(self):
        for config in game_configs:
            with self.subTest(game=config.name):
                game_encounters = self._get_game_encounters(config)
                invalid = [
                    f"id={e['id']} pokemon={e['pokemon_id']}"
                    for e in game_encounters
                    if parse_int(e["pokemon_id"]) not in config.valid_pokemon
                ]
                self.assertFalse(
                    invalid,
                    f"Invalid Pokemon for {config.name}:\n"
                    + "\n".join(invalid[:10])
                    + (
                        f"\n... and {len(invalid) - 10} more"
                        if len(invalid) > 10
                        else ""
                    ),
                )

    def test_method_ids_valid_for_game(self):
        for config in game_configs:
            with self.subTest(game=config.name):
                game_encounters = self._get_game_encounters(config)
                invalid_methods = set()
                for enc in game_encounters:
                    slot = encounter_slots_lookup.get(enc["encounter_slot_id"], {})
                    method_id = parse_int(slot.get("encounter_method_id"))
                    if method_id not in config.valid_method_ids:
                        invalid_methods.add(method_id)
                self.assertFalse(
                    invalid_methods,
                    f"Invalid methods for {config.name}: {invalid_methods}\n"
                    f"Valid: {config.valid_method_ids}",
                )

    def test_min_level_not_greater_than_max(self):
        for config in game_configs:
            with self.subTest(game=config.name):
                game_encounters = self._get_game_encounters(config)
                invalid = [
                    f"id={e['id']} min={e['min_level']} max={e['max_level']}"
                    for e in game_encounters
                    if parse_int(e["min_level"]) > parse_int(e["max_level"])
                ]
                self.assertFalse(
                    invalid, "min_level > max_level:\n" + "\n".join(invalid)
                )

    def test_version_exclusives_correct(self):
        for config in game_configs:
            if not config.version_exclusives:
                continue
            with self.subTest(game=config.name):
                game_encounters = self._get_game_encounters(config)
                wrong = []
                for e in game_encounters:
                    pid = parse_int(e["pokemon_id"])
                    vid = parse_int(e["version_id"])
                    if pid in config.version_exclusives:
                        expected = config.version_exclusives[pid]
                        if vid != expected:
                            wrong.append(
                                f"id={e['id']} pokemon={pid} "
                                f"version={vid} expected={expected}"
                            )
                self.assertFalse(
                    wrong,
                    f"Wrong version for exclusives:\n"
                    + "\n".join(wrong[:10])
                    + (f"\n... and {len(wrong) - 10} more" if len(wrong) > 10 else ""),
                )

    def test_no_duplicate_encounters(self):
        for config in game_configs:
            with self.subTest(game=config.name):
                game_encounters = self._get_game_encounters(config)
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
                self.assertFalse(
                    dupes,
                    f"Duplicates in {config.name}:\n"
                    + "\n".join(dupes[:10])
                    + (f"\n... and {len(dupes) - 10} more" if len(dupes) > 10 else ""),
                )

    def test_version_ids_valid_for_game(self):
        for config in game_configs:
            with self.subTest(game=config.name):
                game_encounters = self._get_game_encounters(config)
                invalid_versions = set()
                for e in game_encounters:
                    vid = parse_int(e["version_id"])
                    if vid not in config.version_ids:
                        invalid_versions.add(vid)
                self.assertFalse(
                    invalid_versions,
                    f"Invalid version IDs for {config.name}: {invalid_versions}\n"
                    f"Valid: {config.version_ids}",
                )
