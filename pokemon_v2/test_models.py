from django.test import TestCase
from pokemon_v2.models import *


class AbilityTestCase(TestCase):
    def setUp(self):
        Ability.objects.create(name="Smell", generation_id=3, is_main_series=True)

    def fields_are_valid(self):
        smell = Ability.objects.get(name="Smell")
        self.assertEqual(smell.generation_id, 3)


class PokemonSummaryTestCase(TestCase):
    def setUp(self):
        # Create test data
        self.language = Language.objects.create(
            name="en",
            iso639="en",
            iso3166="us",
            official=True
        )
        self.pokemon_species = PokemonSpecies.objects.create(
            name="pikachu",
            generation_id=1,
            pokemon_color_id=1,
            pokemon_shape_id=1,
            growth_rate_id=1
        )
        self.pokemon = Pokemon.objects.create(
            name="pikachu",
            pokemon_species=self.pokemon_species,
            height=40,
            weight=60,
            base_experience=112,
            is_default=True
        )

    def test_pokemon_summary_creation(self):
        """Test creating a Pokemon summary."""
        summary_text = "Pikachu is an Electric-type Pokémon known for its yellow fur and red cheeks."
        
        pokemon_summary = PokemonSummary.objects.create(
            pokemon=self.pokemon,
            language=self.language,
            summary=summary_text
        )
        
        self.assertEqual(pokemon_summary.pokemon, self.pokemon)
        self.assertEqual(pokemon_summary.language, self.language)
        self.assertEqual(pokemon_summary.summary, summary_text)

    def test_pokemon_summary_unique_constraint(self):
        """Test that Pokemon summaries are unique per Pokemon and language."""
        summary_text = "Pikachu is an Electric-type Pokémon."
        
        # Create first summary
        PokemonSummary.objects.create(
            pokemon=self.pokemon,
            language=self.language,
            summary=summary_text
        )
        
        # Try to create duplicate - should raise IntegrityError
        with self.assertRaises(Exception):  # IntegrityError
            PokemonSummary.objects.create(
                pokemon=self.pokemon,
                language=self.language,
                summary="Different summary"
            )
