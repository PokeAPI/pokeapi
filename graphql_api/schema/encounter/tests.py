from pokemon_v2.tests import APIData as A
from graphql_api.graphql_test import GraphQLTest


class EncounterTests(GraphQLTest):
    def setUp(self):
        self.encounters = []
        pokemons = []
        for n in range(3):
            species = A.setup_pokemon_species_data(name=f"pkmn species {n}")
            pokemons.append(
                A.setup_pokemon_data(name=f"pokemon {n}", pokemon_species=species)
            )

        for i in range(10):
            location = A.setup_location_data(name=f"lctn {i}")
            location_area = A.setup_location_area_data(location, name=f"lctn area {i}")

            encounter_method = A.setup_encounter_method_data()
            encounter_slot = A.setup_encounter_slot_data(
                encounter_method, slot=i, rarity=i * 8
            )
            encounter = A.setup_encounter_data(
                pokemon=pokemons[i % 3],
                location_area=location_area,
                encounter_slot=encounter_slot,
                min_level=i * 9,
                max_level=i * 9 + 11,
            )
            self.encounters.append(encounter)

            # Multiple conditions per encounter
            for c in range(3):
                condition = A.setup_encounter_condition_data(name=f"encntr cndtn {c}")
                condition_value = A.setup_encounter_condition_value_data(
                    condition, name=f"encntr cndtn val {c}"
                )
                A.setup_encounter_condition_value_map_data(encounter, condition_value)

    def test_encounters(self):
        executed = self.execute_query(
            """
            query {
                encounters(first: 50) {
                    edges {
                        node {
                            chance
                            conditionValues {idName}
                            locationArea {idName}
                            maxLevel
                            method {idName}
                            minLevel
                            idName
                            pokemon {idName}
                            version {idName}
                        }
                    }
                }
            }
            """
        )
        expected = {
            "data": {
                "encounters": {
                    "edges": [
                        {
                            "node": {
                                "chance": encounter.encounter_slot.rarity,
                                "conditionValues": [
                                    {"idName": ecvm.encounter_condition_value.name}
                                    for ecvm in encounter.encounterconditionvaluemap_set.all()
                                ],
                                "locationArea": {"idName": encounter.location_area.name},
                                "maxLevel": encounter.max_level,
                                "method": {
                                    "idName": encounter.encounter_slot.encounter_method.name
                                },
                                "minLevel": encounter.min_level,
                                "idName": str(encounter.pk),
                                "pokemon": {"idName": encounter.pokemon.name},
                                "version": {"idName": encounter.version.name},
                            }
                        }
                        for encounter in self.encounters
                    ]
                }
            }
        }
        self.assertEqual(executed, expected)

    def test_encounter(self):
        encounter = self.encounters[1]
        executed = self.execute_query(
            """
            query {
                encounter(idName: "%s") {
                    idName
                }
            }
            """
            % encounter.pk
        )
        expected = {"data": {"encounter": {"idName": str(encounter.pk)}}}
        self.assertEqual(executed, expected)
