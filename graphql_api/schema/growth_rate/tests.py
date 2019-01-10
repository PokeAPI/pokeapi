from pokemon_v2.tests import APIData as A
from graphql_api.graphql_test import GraphQLTest


class GrowthRateTests(GraphQLTest):
    def setUp(self):
        self.growth_rates = [
            A.setup_growth_rate_data(name=f"growth rate {n}") for n in range(3)
        ]

        for i, gr in enumerate(self.growth_rates):
            A.setup_growth_rate_description_data(gr, description=f"{gr.name} desc")

            for x in range(1, 21):
                A.setup_experience_data(gr, level=x, experience=x ** i)

            for y in range(3):
                A.setup_pokemon_species_data(
                    name=f"pokemon species {y} for growth rate {gr.name}",
                    growth_rate=gr,
                )

    def test_growth_rates(self):
        executed = self.execute_query(
            """
            query {
                growthRates {
                    descriptions {text}
                    experienceForLevel99: experience(level: 99)
                    experienceForLevel32: experience(level: 32)
                    formula
                    levels {
                        level
                        experience
                    }
                    idName
                    pokemonSpeciess(first: 10) {
                        edges {
                            node {
                                idName
                            }
                        }
                    }
                }
            }
            """
        )

        def get_experience(experiences, level):
            for e in experiences:
                if e.level == level:
                    return e.experience

        expected = {
            "data": {
                "growthRates": [
                    {
                        "descriptions": [
                            {"text": d.description}
                            for d in gr.growthratedescription.all()
                        ],
                        "experienceForLevel99": get_experience(gr.experience.all(), 99),
                        "experienceForLevel32": get_experience(gr.experience.all(), 32),
                        "formula": gr.formula,
                        "levels": [
                            {"level": e.level, "experience": e.experience}
                            for e in gr.experience.all()
                        ],
                        "idName": gr.name,
                        "pokemonSpeciess": {
                            "edges": [
                                {"node": {"idName": ps.name}}
                                for ps in gr.pokemonspecies.all()
                            ]
                        },
                    }
                    for gr in self.growth_rates
                ]
            }
        }
        self.assertEqual(executed, expected)

    def test_growth_rate(self):
        gr = self.growth_rates[1]
        executed = self.execute_query(
            """
            query {
                growthRate(idName: "%s") {
                    idName
                }
            }
            """
            % gr.name
        )
        expected = {"data": {"growthRate": {"idName": gr.name}}}
        self.assertEqual(executed, expected)
