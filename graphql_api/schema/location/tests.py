from pokemon_v2.tests import APIData as A
from graphql_api.graphql_test import GraphQLTest


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
                            areas {idName}
                            gameIndices {
                                gameIndex
                                generation {idName}
                            }
                            idName
                            names {
                                text
                                language {idName}
                            }
                            region {idName}
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
                                    {"idName": a.name} for a in l.locationarea.all()
                                ],
                                "gameIndices": [
                                    {
                                        "gameIndex": lgi.game_index,
                                        "generation": {"idName": lgi.generation.name}
                                    } for lgi in l.locationgameindex.all()
                                ],
                                "idName": l.name,
                                "names": [
                                    {
                                        "text": n.name,
                                        "language": {"idName": n.language.name},
                                    }
                                    for n in l.locationname.all()
                                ],
                                "region": {"idName": l.region.name},
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
                location(idName: "%s") {
                    idName
                    names {
                        text
                        language {idName}
                    }
                }
            }
            """
            % l.name
        )
        expected = {
            "data": {
                "location": {
                    "idName": l.name,
                    "names": [
                        {"text": n.name, "language": {"idName": n.language.name}}
                        for n in l.locationname.all()
                    ],
                }
            }
        }
        self.assertEqual(executed, expected)
