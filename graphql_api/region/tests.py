from pokemon_v2.tests import APIData as A
from ..graphql_test import GraphQLTest


class RegionTests(GraphQLTest):
    def setUp(self):
        self.regions = [A.setup_region_data(name=f"base rgn {n}") for n in range(4)]
        generations = []

        for r in self.regions:
            A.setup_region_name_data(r, name=f"{r.name} name")
            A.setup_location_data(region=r, name=f"lctn for {r.name}")
            generations.append(
                A.setup_generation_data(region=r, name=f"gnrtn for {r.name}")
            )
            A.setup_pokedex_data(region=r, name=f"pkdx for {r.name}")
            A.setup_pokedex_data(region=r, name=f"pkdx for {r.name}")

        version_group = A.setup_version_group_data(
            name="ver grp", generation=generations[0]
        )
        for r in self.regions:
            A.setup_version_group_region_data(region=r, version_group=version_group)

    def test_regions(self):
        executed = self.execute_query(
            """
            query {
                regions(first: 10) {
                    edges {
                        node {
                            locations(first: 5) {
                                edges {
                                    node {
                                        name
                                    }
                                }
                            }
                            mainGeneration {name}
                            name
                            names {
                                text
                                language {name}
                            }
                            versionGroups {name}
                        }
                    }
                }
            }
            """
        )
        expected = {
            "data": {
                "regions": {
                    "edges": [
                        {
                            "node": {
                                "locations": {
                                    "edges": [
                                        {"node": {"name": l.name}}
                                        for l in reg.location.all()
                                    ]
                                },
                                "mainGeneration": {"name": reg.generation.name},
                                "name": reg.name,
                                "names": [
                                    {
                                        "text": n.name,
                                        "language": {"name": n.language.name},
                                    }
                                    for n in reg.regionname.all()
                                ],
                                "versionGroups": [
                                    {"name": vgr.version_group.name}
                                    for vgr in reg.versiongroupregion.all()
                                ],
                            }
                        }
                        for reg in self.regions
                    ]
                }
            }
        }
        self.assertEqual(executed, expected)

    def test_region(self):
        m = self.regions[1]
        executed = self.execute_query(
            """
            query {
                region(name: "%s") {
                    name
                    names {
                        text
                        language {name}
                    }
                }
            }
            """
            % m.name
        )
        expected = {
            "data": {
                "region": {
                    "name": m.name,
                    "names": [
                        {"text": n.name, "language": {"name": n.language.name}}
                        for n in m.regionname.all()
                    ],
                }
            }
        }
        self.assertEqual(executed, expected)
