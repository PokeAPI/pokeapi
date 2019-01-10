from pokemon_v2.tests import APIData as A
from graphql_api.graphql_test import GraphQLTest


class PokedexTests(GraphQLTest):
    def setUp(self):
        self.pokedexes = [A.setup_pokedex_data(name=f"pkdx {i}") for i in range(4)]

        for p in self.pokedexes:
            A.setup_pokedex_name_data(p, name=f"{p.name} name")
            A.setup_pokedex_description_data(p, description=f"{p.name} desc")

            for n in range(10):
                pokemon_species = A.setup_pokemon_species_data(
                    name=f"pkmn spcs {n} for {p.name}"
                )
                A.setup_pokemon_dex_entry_data(
                    pokedex=p, pokemon_species=pokemon_species
                )

    def test_pokedexes(self):
        executed = self.execute_query(
            """
            query {
                pokedexes {
                    isMainSeries
                    descriptions {text}
                    idName
                    names {
                        text
                        language {idName}
                    }
                    pokemonEntries(first: 100) {
                        totalCount
                        edges {
                            entryNumber
                            node {idName}
                        }
                    }
                }
            }
            """
        )
        expected = {
            "data": {
                "pokedexes": [
                    {
                        "isMainSeries": p.is_main_series,
                        "descriptions": [
                            {"text": d.description} for d in p.pokedexdescription.all()
                        ],
                        "idName": p.name,
                        "names": [
                            {"text": n.name, "language": {"idName": n.language.name}}
                            for n in p.pokedexname.all()
                        ],
                        "pokemonEntries": {
                            "totalCount": len(p.pokemondexnumber.all()),
                            "edges": [
                                {
                                    "entryNumber": pdn.pokedex_number,
                                    "node": {"idName": pdn.pokemon_species.name},
                                }
                                for pdn in p.pokemondexnumber.all()
                            ],
                        },
                    }
                    for p in self.pokedexes
                ]
            }
        }
        self.assertEqual(executed, expected)

    def test_pokedex(self):
        p = self.pokedexes[1]
        executed = self.execute_query(
            """
            query {
                pokedex(idName: "%s") {
                    idName
                }
            }
            """
            % p.name
        )
        expected = {"data": {"pokedex": {"idName": p.name}}}
        self.assertEqual(executed, expected)
