from django.test import TestCase
from pokemon_v2.models import *


class AbilityTestCase(TestCase):
    def setUp(self):
        Ability.objects.create(name="Smell", generation_id=3, is_main_series=True)

    def fields_are_valid(self):
        smell = Ability.objects.get(name="Smell")
        self.assertEqual(smell.generation_id, 3)
