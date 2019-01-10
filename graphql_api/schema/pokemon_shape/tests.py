from pokemon_v2.tests import APIData as A
from graphql_api.graphql_test import GraphQLTest


class PokemonShapeTests(GraphQLTest):
    def setUp(self):
        self.pokemon_shapes = [
            A.setup_pokemon_shape_data(name=f"pkmn shape {n}") for n in range(4)
        ]

        for shape in self.pokemon_shapes:
            A.setup_pokemon_shape_name_data(shape, name=f"{shape.name} name")

            for x in range(3):
                A.setup_pokemon_species_data(
                    name=f"pokemon species {x} for {shape.name}", pokemon_shape=shape
                )

    def test_pokemon_shapes(self):
        executed = self.execute_query(
            """
            query {
                pokemonShapes {
                    idName
                    names {text}
                    pokemonSpeciess(first: 10) {
                        edges {
                            node {
                                idName
                            }
                        }
                    }
                }
            }
            """
        )
        expected = {
            "data": {
                "pokemonShapes": [
                    {
                        "idName": shape.name,
                        "names": [
                            {"text": n.name} for n in shape.pokemonshapename.all()
                        ],
                        "pokemonSpeciess": {
                            "edges": [
                                {"node": {"idName": ps.name}}
                                for ps in shape.pokemonspecies.all()
                            ]
                        },
                    }
                    for shape in self.pokemon_shapes
                ]
            }
        }
        self.assertEqual(executed, expected)

    def test_pokemon_shape(self):
        shape = self.pokemon_shapes[1]
        executed = self.execute_query(
            """
            query {
                pokemonShape(idName: "%s") {
                    idName
                }
            }
            """
            % shape.name
        )
        expected = {"data": {"pokemonShape": {"idName": shape.name}}}
        self.assertEqual(executed, expected)
