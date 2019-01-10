from pokemon_v2.tests import APIData as A
from graphql_api.graphql_test import GraphQLTest


class GenderTests(GraphQLTest):
    def setUp(self):
        male = A.setup_gender_data(name="male")
        female = A.setup_gender_data(name="female")
        genderless = A.setup_gender_data(name="genderless")

        self.genders = [male, female, genderless]
        self.pokemon_species = {"male": [], "female": [], "genderless": []}

        # male
        for x in range(3):
            species = A.setup_pokemon_species_data(
                name=f"species {x} for {male.name}", gender_rate=8
            )
            A.setup_pokemon_evolution_data(evolved_species=species, gender=male)
            self.pokemon_species["male"].append(species)

        # female
        for y in range(4):
            species = A.setup_pokemon_species_data(
                name=f"species {y} for {female.name}", gender_rate=0
            )
            A.setup_pokemon_evolution_data(evolved_species=species, gender=None)
            self.pokemon_species["female"].append(species)

        # genderless
        for z in range(1):
            species = A.setup_pokemon_species_data(
                name=f"species {z} for {genderless.name}", gender_rate=-1
            )
            A.setup_pokemon_evolution_data(evolved_species=species, gender=genderless)
            self.pokemon_species["genderless"].append(species)

    def test_genders(self):
        executed = self.execute_query(
            """
            query {
                genders {
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
        expected = {
            "data": {
                "genders": [
                    {
                        "idName": gender.name,
                        "pokemonSpeciess": {
                            "edges": [
                                {"node": {"idName": ps.name}}
                                for ps in self.pokemon_species[gender.name]
                            ]
                        },
                    }
                    for gender in self.genders
                ]
            }
        }
        self.assertEqual(executed, expected)

    def test_gender(self):
        gender = self.genders[1]
        executed = self.execute_query(
            """
            query {
                gender(idName: "%s") {
                    idName
                }
            }
            """
            % gender.name
        )
        expected = {"data": {"gender": {"idName": gender.name}}}
        self.assertEqual(executed, expected)
