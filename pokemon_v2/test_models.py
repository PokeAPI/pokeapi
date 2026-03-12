import csv
import os
import re
from django.conf import settings
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

    # CSV files with 'identifier' column to validate
    CSV_FILES_TO_VALIDATE = [
        "abilities.csv",
        "berry_firmness.csv",
        "conquest_episodes.csv",
        "conquest_kingdoms.csv",
        "conquest_move_displacements.csv",
        "conquest_move_ranges.csv",
        "conquest_stats.csv",
        "conquest_warrior_archetypes.csv",
        "conquest_warrior_skills.csv",
        "conquest_warrior_stats.csv",
        "conquest_warriors.csv",
        "contest_types.csv",
        "egg_groups.csv",
        "encounter_conditions.csv",
        "encounter_condition_values.csv",
        "encounter_methods.csv",
        "evolution_triggers.csv",
        "genders.csv",
        "generations.csv",
        "growth_rates.csv",
        "items.csv",
        "item_categories.csv",
        "item_flags.csv",
        "item_fling_effects.csv",
        "item_pockets.csv",
        "languages.csv",
        "locations.csv",
        "location_areas.csv",
        "moves.csv",
        "move_battle_styles.csv",
        "move_damage_classes.csv",
        "move_flags.csv",
        "move_meta_ailments.csv",
        "move_meta_categories.csv",
        "move_targets.csv",
        "natures.csv",
        "pal_park_areas.csv",
        "pokeathlon_stats.csv",
        "pokedexes.csv",
        "pokemon.csv",
        "pokemon_colors.csv",
        "pokemon_forms.csv",
        "pokemon_habitats.csv",
        "pokemon_move_methods.csv",
        "pokemon_shapes.csv",
        "pokemon_species.csv",
        "regions.csv",
        "stats.csv",
        "types.csv",
        "versions.csv",
        "version_groups.csv",
    ]

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

        for filename in self.CSV_FILES_TO_VALIDATE:
            csv_path = os.path.join(settings.BASE_DIR, "data", "v2", "csv", filename)

            # Track missing files to report at the end
            if not os.path.exists(csv_path):
                missing_files.append(filename)
                continue

            try:
                with open(csv_path, "r", encoding="utf-8") as csvfile:
                    reader = csv.DictReader(csvfile)

                    # Check if the identifier column exists
                    if "identifier" not in reader.fieldnames:
                        violations.append(
                            {
                                "file": filename,
                                "row": "N/A",
                                "id": "N/A",
                                "identifier": "Column 'identifier' not found",
                            }
                        )
                        continue

                    for row_num, row in enumerate(reader, start=2):
                        identifier = row.get("identifier", "").strip()

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
