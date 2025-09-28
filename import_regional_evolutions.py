#!/usr/bin/env python3
"""
Import regional evolution data from CSV and update the pokemon_evolution.csv file

REGIONAL EVOLUTION SYSTEM WITH BUILD PROCESS INTEGRATION
========================================================

This script implements the regional evolution system by updating the pokemon_evolution.csv file
with regional metadata. The system works as follows:

1. CSV STRUCTURE:
   - The pokemon_evolution.csv file has been extended with two new columns:
     * region_id: References the Region ID where this evolution is restricted to
     * base_form_id: References the PokemonSpecies ID of the base form required for evolution
   
2. BUILD PROCESS INTEGRATION:
   - The data/v2/build.py file has been updated to handle these new columns
   - The csv_record_to_objects function for PokemonEvolution now includes:
     * region_id=int(info[20]) if info[20] != "" else None
     * base_form_id=int(info[21]) if info[21] != "" else None
   
3. DATA FLOW:
   - Regional evolution data is scraped from Bulbapedia and stored in regional_evolutions.csv
   - This script reads the regional data and updates the main pokemon_evolution.csv file
   - When the build process runs (make docker-build-db), it loads all data from CSV files
   - The regional evolution data becomes part of the database and persists through rebuilds
   
4. REGIONAL EVOLUTION EXAMPLES:
   - Galarian Meowth → Perrserker (region_id=8, base_form_id=52)
   - Hisuian Scyther → Kleavor (region_id=9, base_form_id=123)
   - Alolan Rattata → Raticate (region_id=7, base_form_id=19)
   
5. API INTEGRATION:
   - The PokemonEvolution model includes the new fields as ForeignKeys
   - Serializers automatically expose regional data through existing API endpoints
   - GraphQL metadata files have been updated to include the new fields
   
6. PERSISTENCE:
   - Unlike database-only updates, this approach ensures data survives Docker rebuilds
   - The CSV file is the source of truth for all evolution data
   - Regional evolution data is now permanently part of the build system

This approach follows the PokeAPI architecture where all data comes from CSV files
and is loaded through the build process, ensuring consistency and persistence.
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


def ensure_csv_columns(csv_file):
    """Ensure the CSV file has the required columns"""
    with open(csv_file, "r") as f:
        reader = csv.reader(f)
        header = next(reader)

    # Check if we need to add the new columns
    if "region_id" not in header or "base_form_id" not in header:
        print("Adding missing columns to CSV...")

        # Read all data
        with open(csv_file, "r") as f:
            reader = csv.reader(f)
            rows = list(reader)

        # Update header
        if "region_id" not in header:
            header.append("region_id")
        if "base_form_id" not in header:
            header.append("base_form_id")

        # Add empty columns to all data rows
        for i in range(1, len(rows)):
            while len(rows[i]) < len(header):
                rows[i].append("")

        # Write back to file
        with open(csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(rows)

        print("✅ Added missing columns to CSV")
        return True  # Indicate that columns were added
    else:
        print("✅ CSV already has required columns")
        return False  # Indicate that columns already existed


def get_region_id(region_name):
    """Get region ID by name from CSV"""
    if not region_name:
        return ""
    try:
        with open("data/v2/csv/regions.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["identifier"] == region_name:
                    return row["id"]
        print(f"⚠️  Region '{region_name}' not found in regions.csv")
        return ""
    except FileNotFoundError:
        print("⚠️  regions.csv not found")
        return ""


def get_species_id(species_name):
    """Get species ID by name from CSV"""
    if not species_name:
        return ""
    try:
        with open("data/v2/csv/pokemon_species.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["identifier"] == species_name:
                    return row["id"]
        print(f"⚠️  Species '{species_name}' not found in pokemon_species.csv")
        return ""
    except FileNotFoundError:
        print("⚠️  pokemon_species.csv not found")
        return ""


def get_species_name_by_id(species_id):
    """Get species name by ID from CSV"""
    if not species_id:
        return ""
    try:
        with open("data/v2/csv/pokemon_species.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["id"] == species_id:
                    return row["identifier"]
        return ""
    except FileNotFoundError:
        return ""


def get_trigger_name_by_id(trigger_id):
    """Get trigger name by ID from CSV"""
    if not trigger_id:
        return ""
    try:
        with open("data/v2/csv/evolution_triggers.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["id"] == trigger_id:
                    return row["identifier"]
        return ""
    except FileNotFoundError:
        return ""


def get_evolution_id(evolved_species_name, trigger_name):
    """Get evolution ID by evolved species and trigger"""
    try:
        evolved_species = PokemonSpecies.objects.get(name=evolved_species_name)
        trigger = EvolutionTrigger.objects.get(name=trigger_name)
        evolution = PokemonEvolution.objects.get(
            evolved_species=evolved_species, evolution_trigger=trigger
        )
        return evolution.id
    except (
        PokemonSpecies.DoesNotExist,
        EvolutionTrigger.DoesNotExist,
        PokemonEvolution.DoesNotExist,
    ):
        print(
            f"⚠️  Evolution '{evolved_species_name}' with trigger '{trigger_name}' not found"
        )
        return None


def update_evolution_csv(regional_csv_file, evolution_csv_file):
    """Update the evolution CSV with regional data"""
    print(
        f"Updating {evolution_csv_file} with regional data from {regional_csv_file}..."
    )

    # Read regional data
    regional_data = {}
    with open(regional_csv_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = f"{row['evolves_to']}_{row['method']}"
            regional_data[key] = {
                "region": row["region"],
                "base_form_id": row["base_form_id"],
            }

    # Read evolution CSV
    with open(evolution_csv_file, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    header = rows[0]

    # Check if columns exist
    if "region_id" not in header:
        print("❌ region_id column not found in CSV")
        return
    if "base_form_id" not in header:
        print("❌ base_form_id column not found in CSV")
        return

    region_col_idx = header.index("region_id")
    base_form_col_idx = header.index("base_form_id")

    updated_count = 0

    # Update each row
    for i in range(1, len(rows)):
        row = rows[i]

        # Ensure row has enough columns
        if len(row) < len(header):
            # Add empty columns to match header length
            missing_columns = len(header) - len(row)
            for _ in range(missing_columns):
                row.append("")
            updated_count += 1
            if i <= 3:  # Show first few rows
                print(f"Row {i}: {len(row)} columns -> {len(header)} columns")

        # Get evolution details from CSV
        evolved_species_id = row[1]  # evolved_species_id column
        trigger_id = row[2]  # evolution_trigger_id column

        # Look up species and trigger names from CSV files
        evolved_species_name = get_species_name_by_id(evolved_species_id)
        trigger_name = get_trigger_name_by_id(trigger_id)

        if evolved_species_name and trigger_name:
            # Create key to match regional data
            key = f"{evolved_species_name}_{trigger_name}"

            if key in regional_data:
                # Update with regional data
                region_data = regional_data[key]
                region_id = get_region_id(region_data["region"])
                base_form_id = get_species_id(region_data["base_form_id"])

                row[region_col_idx] = region_id
                row[base_form_col_idx] = base_form_id
                print(f"✅ Updated {evolved_species_name} evolution with regional data")
            else:
                # Set empty values for the new columns
                row[region_col_idx] = ""
                row[base_form_col_idx] = ""

    # Write updated CSV
    with open(evolution_csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f"✅ Updated {updated_count} rows with correct column count")
    print(f"✅ CSV file updated: {evolution_csv_file}")


def main():
    """Main function"""
    regional_csv_file = "regional_evolutions.csv"
    evolution_csv_file = "data/v2/csv/pokemon_evolution.csv"

    if not os.path.exists(regional_csv_file):
        print(f"❌ Regional CSV file '{regional_csv_file}' not found")
        return

    if not os.path.exists(evolution_csv_file):
        print(f"❌ Evolution CSV file '{evolution_csv_file}' not found")
        return

    # Ensure CSV has required columns
    columns_added = ensure_csv_columns(evolution_csv_file)

    # Update evolution CSV with regional data
    update_evolution_csv(regional_csv_file, evolution_csv_file)

    print("\n🎉 Import completed successfully!")
    print(
        "The pokemon_evolution.csv file has been updated with regional evolution data."
    )
    print("You can now rebuild the database to see the changes.")


if __name__ == "__main__":
    main()
