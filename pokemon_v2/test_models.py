import csv
import os
import re

from django.conf import settings
from django.test import TestCase
from typing_extensions import override

from pokemon_v2.models import *


class AbilityTestCase(TestCase):
    @override
    def setUp(self):
        Ability.objects.create(name="Smell", generation_id=3, is_main_series=True)

    def fields_are_valid(self):
        smell = Ability.objects.get(name="Smell")
        assert smell.generation is not None
        self.assertEqual(smell.generation.pk, 3)


class EncounterPokemonDetailTestCase(TestCase):
    def test_unique_encounter_pokemon_details(self):
        csv_dir = os.path.join(settings.BASE_DIR, "data", "v2", "csv")
        with open(os.path.join(csv_dir, "encounter_pokemon_details.csv")) as infile:
            reader = csv.DictReader(infile)
            encounter_ids = []
            duplicate_ids = []
            for row in reader:
                if row["encounter_id"] in encounter_ids:
                    duplicate_ids.append(row["encounter_id"])
                else:
                    encounter_ids.append(row["encounter_id"])

            if duplicate_ids:
                self.fail(f"Duplicate encounter ID(s) found in encounter_pokemon_details.csv: {duplicate_ids}")


class CSVResourceNameValidationTestCase(TestCase):
    """
    Test that all resource identifiers in CSV files follow ASCII slug format.

    Resource identifiers are used in API URLs and should be URL-safe ASCII slugs
    (lowercase letters, numbers, and hyphens only).

    This test validates the data source (CSV files) before it's loaded into the database.
    """

    # Pattern for valid resource identifiers: lowercase letters, numbers, and hyphens only
    VALID_IDENTIFIER_PATTERN = re.compile(r"^[a-z0-9-]+$")

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
        csv_dir = os.path.join(settings.BASE_DIR, "data", "v2", "csv")

        for filename in sorted(os.listdir(csv_dir)):
            if not filename.endswith(".csv"):
                continue

            csv_path = os.path.join(csv_dir, filename)

            try:
                with open(csv_path, encoding="utf-8") as csvfile:
                    reader = csv.DictReader(csvfile)

                    if "identifier" not in (reader.fieldnames or []):
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

            except Exception as e:  # noqa: BLE001
                violations.append(
                    {
                        "file": filename,
                        "row": "N/A",
                        "id": "N/A",
                        "identifier": f"Error reading file: {e!s}",
                    }
                )

        error_lines = []

        # Report violations
        if violations:
            error_lines.extend(
                (
                    f"\n\nFound {len(violations)} resource(s) with invalid identifiers (not ASCII slugs):",
                    "\nIdentifiers must match pattern: ^[a-z0-9-]+$",
                    "\nInvalid identifiers found in CSV files:",
                )
            )

            error_lines.extend("  - {file} (row {row}, id={id}): {identifier}".format(**v) for v in violations)

            error_lines.extend(
                (
                    "\nThese identifiers contain invalid characters and must be normalized.",
                    "Update the CSV files in data/v2/csv/ to fix these identifiers.",
                    "\nSuggested fixes:",
                    "  - Remove Unicode apostrophes (') and replace with regular hyphens or remove",
                    "  - Remove Unicode letters (ñ → n)",
                    "  - Remove parentheses and other special characters",
                    "  - Convert to lowercase",
                )
            )

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
