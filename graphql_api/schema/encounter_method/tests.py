from pokemon_v2.tests import APIData as A
from graphql_api.graphql_test import GraphQLTest


class EncounterMethodTests(GraphQLTest):
    def setUp(self):
        self.encounter_methods = [
            A.setup_encounter_method_data(name=f"enctr method {n}") for n in range(4)
        ]

        for em in self.encounter_methods:
            A.setup_encounter_method_name_data(em, name=f"{em.name} name")

    def test_encounter_methods(self):
        executed = self.execute_query(
            """
            query {
                encounterMethods {
                    name
                    names {text}
                    order
                }
            }
            """
        )
        expected = {
            "data": {
                "encounterMethods": [
                    {
                        "name": em.name,
                        "names": [{"text": n.name} for n in em.encountermethodname.all()],
                        "order": em.order,
                    }
                    for em in self.encounter_methods
                ]
            }
        }
        self.assertEqual(executed, expected)

    def test_encounter_method(self):
        em = self.encounter_methods[1]
        executed = self.execute_query(
            """
            query {
                encounterMethod(name: "%s") {
                    name
                }
            }
            """
            % em.name
        )
        expected = {"data": {"encounterMethod": {"name": em.name}}}
        self.assertEqual(executed, expected)
