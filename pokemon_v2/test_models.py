import csv
import os
import re
from django.test import TestCase
from pokemon_v2.models import *


class AbilityTestCase(TestCase):
    def setUp(self):
        Ability.objects.create(name="Smell", generation_id=3, is_main_series=True)

    def fields_are_valid(self):
        smell = Ability.objects.get(name="Smell")
        self.assertEqual(smell.generation_id, 3)


class CSVResourceNameValidationTestCase(TestCase):
    """
    Test that all resource identifiers in CSV files follow ASCII slug format.

    Resource identifiers are used in API URLs and should be URL-safe ASCII slugs
    (lowercase letters, numbers, and hyphens only).

    This test validates the data source (CSV files) before it's loaded into the database.
    """

    # Pattern for valid resource identifiers: lowercase letters, numbers, and hyphens only
    VALID_IDENTIFIER_PATTERN = re.compile(r"^[a-z0-9-]+$")

    # CSV files that contain an 'identifier' column to validate
    # Format: (filename, identifier_column_name)
    CSV_FILES_TO_VALIDATE = [
        ("abilities.csv", "identifier"),
        ("berry_firmness.csv", "identifier"),
        ("conquest_episodes.csv", "identifier"),
        ("conquest_kingdoms.csv", "identifier"),
        ("conquest_move_displacements.csv", "identifier"),
        ("conquest_move_ranges.csv", "identifier"),
        ("conquest_stats.csv", "identifier"),
        ("conquest_warrior_archetypes.csv", "identifier"),
        ("conquest_warrior_skills.csv", "identifier"),
        ("conquest_warrior_stats.csv", "identifier"),
        ("conquest_warriors.csv", "identifier"),
        ("contest_types.csv", "identifier"),
        ("egg_groups.csv", "identifier"),
        ("encounter_conditions.csv", "identifier"),
        ("encounter_condition_values.csv", "identifier"),
        ("encounter_methods.csv", "identifier"),
        ("evolution_triggers.csv", "identifier"),
        ("genders.csv", "identifier"),
        ("generations.csv", "identifier"),
        ("growth_rates.csv", "identifier"),
        ("items.csv", "identifier"),
        ("item_categories.csv", "identifier"),
        ("item_flags.csv", "identifier"),
        ("item_fling_effects.csv", "identifier"),
        ("item_pockets.csv", "identifier"),
        ("languages.csv", "identifier"),
        ("locations.csv", "identifier"),
        ("location_areas.csv", "identifier"),
        ("moves.csv", "identifier"),
        ("move_battle_styles.csv", "identifier"),
        ("move_damage_classes.csv", "identifier"),
        ("move_flags.csv", "identifier"),
        ("move_meta_ailments.csv", "identifier"),
        ("move_meta_categories.csv", "identifier"),
        ("move_targets.csv", "identifier"),
        ("natures.csv", "identifier"),
        ("pal_park_areas.csv", "identifier"),
        ("pokeathlon_stats.csv", "identifier"),
        ("pokedexes.csv", "identifier"),
        ("pokemon.csv", "identifier"),
        ("pokemon_colors.csv", "identifier"),
        ("pokemon_forms.csv", "identifier"),
        ("pokemon_habitats.csv", "identifier"),
        ("pokemon_move_methods.csv", "identifier"),
        ("pokemon_shapes.csv", "identifier"),
        ("pokemon_species.csv", "identifier"),
        ("regions.csv", "identifier"),
        ("stats.csv", "identifier"),
        ("types.csv", "identifier"),
        ("versions.csv", "identifier"),
        ("version_groups.csv", "identifier"),
    ]

    def get_csv_path(self, filename):
        """Get the absolute path to a CSV file in data/v2/csv/"""
        from django.conf import settings

        base_dir = settings.BASE_DIR
        return os.path.join(base_dir, "data", "v2", "csv", filename)

    def test_all_csv_identifiers_are_ascii_slugs(self):
        """
        Validate that all resource identifiers in CSV files follow the ASCII slug format.

        Identifiers should only contain:
        - Lowercase letters (a-z)
        - Numbers (0-9)
        - Hyphens (-)

        This test will fail if any CSV contains identifiers with:
        - Unicode characters (ñ, ', é, etc.)
        - Uppercase letters
        - Spaces
        - Special characters (&, (), ', etc.)
        """
        violations = []
        missing_files = []

        for filename, identifier_column in self.CSV_FILES_TO_VALIDATE:
            csv_path = self.get_csv_path(filename)

            # Track missing files to report at the end
            if not os.path.exists(csv_path):
                missing_files.append(filename)
                continue

            try:
                with open(csv_path, "r", encoding="utf-8") as csvfile:
                    reader = csv.DictReader(csvfile)

                    # Check if the identifier column exists
                    if identifier_column not in reader.fieldnames:
                        violations.append(
                            {
                                "file": filename,
                                "row": "N/A",
                                "id": "N/A",
                                "identifier": f"Column '{identifier_column}' not found",
                            }
                        )
                        continue

                    for row_num, row in enumerate(
                        reader, start=2
                    ):  # Start at 2 (after header)
                        identifier = row.get(identifier_column, "").strip()

                        # Skip empty identifiers
                        if not identifier:
                            continue

                        # Check if identifier matches the pattern
                        if not self.VALID_IDENTIFIER_PATTERN.match(identifier):
                            violations.append(
                                {
                                    "file": filename,
                                    "row": row_num,
                                    "id": row.get("id", "N/A"),
                                    "identifier": identifier,
                                }
                            )

            except Exception as e:
                violations.append(
                    {
                        "file": filename,
                        "row": "N/A",
                        "id": "N/A",
                        "identifier": f"Error reading file: {str(e)}",
                    }
                )

        # If there are violations or missing files, create a detailed error message
        if violations or missing_files:
            error_lines = []

            # Report missing files first
            if missing_files:
                error_lines.append("\n\nMissing CSV files:")
                for filename in missing_files:
                    error_lines.append(f"  - {filename}")
                error_lines.append(
                    "\nAll CSV files listed in CSV_FILES_TO_VALIDATE must exist."
                )

            # Report violations
            if violations:
                error_lines.append(
                    "\n\nFound {} resource(s) with invalid identifiers (not ASCII slugs):".format(
                        len(violations)
                    )
                )
                error_lines.append("\nIdentifiers must match pattern: ^[a-z0-9-]+$")
                error_lines.append("\nInvalid identifiers found in CSV files:")

                for v in violations:
                    error_lines.append(
                        "  - {file} (row {row}, id={id}): {identifier}".format(**v)
                    )

                error_lines.append(
                    "\nThese identifiers contain invalid characters and must be normalized."
                )
                error_lines.append(
                    "Update the CSV files in data/v2/csv/ to fix these identifiers."
                )
                error_lines.append("\nSuggested fixes:")
                error_lines.append(
                    "  - Remove Unicode apostrophes (') and replace with regular hyphens or remove"
                )
                error_lines.append("  - Remove Unicode letters (ñ → n)")
                error_lines.append(
                    "  - Remove parentheses and other special characters"
                )
                error_lines.append("  - Convert to lowercase")

            self.fail("\n".join(error_lines))

    def test_identifier_pattern_examples(self):
        """Test that the validation pattern works correctly with example identifiers."""
        # Valid identifiers
        valid_identifiers = [
            "pikachu",
            "charizard-mega-x",
            "mr-mime",
            "ho-oh",
            "type-null",
            "item-123",
            "mega-stone",
        ]

        for identifier in valid_identifiers:
            self.assertTrue(
                self.VALID_IDENTIFIER_PATTERN.match(identifier),
                f"{identifier} should be valid but was rejected",
            )

        # Invalid identifiers
        invalid_identifiers = [
            "Pikachu",  # Uppercase
            "Mr. Mime",  # Space and period
            "kofu's-wallet",  # Unicode apostrophe
            "jalapeño",  # Unicode ñ
            "steel-bottle-(r)",  # Parentheses
            "b&w-grass-tablecloth",  # Ampersand
            "farfetch'd",  # Apostrophe
            "kofu's-wallet",  # Regular apostrophe
        ]

        for identifier in invalid_identifiers:
            self.assertFalse(
                self.VALID_IDENTIFIER_PATTERN.match(identifier),
                f"{identifier} should be invalid but was accepted",
            )
