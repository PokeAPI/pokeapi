from pokemon_v2.tests import APIData as A
from graphql_api.graphql_test import GraphQLTest
from graphql_api.utils import group


class LocationAreaTests(GraphQLTest):
    def setUp(self):

        location = A.setup_location_data(name="lctn for base lctn area")
        self.location_areas = [
            A.setup_location_area_data(location, name=f"base lctn area {n}")
            for n in range(4)
        ]

        for la in self.location_areas:
            A.setup_location_area_name_data(la, name=f"{la.name} name")

            # Encounter Rates
            for i in range(4):
                encounter_method = A.setup_encounter_method_data(
                    name=f"encntr mthd B{i} for {la.name}"
                )
                A.setup_location_area_encounter_rate_data(
                    la, encounter_method, rate=20 + i
                )

            # Encounters
            for x in range(1, 4):
                pokemon_species = A.setup_pokemon_species_data(name=f"spcs for pkmn{x}")
                pokemon = A.setup_pokemon_data(
                    name=f"pkmn{x} for encntr{x}", pokemon_species=pokemon_species
                )

                # Some location areas have multiple encounters with each Pokémon
                for y in range(1, x):
                    encounter_method = A.setup_encounter_method_data(
                        name=f"encntr mthd {x}.{y} for {la.name}"
                    )
                    encounter_slot = A.setup_encounter_slot_data(
                        encounter_method, slot=y + 1, rarity=30 + y + x
                    )
                    A.setup_encounter_data(
                        pokemon=pokemon,
                        location_area=la,
                        encounter_slot=encounter_slot,
                        min_level=y * 8,
                        max_level=y * 8 + 7,
                    )

    def test_location_areas(self):
        executed = self.execute_query(
            """
            query {
                locationAreas(first: 10) {
                    edges {
                        node {
                            encounterMethodRates {
                                encounterMethod {name}
                                versionDetails {
                                    rate
                                    version {name}
                                }
                            }
                            gameIndex
                            location {name}
                            name
                            names {
                                text
                                language {name}
                            }
                            pokemonEncounters(first: 10) {
                                edges {
                                    node {
                                        pokemon {name}
                                        versionDetails {
                                            encounters {name}
                                            maxChance
                                            version {name}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
            """
        )

        def get_encounter_rates(all_encounter_rates):
            results = []
            grouped = group(all_encounter_rates, "encounter_method")
            for em, encounter_rates in grouped.items():
                version_details = []
                for er in encounter_rates:
                    version_details.append(
                        {"rate": er.rate, "version": {"name": er.version.name}}
                    )

                results.append(
                    {
                        "encounterMethod": {"name": em.name},
                        "versionDetails": version_details,
                    }
                )
            return results

        def get_pokemon_encounters(all_encounters):
            pokemon_encounters = []
            for pokemon, p_encntrs in group(all_encounters, "pokemon").items():
                version_details = []
                for version, v_encounters in group(p_encntrs, "version").items():
                    max_chance = 0
                    for e in v_encounters:
                        max_chance += e.encounter_slot.rarity
                    version_details.append(
                        {
                            "encounters": [{"name": str(e.pk)} for e in v_encounters],
                            "maxChance": max_chance,
                            "version": {"name": version.name},
                        }
                    )
                pokemon_encounters.append(
                    {
                        "node": {
                            "pokemon": {"name": pokemon.name},
                            "versionDetails": version_details,
                        }
                    }
                )

            return pokemon_encounters

        expected = {
            "data": {
                "locationAreas": {
                    "edges": [
                        {
                            "node": {
                                "encounterMethodRates": get_encounter_rates(
                                    la.locationareaencounterrate.all()
                                ),
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
                                "pokemonEncounters": {
                                    "edges": get_pokemon_encounters(la.encounter.all())
                                },
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
