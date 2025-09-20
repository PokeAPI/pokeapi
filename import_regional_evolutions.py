#!/usr/bin/env python3
"""
Import regional evolution data from CSV into the database
"""
import os
import sys
import csv
import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.local")
django.setup()

from pokemon_v2.models import (
    PokemonEvolution,
    PokemonSpecies,
    Region,
    Item,
    Location,
    EvolutionTrigger,
    Move,
    Type,
)


def get_or_create_trigger(name):
    """Get or create an evolution trigger"""
    trigger, created = EvolutionTrigger.objects.get_or_create(name=name)
    return trigger


def get_or_create_item(name):
    """Get or create an item"""
    if not name or name.lower() in ["null", ""]:
        return None
    try:
        return Item.objects.get(name=name)
    except Item.DoesNotExist:
        print(f"⚠️  Item '{name}' not found")
        return None


def get_or_create_location(name):
    """Get or create a location"""
    if not name or name.lower() in ["null", ""]:
        return None
    try:
        return Location.objects.get(name=name)
    except Location.DoesNotExist:
        print(f"⚠️  Location '{name}' not found")
        return None


def get_or_create_region(name):
    """Get or create a region"""
    if not name or name.lower() in ["null", ""]:
        return None
    try:
        return Region.objects.get(name=name)
    except Region.DoesNotExist:
        print(f"⚠️  Region '{name}' not found")
        return None


def get_or_create_species(name):
    """Get or create a Pokemon species"""
    if not name or name.lower() in ["null", ""]:
        return None
    try:
        return PokemonSpecies.objects.get(name=name)
    except PokemonSpecies.DoesNotExist:
        print(f"⚠️  Pokemon species '{name}' not found")
        return None


def import_regional_evolution_data(csv_file):
    """Import regional evolution data from CSV"""
    print(f"Importing regional evolution data from {csv_file}...")

    imported_count = 0
    skipped_count = 0

    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)

        for row_num, row in enumerate(reader, start=2):  # Start at 2 for header
            try:
                # Get Pokemon species
                pokemon_name = row["pokemon"]
                evolves_to_name = row["evolves_to"]

                pokemon = get_or_create_species(pokemon_name)
                evolves_to = get_or_create_species(evolves_to_name)

                if not pokemon or not evolves_to:
                    print(f"⚠️  Skipping row {row_num}: Missing Pokemon species")
                    skipped_count += 1
                    continue

                # Get evolution trigger
                method = row["method"]
                trigger = get_or_create_trigger(method)

                # Get other fields
                region = get_or_create_region(row["region"])
                item = get_or_create_item(row["item"])
                location = get_or_create_location(row["location"])
                base_form = get_or_create_species(row["base_form_required"])

                # Parse level
                min_level = None
                if row["level"] and row["level"].strip():
                    try:
                        min_level = int(row["level"])
                    except ValueError:
                        print(f"⚠️  Invalid level '{row['level']}' in row {row_num}")
                # Create or update evolution
                evolution, created = PokemonEvolution.objects.get_or_create(
                    evolved_species=evolves_to,
                    evolution_trigger=trigger,
                    defaults={
                        "evolution_item": item,
                        "min_level": min_level,
                        "location": location,
                        "region_restriction": region,
                        "base_form_required": base_form,
                    },
                )

                if created:
                    print(f"✅ Created evolution: {pokemon_name} → {evolves_to_name}")
                    imported_count += 1
                else:
                    # Update existing evolution with new fields
                    evolution.region_restriction = region
                    evolution.base_form_required = base_form
                    evolution.save()
                    print(f"🔄 Updated evolution: {pokemon_name} → {evolves_to_name}")
                    imported_count += 1

            except Exception as e:
                print(f"❌ Error processing row {row_num}: {e}")
                skipped_count += 1

    print(f"\nImport completed!")
    print(f"✅ Imported/Updated: {imported_count}")
    print(f"⚠️  Skipped: {skipped_count}")


def main():
    """Main function"""
    csv_file = "regional_evolutions.csv"

    if not os.path.exists(csv_file):
        print(f"❌ CSV file '{csv_file}' not found")
        return

    import_regional_evolution_data(csv_file)


if __name__ == "__main__":
    main()
