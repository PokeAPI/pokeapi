from pokemon_v2.tests import APIData as A
from graphql_api.graphql_test import GraphQLTest


class NatureTests(GraphQLTest):
    def setUp(self):
        self.natures = [
            A.setup_nature_data(
                name=f"nature {n}",
                hates_flavor=A.setup_berry_flavor_data(name=f"hts flvr for nature {n}"),
                likes_flavor=A.setup_berry_flavor_data(name=f"lks flvr for nature {n}"),
                decreased_stat=A.setup_stat_data(name=f"dcrs stt for nature {n}"),
                increased_stat=A.setup_stat_data(name=f"ncrs stt for nature {n}"),
            )
            for n in range(4)
        ]

        for nature in self.natures:
            A.setup_nature_name_data(nature, name=f"{nature.name} name")

            for x in range(3):
                A.setup_nature_pokeathlon_stat_data(
                    nature=nature,
                    pokeathlon_stat=A.setup_pokeathlon_stat_data(
                        name=f"pkeathln stt {x} for {nature.name}"
                    ),
                    max_change=x,
                )
                A.setup_nature_battle_style_preference_data(
                    nature=nature,
                    move_battle_style=A.setup_move_battle_style_data(
                        name="mv btl stl {x} for {nature.name}"
                    ),
                )

    def test_natures(self):
        executed = self.execute_query(
            """
            query {
                natures {
                    decreasedStat {idName}
                    increasedStat {idName}
                    moveBattleStylePreferences {
                        lowHPPreference
                        highHPPreference
                    }
                    idName
                    names {
                        text
                        language {idName}
                    }
                    pokeathlonStatChanges {
                        maxChange
                    }
                }
            }
            """
        )
        expected = {
            "data": {
                "natures": [
                    {
                        "decreasedStat": {"idName": nature.decreased_stat.name},
                        # "hatesFlavor": {"idName": nature.hates_flavor.name},
                        "increasedStat": {"idName": nature.increased_stat.name},
                        # "likesFlavor": {"idName": nature.likes_flavor.name},
                        "moveBattleStylePreferences": [
                            {
                                "lowHPPreference": nbsp.low_hp_preference,
                                "highHPPreference": nbsp.high_hp_preference,
                                # "moveBattleStyle": {
                                #     "idName": nbsp.move_battle_style.name
                                # },
                            }
                            for nbsp in nature.naturebattlestylepreference.all()
                        ],
                        "idName": nature.name,
                        "names": [
                            {"text": n.name, "language": {"idName": n.language.name}}
                            for n in nature.naturename.all()
                        ],
                        "pokeathlonStatChanges": [
                            {
                                "maxChange": nps.max_change,
                                # "pokeathlonStat": {"idName": nps.pokeathlon_stat.name},
                            }
                            for nps in nature.naturepokeathlonstat.all()
                        ]
                    }
                    for nature in self.natures
                ]
            }
        }
        self.assertEqual(executed, expected)

    def test_nature(self):
        nature = self.natures[1]
        executed = self.execute_query(
            """
            query {
                nature(idName: "%s") {
                    idName
                    names {
                        text
                        language {idName}
                    }
                }
            }
            """
            % nature.name
        )
        expected = {
            "data": {
                "nature": {
                    "idName": nature.name,
                    "names": [
                        {"text": n.name, "language": {"idName": n.language.name}}
                        for n in nature.naturename.all()
                    ],
                }
            }
        }
        self.assertEqual(executed, expected)
