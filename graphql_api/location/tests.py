from pokemon_v2.tests import APIData as A
from ..graphql_test import GraphQLTest


class LocationTests(GraphQLTest):
    def setUp(self):
        region = A.setup_region_data(name="rgn for lctn")
        self.locations = [
            A.setup_location_data(name=f"base lctn {n}", region=region)
            for n in range(4)
        ]
        for l in self.locations:
            A.setup_location_name_data(l, name=f"{l.name} name")
            A.setup_location_game_index_data(l, game_index=l.id + 10)
            A.setup_location_area_data(l, name=f"lctn area for {l.name}")

    def test_locations(self):
        executed = self.execute_query(
            """
            query {
                locations(first: 10) {
                    edges {
                        node {
                            areas {name}
                            gameIndices {
                                gameIndex
                                generation {name}
                            }
                            name
                            names {
                                text
                                language {name}
                            }
                            region {name}
                        }
                    }
                }
            }
            """
        )
        expected = {
            "data": {
                "locations": {
                    "edges": [
                        {
                            "node": {
                                "areas": [
                                    {"name": a.name} for a in l.locationarea.all()
                                ],
                                "gameIndices": [
                                    {
                                        "gameIndex": lgi.game_index,
                                        "generation": {"name": lgi.generation.name}
                                    } for lgi in l.locationgameindex.all()
                                ],
                                "name": l.name,
                                "names": [
                                    {
                                        "text": n.name,
                                        "language": {"name": n.language.name},
                                    }
                                    for n in l.locationname.all()
                                ],
                                "region": {"name": l.region.name},
                            }
                        }
                        for l in self.locations
                    ]
                }
            }
        }
        self.assertEqual(executed, expected)

    def test_location(self):
        l = self.locations[1]
        executed = self.execute_query(
            """
            query {
                location(name: "%s") {
                    name
                    names {
                        text
                        language {name}
                    }
                }
            }
            """
            % l.name
        )
        expected = {
            "data": {
                "location": {
                    "name": l.name,
                    "names": [
                        {"text": n.name, "language": {"name": n.language.name}}
                        for n in l.locationname.all()
                    ],
                }
            }
        }
        self.assertEqual(executed, expected)
