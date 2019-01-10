from pokemon_v2.tests import APIData as A
from graphql_api.graphql_test import GraphQLTest


class GenerationTests(GraphQLTest):
    def setUp(self):
        self.generations = []
        for n in range(4):
            region = A.setup_region_data(name=f"reg for gen {n}")
            self.generations.append(
                A.setup_generation_data(name=f"base gen {n}", region=region)
            )
        for gen in self.generations:
            A.setup_generation_name_data(gen, name=f"{gen.name} name")
            A.setup_ability_data(name=f"ablty for {gen.name}", generation=gen)
            of_type = A.setup_type_data(name=f"tp for {gen.name}", generation=gen)
            A.setup_move_data(name=f"mv for {gen.name}", generation=gen, type=of_type)
            A.setup_pokemon_species_data(
                name=f"pkmn spcs for {gen.name}", generation=gen
            )
            A.setup_version_group_data(name=f"ver grp for {gen.name}", generation=gen)

    def test_generations(self):
        executed = self.execute_query(
            """
            query {
                generations(first: 10) {
                    edges {
                        node {
                            mainRegion {idName}
                            idName
                            names {
                                text
                                language {idName}
                            }
                            pokemonSpecies(first: 10) {
                                totalCount
                                edges {
                                    node {idName}
                                }
                            }
                            versionGroups {idName}
                        }
                    }
                }
            }
            """
        )
        expected = {
            "data": {
                "generations": {
                    "edges": [
                        {
                            "node": {
                                "mainRegion": {"idName": gen.region.name},
                                "idName": gen.name,
                                "names": [
                                    {
                                        "text": n.name,
                                        "language": {"idName": n.language.name},
                                    }
                                    for n in gen.generationname.all()
                                ],
                                "pokemonSpecies": {
                                    "totalCount": len(gen.pokemonspecies.all()),
                                    "edges": [
                                        {"node": {"idName": ps.name}}
                                        for ps in gen.pokemonspecies.all()
                                    ],
                                },
                                "versionGroups": [
                                    {"idName": vg.name} for vg in gen.versiongroup.all()
                                ],
                            }
                        }
                        for gen in self.generations
                    ]
                }
            }
        }
        self.assertEqual(executed, expected)

    def test_generation(self):
        gen = self.generations[1]
        executed = self.execute_query(
            """
            query {
                generation(idName: "%s") {
                    idName
                    names {
                        text
                        language {idName}
                    }
                }
            }
            """
            % gen.name
        )
        expected = {
            "data": {
                "generation": {
                    "idName": gen.name,
                    "names": [
                        {"text": n.name, "language": {"idName": n.language.name}}
                        for n in gen.generationname.all()
                    ],
                }
            }
        }
        self.assertEqual(executed, expected)
