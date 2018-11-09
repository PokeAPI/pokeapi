from pokemon_v2.tests import APIData as A
from graphql_api.graphql_test import GraphQLTest


class EggGroupTests(GraphQLTest):
    def setUp(self):
        self.egg_groups = [
            A.setup_egg_group_data(name=f"egg group {n}") for n in range(4)
        ]
        for eg in self.egg_groups:
            A.setup_egg_group_name_data(eg, name=f"{eg.name} name")

            for _ in range(6):
                ps = A.setup_pokemon_species_data()
                A.setup_pokemon_egg_group_data(pokemon_species=ps, egg_group=eg)

    def test_egg_groups(self):
        executed = self.execute_query(
            """
            query {
                eggGroups {
                    name
                    names {text}
                    pokemonSpecies(first: 10) {
                        edges {
                            node {name}
                        }
                    }
                }
            }
            """
        )
        expected = {
            "data": {
                "eggGroups": [
                    {
                        "name": egg_group.name,
                        "names": [
                            {"text": n.name}
                            for n in egg_group.egggroupname.all()
                        ],
                        "pokemonSpecies": {
                            "edges": [
                                {
                                    "node": {"name": peg.pokemon_species.name}
                                }
                                for peg in egg_group.pokemonegggroup.all()
                            ]
                        }
                    }
                    for egg_group in self.egg_groups
                ]
            }
        }
        self.assertEqual(executed, expected)

    def test_egg_group(self):
        egg_group = self.egg_groups[1]
        executed = self.execute_query(
            """
            query {
                eggGroup(name: "%s") {
                    name
                    names {
                        text
                        language {name}
                    }
                }
            }
            """
            % egg_group.name
        )
        expected = {
            "data": {
                "eggGroup": {
                    "name": egg_group.name,
                    "names": [
                        {"text": n.name, "language": {"name": n.language.name}}
                        for n in egg_group.egggroupname.all()
                    ],
                }
            }
        }
        self.assertEqual(executed, expected)
