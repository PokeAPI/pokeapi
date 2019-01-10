from pokemon_v2.tests import APIData as A
from graphql_api.graphql_test import GraphQLTest


class PokemonColorTests(GraphQLTest):
    def setUp(self):
        self.pokemon_colors = [
            A.setup_pokemon_color_data(name=f"pkmn color {n}") for n in range(4)
        ]

        for pc in self.pokemon_colors:
            A.setup_pokemon_color_name_data(pc, name=f"{pc.name} name")

            for x in range(3):
                A.setup_pokemon_species_data(
                    name=f"pokemon species {x} for {pc.name}",
                    pokemon_color=pc,
                )

    def test_pokemon_colors(self):
        executed = self.execute_query(
            """
            query {
                pokemonColors {
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
                "pokemonColors": [
                    {
                        "idName": pc.name,
                        "names": [
                            {"text": n.name}
                            for n in pc.pokemoncolorname.all()
                        ],
                        "pokemonSpeciess": {
                            "edges": [
                                {"node": {"idName": ps.name}}
                                for ps in pc.pokemonspecies.all()
                            ]
                        },
                    }
                    for pc in self.pokemon_colors
                ]
            }
        }
        self.assertEqual(executed, expected)

    def test_pokemon_color(self):
        pc = self.pokemon_colors[1]
        executed = self.execute_query(
            """
            query {
                pokemonColor(idName: "%s") {
                    idName
                }
            }
            """
            % pc.name
        )
        expected = {"data": {"pokemonColor": {"idName": pc.name}}}
        self.assertEqual(executed, expected)
