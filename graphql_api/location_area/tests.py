from pokemon_v2.tests import APIData as A
from ..graphql_test import GraphQLTest


class LocationAreaTests(GraphQLTest):
    def setUp(self):

        location = A.setup_location_data(name="lctn for base lctn area")
        self.location_areas = [
            A.setup_location_area_data(location, name=f"base lctn area {n}")
            for n in range(4)
        ]

        for la in self.location_areas:
            A.setup_location_area_name_data(la, name=f"{la.name} name")

            encounter_method = A.setup_encounter_method_data(
                name=f"encntr mthd for {la.name}"
            )
            A.setup_location_area_encounter_rate_data(la, encounter_method, rate=20)

            for x in range(3):
                pokemon_species = A.setup_pokemon_species_data(name=f"spcs for pkmn{x}")
                pokemon = A.setup_pokemon_data(
                    name=f"pkmn{x} for encntr{x}", pokemon_species=pokemon_species
                )
                encounter_slot = A.setup_encounter_slot_data(
                    encounter_method, slot=1, rarity=30
                )
                A.setup_encounter_data(
                    pokemon=pokemon,
                    location_area=la,
                    encounter_slot=encounter_slot,
                    min_level=x * 8,
                    max_level=x * 8 + 7,
                )

    def test_location_areas(self):
        executed = self.execute_query(
            """
            query {
                locationAreas(first: 10) {
                    edges {
                        node {
                            gameIndex
                            location {name}
                            name
                            names {
                                text
                                language {name}
                            }
                        }
                    }
                }
            }
            """
        )

        # Remember to accurately test the maxChance value of
        # pokemonEncounter.versionDetails. The actual value is the sum of all rarities
        # in that version.

        expected = {
            "data": {
                "locationAreas": {
                    "edges": [
                        {
                            "node": {
                                "gameIndex": la.game_index,
                                "location": {"name": la.location.name},
                                "name": la.name,
                                "names": [
                                    {
                                        "text": n.name,
                                        "language": {"name": n.language.name},
                                    }
                                    for n in la.locationareaname.all()
                                ],
                            }
                        }
                        for la in self.location_areas
                    ]
                }
            }
        }
        self.assertEqual(executed, expected)

    def test_location_area(self):
        la = self.location_areas[1]
        executed = self.execute_query(
            """
            query {
                locationArea(name: "%s") {
                    name
                    names {text}
                }
            }
            """
            % la.name
        )
        expected = {
            "data": {
                "locationArea": {
                    "name": la.name,
                    "names": [{"text": n.name} for n in la.locationareaname.all()],
                }
            }
        }
        self.assertEqual(executed, expected)
