from pokemon_v2.tests import APIData as A
from graphql_api.graphql_test import GraphQLTest


class CharacteristicTests(GraphQLTest):
    def setUp(self):
        self.characteristics = [
            A.setup_characteristic_data(
                gene_mod_5=n * 5, stat=A.setup_stat_data(name=f"stat for char {n}")
            )
            for n in range(4)
        ]
        for char in self.characteristics:
            A.setup_characteristic_description_data(
                char, description=f"char {char.pk} description"
            )

    def test_characteristics(self):
        executed = self.execute_query(
            """
            query {
                characteristics {
                    descriptions {
                        text
                        language {name}
                    }
                    geneModulo
                    highestStat {name}
                    name
                    possibleValues
                }
            }
            """
        )

        def get_possible_values(mod):
            values = []
            while mod <= 30:
                values.append(mod)
                mod += 5
            return values

        expected = {
            "data": {
                "characteristics": [
                    {
                        "descriptions": [
                            {
                                "text": d.description,
                                "language": {"name": d.language.name},
                            }
                            for d in char.characteristicdescription.all()
                        ],
                        "geneModulo": char.gene_mod_5,
                        "highestStat": {"name": char.stat.name},
                        "name": str(char.pk),
                        "possibleValues": get_possible_values(char.gene_mod_5),
                    }
                    for char in self.characteristics
                ]
            }
        }
        self.assertEqual(executed, expected)

    def test_characteristic(self):
        char = self.characteristics[1]
        executed = self.execute_query(
            """
            query {
                characteristic(name: "%i") {
                    name
                }
            }
            """
            % char.pk
        )
        expected = {"data": {"characteristic": {"name": str(char.pk)}}}
        self.assertEqual(executed, expected)
