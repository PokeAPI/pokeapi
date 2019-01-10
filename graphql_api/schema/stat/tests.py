from pokemon_v2.tests import APIData as A
from graphql_api.graphql_test import GraphQLTest


class StatTests(GraphQLTest):
    def setUp(self):
        self.stats = [A.setup_stat_data(name=f"stat {n}") for n in range(10)]

        for stat in self.stats:
            A.setup_stat_name_data(stat, name=f"{stat.name} name")

            for _ in range(3):
                A.setup_characteristic_data(stat=stat)

            for change in range(-3, 2):
                move = A.setup_move_data(name=f"move {change} for {stat.name}")
                A.setup_move_stat_change_data(move=move, stat=stat, change=change)

            for _ in range(4):
                A.setup_nature_data(name=f"+ntr for {stat.name}", increased_stat=stat)
                A.setup_nature_data(name=f"-ntr for {stat.name}", decreased_stat=stat)

    def test_stats(self):
        executed = self.execute_query(
            """
            query {
                stats{
                    characteristics {idName}
                    gameIndex
                    isBattleOnly
                    idName
                    names {
                        text
                        language {idName}
                    }
                    negativeAffectingNatures {idName}
                    positiveAffectingNatures {idName}
                }
            }
            """
        )
        expected = {
            "data": {
                "stats": [
                    {
                        "characteristics": [
                            {"idName": str(char.pk)} for char in stat.characteristic.all()
                        ],
                        "gameIndex": stat.game_index,
                        "isBattleOnly": stat.is_battle_only,
                        "idName": stat.name,
                        "names": [
                            {"text": n.name, "language": {"idName": n.language.name}}
                            for n in stat.statname.all()
                        ],
                        "negativeAffectingNatures": [
                            {"idName": nature.name} for nature in stat.decreased.all()
                        ],
                        "positiveAffectingNatures": [
                            {"idName": nature.name} for nature in stat.increased.all()
                        ],
                    }
                    for stat in self.stats
                ]
            }
        }
        self.assertEqual(executed, expected)

    def test_stat(self):
        stat = self.stats[1]
        executed = self.execute_query(
            """
            query {
                stat(idName: "%s") {
                    idName
                    names {
                        text
                        language {idName}
                    }
                }
            }
            """
            % stat.name
        )
        expected = {
            "data": {
                "stat": {
                    "idName": stat.name,
                    "names": [
                        {"text": n.name, "language": {"idName": n.language.name}}
                        for n in stat.statname.all()
                    ],
                }
            }
        }
        self.assertEqual(executed, expected)
