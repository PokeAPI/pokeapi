from pokemon_v2.tests import APIData as A
from graphql_api.graphql_test import GraphQLTest


class PokemonHabitatTests(GraphQLTest):
    def setUp(self):
        self.pokemon_habitats = [
            A.setup_pokemon_habitat_data(name=f"pkmn habitat {n}") for n in range(4)
        ]

        for ph in self.pokemon_habitats:
            A.setup_pokemon_habitat_name_data(ph, name=f"{ph.name} name")

            for x in range(3):
                A.setup_pokemon_species_data(
                    name=f"pokemon species {x} for {ph.name}",
                    pokemon_habitat=ph,
                )


    def test_pokemon_habitats(self):
        executed = self.execute_query(
            """
            query {
                pokemonHabitats {
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
                "pokemonHabitats": [
                    {
                        "idName": ph.name,
                        "names": [
                            {"text": n.name}
                            for n in ph.pokemonhabitatname.all()
                        ],
                        "pokemonSpeciess": {
                            "edges": [
                                {"node": {"idName": ps.name}}
                                for ps in ph.pokemonspecies.all()
                            ]
                        },
                    }
                    for ph in self.pokemon_habitats
                ]
            }
        }
        self.assertEqual(executed, expected)

    def test_pokemon_habitat(self):
        ph = self.pokemon_habitats[1]
        executed = self.execute_query(
            """
            query {
                pokemonHabitat(idName: "%s") {
                    idName
                }
            }
            """
            % ph.name
        )
        expected = {"data": {"pokemonHabitat": {"idName": ph.name}}}
        self.assertEqual(executed, expected)
