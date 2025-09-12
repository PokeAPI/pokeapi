#!/usr/bin/env python3
"""
Export Pokemon summaries from the local database to CSV format.
This creates the data files that should be committed to git.
"""

import os
import sys
import django
import csv

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.local')
django.setup()

from pokemon_v2.models import PokemonSummary


def export_summaries_to_csv():
    """Export Pokemon summaries to CSV format."""
    
    # Get all summaries
    summaries = PokemonSummary.objects.select_related('pokemon', 'language').all()
    
    print(f"Exporting {summaries.count()} Pokemon summaries to CSV...")
    
    # Create the CSV file
    csv_file_path = 'data/v2/csv/pokemon_summaries.csv'
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
    
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['pokemon_id', 'pokemon_name', 'language_id', 'language_name', 'summary']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header
        writer.writeheader()
        
        # Write data
        for summary in summaries:
            writer.writerow({
                'pokemon_id': summary.pokemon.id,
                'pokemon_name': summary.pokemon.name,
                'language_id': summary.language.id,
                'language_name': summary.language.name,
                'summary': summary.summary
            })
    
    print(f"✅ Exported {summaries.count()} summaries to {csv_file_path}")
    return csv_file_path


if __name__ == '__main__':
    csv_file = export_summaries_to_csv()
    print(f"\n📁 CSV file created: {csv_file}")
    print("This file should now be committed to git!")
