#!/usr/bin/env python3
"""
Simple Regional Pokemon Extractor

This script:
1. Reads the existing CSV files in data/v2/csv/
2. Finds Pokemon with regional forms (alola, galar, hisui, paldea)
3. Outputs a simple CSV with pokemon_id, name, region
"""

import csv
import os
from typing import List, Dict

class SimpleRegionalExtractor:
    """Simple regional Pokemon extractor from CSV files"""
    
    def __init__(self):
        # Known regional suffixes
        self.regional_suffixes = ['-alola', '-galar', '-hisui', '-paldea']
        
        # Load regions mapping from CSV
        self.regions = self.load_regions()
        
        # Load base form mappings from CSV
        self.base_forms = self.load_base_forms()
        
        # Load evolution chain mappings from CSV
        self.evolution_chains = self.load_evolution_chains()
        
        # Load location to region mappings from CSV
        self.location_regions = self.load_location_regions()
    
    def load_regions(self) -> Dict[str, str]:
        """Load region names and IDs from regions.csv"""
        regions = {}
        regions_file = "data/v2/csv/regions.csv"
        
        if os.path.exists(regions_file):
            with open(regions_file, 'r', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    region_id = row.get('id', '')
                    region_name = row.get('identifier', '')
                    regions[region_name] = region_id
        
        return regions
    
    def load_base_forms(self) -> Dict[str, str]:
        """Load base form names and IDs from pokemon.csv"""
        base_forms = {}
        pokemon_file = "data/v2/csv/pokemon.csv"
        
        if os.path.exists(pokemon_file):
            with open(pokemon_file, 'r', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    pokemon_id = row.get('id', '')
                    pokemon_name = row.get('identifier', '').lower()
                    
                    # Only include base forms (no regional suffixes)
                    if not any(suffix in pokemon_name for suffix in self.regional_suffixes):
                        base_forms[pokemon_name] = pokemon_id
        
        return base_forms
    
    def load_evolution_chains(self) -> Dict[str, str]:
        """Load evolution chain IDs from pokemon_species.csv"""
        evolution_chains = {}
        species_file = "data/v2/csv/pokemon_species.csv"
        
        if os.path.exists(species_file):
            with open(species_file, 'r', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    species_id = row.get('id', '')
                    evolution_chain_id = row.get('evolution_chain_id', '')
                    if evolution_chain_id:
                        evolution_chains[species_id] = evolution_chain_id
        
        return evolution_chains
    
    def load_location_regions(self) -> Dict[str, str]:
        """Load location to region mapping from locations.csv"""
        location_regions = {}
        locations_file = "data/v2/csv/locations.csv"
        
        if os.path.exists(locations_file):
            with open(locations_file, 'r', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    location_id = row.get('id', '')
                    region_id = row.get('region_id', '')
                    if region_id:
                        location_regions[location_id] = region_id
        
        return location_regions
    
    def get_region_id(self, region_name: str) -> str:
        """Get region ID from region name"""
        return self.regions.get(region_name, '')
    
    def get_base_form_info(self, pokemon_name: str) -> tuple:
        """Get base form ID and name from Pokemon name"""
        # Remove regional suffix to get base form name
        base_name = pokemon_name.lower()
        for suffix in self.regional_suffixes:
            if base_name.endswith(suffix):
                base_name = base_name[:-len(suffix)]
                break
        
        base_form_id = self.base_forms.get(base_name, '')
        return base_form_id, base_name
    
    def get_evolution_chain_id(self, species_id: str) -> str:
        """Get evolution chain ID from species ID"""
        return self.evolution_chains.get(species_id, '')
    
    def get_evolution_location_data(self, pokemon_id: str) -> tuple:
        """Get location_id and region_id from evolution location for a Pokemon"""
        evolution_file = "data/v2/csv/pokemon_evolution.csv"
        
        if os.path.exists(evolution_file):
            with open(evolution_file, 'r', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    evolved_species_id = row.get('evolved_species_id', '')
                    location_id = row.get('location_id', '')
                    
                    if evolved_species_id == pokemon_id:
                        if location_id:
                            # Map location_id to region_id
                            region_id = self.location_regions.get(location_id, '')
                            return location_id, region_id if region_id else 'unknown location'
                        else:
                            # No location_id means region not required
                            return '', 'region not required'
        
        return '', 'no evolution data'
    
    def extract_regional_pokemon(self) -> List[Dict]:
        """Extract regional Pokemon from existing CSV files"""
        
        regional_pokemon = []
        
        # Read pokemon.csv to get all Pokemon with their IDs
        pokemon_file = "data/v2/csv/pokemon.csv"
        if not os.path.exists(pokemon_file):
            print(f"❌ {pokemon_file} not found")
            return []
        
        print(f"📖 Reading {pokemon_file}...")
        
        with open(pokemon_file, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                pokemon_name = row.get('identifier', '').lower()
                pokemon_id = row.get('id', '')
                species_id = row.get('species_id', '')
                
                # Check if this is a regional form
                if any(region in pokemon_name for region in self.regional_suffixes):
                    # Determine region
                    if '-alola' in pokemon_name:
                        region = 'alola'
                    elif '-galar' in pokemon_name:
                        region = 'galar'
                    elif '-hisui' in pokemon_name:
                        region = 'hisui'
                    elif '-paldea' in pokemon_name:
                        region = 'paldea'
                    else:
                        region = 'unknown'
                    
                    # Get base form ID and name
                    base_form_id, base_form_name = self.get_base_form_info(pokemon_name)
                    
                    # Get evolution chain ID
                    evolution_chain_id = self.get_evolution_chain_id(species_id)
                    
                    # Get location-based data
                    location_id, location_region_id = self.get_evolution_location_data(species_id)
                    
                    # Only include if we have a base_form_id
                    if base_form_id:
                        regional_pokemon.append({
                            'evolution_chain_id': evolution_chain_id,
                            'name': row.get('identifier', ''),
                            'region': region,
                            'region_id': self.get_region_id(region),
                            'base_form_id': base_form_id,
                            'base_form_name': base_form_name,
                            'location_id': location_id,
                            'location_region_id': location_region_id
                        })
                        
                        print(f"   ✅ Found: {row.get('identifier', '')} (Chain: {evolution_chain_id}, Region: {region}, Base: {base_form_name} (ID: {base_form_id}), Location ID: {location_id}, Location Region: {location_region_id})")
                    else:
                        print(f"   ⚠️  Skipped: {row.get('identifier', '')} (ID: {pokemon_id}, Region: {region}) - No base form ID")
        
        return regional_pokemon
    
    def save_regional_csv(self, regional_pokemon: List[Dict]):
        """Save regional Pokemon to CSV file"""
        
        output_file = "regional_pokemon_list.csv"
        
        with open(output_file, 'w', newline='') as f:
            if regional_pokemon:
                fieldnames = ['evolution_chain_id', 'name', 'region', 'region_id', 'base_form_id', 'base_form_name', 'location_id', 'location_region_id']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(regional_pokemon)
        
        print(f"💾 Saved {len(regional_pokemon)} regional Pokemon to {output_file}")


def main():
    """Main function"""
    print("🎯 Simple Regional Pokemon Extractor")
    print("=" * 50)
    print("✅ Reads existing CSV files")
    print("✅ Extracts regional Pokemon only")
    print("✅ Outputs simple CSV with ID, name, region")
    print()
    
    extractor = SimpleRegionalExtractor()
    
    # Extract regional Pokemon
    regional_pokemon = extractor.extract_regional_pokemon()
    
    if not regional_pokemon:
        print("❌ No regional Pokemon found")
        return
    
    # Save to CSV
    extractor.save_regional_csv(regional_pokemon)
    
    print(f"\n🎉 Extraction completed!")
    print(f"📊 Found {len(regional_pokemon)} regional Pokemon")
    
    # Show summary by region
    from collections import Counter
    regions = Counter(pokemon['region'] for pokemon in regional_pokemon)
    print(f"\n📊 Summary by region:")
    for region, count in regions.items():
        print(f"   {region}: {count} Pokemon")


if __name__ == "__main__":
    main()