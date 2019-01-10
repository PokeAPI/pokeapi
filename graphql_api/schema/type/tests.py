from pokemon_v2.tests import APIData as A
from graphql_api.graphql_test import GraphQLTest


class TypeTests(GraphQLTest):
    def setUp(self):
        self.types = [A.setup_type_data(name=f"type {n}") for n in range(15)]

        for i, t in enumerate(self.types):
            A.setup_type_name_data(t, name=f"{t.name} name")

            for x in range(3):
                pokemon = A.setup_pokemon_data(name=f"pkmn {i}.{x} for {t.name}")
                A.setup_pokemon_type_data(pokemon=pokemon, type=t)
                A.setup_type_game_index_data(t, game_index=x * i)
                A.setup_move_data(type=t, name=f"move {x} for {t.name}")

            # <-
            for next_i, damage_factor in zip([1, 3, 4, 7, 8], [0, 50, 50, 200, 200]):
                damage_type = self.types[(i + next_i) % len(self.types)]
                A.setup_type_efficacy_data(damage_type, t, damage_factor)

            # ->
            for next_i, damage_factor in zip([2, 5, 9, 12, 15], [0, 0, 50, 200, 200]):
                target_type = self.types[(i + next_i) % len(self.types)]
                A.setup_type_efficacy_data(t, target_type, damage_factor)

    def test_types(self):
        executed = self.execute_query(
            """
            query {
                types(first: 100) {
                    edges {
                        node {
                            gameIndices {
                                gameIndex
                                generation {idName}
                            }
                            generation {idName}
                            idName
                            names {
                                text
                                language {idName}
                            }
                            pokemon(first: 100) {
                                edges {
                                    order
                                    node {
                                        idName
                                    }
                                }
                            }
                            noDamageTo {idName}
                            halfDamageTo {idName}
                            doubleDamageTo {idName}
                            noDamageFrom {idName}
                            halfDamageFrom {idName}
                            doubleDamageFrom {idName}
                        }
                    }
                }
            }
            """
        )
        expected = {
            "data": {
                "types": {
                    "edges": [
                        {
                            "node": {
                                "gameIndices": [
                                    {
                                        "gameIndex": tgi.game_index,
                                        "generation": {"idName": tgi.generation.name},
                                    }
                                    for tgi in t.typegameindex.all()
                                ],
                                "generation": {"idName": t.generation.name},
                                "idName": t.name,
                                "names": [
                                    {
                                        "text": n.name,
                                        "language": {"idName": n.language.name},
                                    }
                                    for n in t.typename.all()
                                ],
                                "pokemon": {
                                    "edges": [
                                        {
                                            "order": pt.slot,
                                            "node": {"idName": pt.pokemon.name},
                                        }
                                        for pt in t.pokemontype.all()
                                    ]
                                },
                                "noDamageTo": [
                                    {"idName": te.target_type.name}
                                    for te in t.damage_type.all()
                                    if te.damage_type == t
                                    if te.damage_factor == 0
                                ],
                                "halfDamageTo": [
                                    {"idName": te.target_type.name}
                                    for te in t.damage_type.all()
                                    if te.damage_type == t
                                    if te.damage_factor == 50
                                ],
                                "doubleDamageTo": [
                                    {"idName": te.target_type.name}
                                    for te in t.damage_type.all()
                                    if te.damage_type == t
                                    if te.damage_factor == 200
                                ],
                                "noDamageFrom": [
                                    {"idName": te.damage_type.name}
                                    for te in t.target_type.all()
                                    if te.target_type == t
                                    if te.damage_factor == 0
                                ],
                                "halfDamageFrom": [
                                    {"idName": te.damage_type.name}
                                    for te in t.target_type.all()
                                    if te.target_type == t
                                    if te.damage_factor == 50
                                ],
                                "doubleDamageFrom": [
                                    {"idName": te.damage_type.name}
                                    for te in t.target_type.all()
                                    if te.target_type == t
                                    if te.damage_factor == 200
                                ],
                            }
                        }
                        for t in self.types
                    ]
                }
            }
        }
        self.assertEqual(executed, expected)

    def test_type(self):
        t = self.types[1]
        executed = self.execute_query(
            """
            query {
                type(idName: "%s") {
                    idName
                    names {
                        text
                        language {idName}
                    }
                }
            }
            """
            % t.name
        )
        expected = {
            "data": {
                "type": {
                    "idName": t.name,
                    "names": [
                        {"text": n.name, "language": {"idName": n.language.name}}
                        for n in t.typename.all()
                    ],
                }
            }
        }
        self.assertEqual(executed, expected)
