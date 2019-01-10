from pokemon_v2.tests import APIData as A
from graphql_api.graphql_test import GraphQLTest


class EncounterConditionTests(GraphQLTest):
    def setUp(self):
        self.encounter_conditions = [
            A.setup_encounter_condition_data(name=f"enctr method {n}") for n in range(4)
        ]

        for ec in self.encounter_conditions:
            A.setup_encounter_condition_name_data(ec, name=f"{ec.name} name")

    def test_encounter_conditions(self):
        executed = self.execute_query(
            """
            query {
                encounterConditions {
                    idName
                    names {text}
                    values {
                        condition {idName}
                        isDefault
                        idName
                        names {text}
                    }
                }
            }
            """
        )
        expected = {
            "data": {
                "encounterConditions": [
                    {
                        "idName": ec.name,
                        "names": [
                            {"text": n.name} for n in ec.encounterconditionname.all()
                        ],
                        "values": [
                            {
                                "condition": {"idName": ec.name},
                                "isDefault": value.is_default,
                                "idName": value.name,
                                "names": [
                                    {"text": n.name}
                                    for n in value.encounterconditionvaluename.all()
                                ]
                            }
                            for value in ec.encounterconditionvalue.all()
                        ],
                    }
                    for ec in self.encounter_conditions
                ]
            }
        }
        self.assertEqual(executed, expected)

    def test_encounter_condition(self):
        ec = self.encounter_conditions[1]
        executed = self.execute_query(
            """
            query {
                encounterCondition(idName: "%s") {
                    idName
                }
            }
            """
            % ec.name
        )
        expected = {"data": {"encounterCondition": {"idName": ec.name}}}
        self.assertEqual(executed, expected)
