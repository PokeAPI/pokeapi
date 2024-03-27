from django.test import TestCase
from pokemon_v2.models import *


class AbilityTestCase(TestCase):
    def setUp(self):
        Ability.objects.create(name="Smell", generation_id=3, is_main_series=True)

    def fields_are_valid(self):
        smell = Ability.objects.get(name="Smell")
        self.assertEqual(smell.generation_id, 3)


class MachineTestCase(TestCase):
    def setUp(self):
        MachineVersionLocations.objects.create(machine_id=1,version_group_id=1, location_id=1)
    def fields_are_valid(self):
        machine = Machine.objects.get(machine_id=1)
        self.assertEqual(machine.version_group_id, 1)