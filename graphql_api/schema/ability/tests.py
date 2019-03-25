from pokemon_v2.tests import APIData as A
from graphql_api.graphql_test import GraphQLTest


class StatTests(GraphQLTest):
    def setUp(self):
        self.abilities = [A.setup_ability_data(name=f"ability {n}") for n in range(10)]

        for a in self.abilities:
            A.setup_ability_name_data(a, name=f"{a.name} name")
            A.setup_ability_effect_text_data(a, effect=f"{a.name} effect")
            A.setup_ability_flavor_text_data(a, flavor_text=f"{a.name} flavor text")

            for x in range(3):
                ability_change = A.setup_ability_change_data(a)
                A.setup_ability_change_effect_text_data(
                    ability_change, effect=f"{a.name} {x} change effect"
                )
                pokemon = A.setup_pokemon_data(name="pkmn for ablty")
                A.setup_pokemon_ability_data(ability=a, pokemon=pokemon)

    def test_abilities(self):
        executed = self.execute_query(
            """
            query {
                abilities(first: 50) {
                    edges {
                        node {
                            isMainSeries
                            effectEntries {text}
                            generation {idName}
                            effectHistory {
                                effectEntries {text}
                                versionGroup {idName}
                            }
                            flavorTextEntries {
                                text
                                versionGroup {idName}
                            }
                            idName
                            names {text}
                            pokemons(first: 10) {
                                edges {
                                    isHidden
                                    order
                                    node {idName}
                                }
                            }
                        }
                    }
                }
            }
            """
        )
        expected = {
            "data": {
                "abilities": {
                    "edges": [
                        {
                            "node": {
                                "isMainSeries": a.is_main_series,
                                "effectEntries": [
                                    {"text": e.effect}
                                    for e in a.abilityeffecttext.all()
                                ],
                                "generation": {"idName": a.generation.name},
                                "effectHistory": [
                                    {
                                        "effectEntries": [
                                            {"text": e.effect}
                                            for e in ac.abilitychangeeffecttext.all()
                                        ],
                                        "versionGroup": {"idName": ac.version_group.name},
                                    }
                                    for ac in a.abilitychange.all()
                                ],
                                "flavorTextEntries": [
                                    {
                                        "text": f.flavor_text,
                                        "versionGroup": {"idName": f.version_group.name},
                                    }
                                    for f in a.abilityflavortext.all()
                                ],
                                "idName": a.name,
                                "names": [
                                    {"text": n.name} for n in a.abilityname.all()
                                ],
                                "pokemons": {
                                    "edges": [
                                        {
                                            "isHidden": pa.is_hidden,
                                            "order": pa.slot,
                                            "node": {"idName": pa.pokemon.name},
                                        }
                                        for pa in a.pokemonability.all()
                                    ]
                                },
                            }
                        }
                        for a in self.abilities
                    ]
                }
            }
        }
        self.assertEqual(executed, expected)

    def test_ability(self):
        ability = self.abilities[1]
        executed = self.execute_query(
            """
            query {
                ability(idName: "%s") {
                    idName
                    names {
                        text
                        language {idName}
                    }
                }
            }
            """
            % ability.name
        )
        expected = {
            "data": {
                "ability": {
                    "idName": ability.name,
                    "names": [
                        {"text": n.name, "language": {"idName": n.language.name}}
                        for n in ability.abilityname.all()
                    ],
                }
            }
        }
        self.assertEqual(executed, expected)