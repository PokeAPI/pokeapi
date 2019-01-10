import json
from pokemon_v2.tests import APIData as A
from graphql_api.graphql_test import GraphQLTest
from graphql_api.constants import IMAGE_HOST


class PokemonFormTests(GraphQLTest):
    def setUp(self):
        self.pokemon_forms = []
        for n in range(6):
            for x in range(n % 3 + 1):  # some Pokémon have multiple forms
                pokemon_species = A.setup_pokemon_species_data(
                    name=f"pokemon species {n}.{x}"
                )
                pokemon = A.setup_pokemon_data(
                    pokemon_species=pokemon_species, name=f"pokemon {n}.{x}"
                )
                self.pokemon_forms.append(
                    A.setup_pokemon_form_data(
                        pokemon=pokemon, name=f"pokemon form for {pokemon.name}"
                    )
                )

        for pf in self.pokemon_forms:
            A.setup_pokemon_form_name_data(
                pf, name=pf.name, pokemon_name=f"pokemon {pf.name}"
            )
            A.setup_pokemon_form_sprites_data(pf)

    def test_pokemon_forms(self):
        executed = self.execute_query(
            """
            query {
                pokemonForms(first: 100) {
                    edges {
                        node {
                            formOrder
                            isBattleOnly
                            isDefault
                            isMega
                            idName
                            names {
                                text
                                shortText
                            }
                            order
                            pokemon {idName}
                            sprites {
                                frontDefault
                                frontShiny
                                backDefault
                                backShiny
                            }
                            versionGroup {idName}
                        }
                    }
                }
            }
            """
        )

        def get_uri(path):
            if path:
                return IMAGE_HOST + path.replace("/media/", "")
            return None

        def get_sprites(data):
            return {
                "frontDefault": get_uri(data["front_default"]),
                "frontShiny": get_uri(data["front_shiny"]),
                "backDefault": get_uri(data["back_default"]),
                "backShiny": get_uri(data["back_shiny"]),
            }

        expected = {
            "data": {
                "pokemonForms": {
                    "edges": [
                        {
                            "node": {
                                "formOrder": pf.form_order,
                                "isBattleOnly": pf.is_battle_only,
                                "isDefault": pf.is_default,
                                "isMega": pf.is_mega,
                                "idName": pf.name,
                                "names": [
                                    {"text": n.pokemon_name, "shortText": n.name}
                                    for n in pf.pokemonformname.all()
                                ],
                                "order": pf.order,
                                "pokemon": {"idName": pf.pokemon.name},
                                "sprites": get_sprites(
                                    json.loads(pf.pokemonformsprites.all()[0].sprites)
                                ),
                                "versionGroup": {"idName": pf.version_group.name},
                            }
                        }
                        for pf in self.pokemon_forms
                    ]
                }
            }
        }
        self.assertEqual(executed, expected)

    def test_pokemon_form(self):
        pokemon_form = self.pokemon_forms[1]
        executed = self.execute_query(
            """
            query {
                pokemonForm(idName: "%s") {
                    idName
                }
            }
            """
            % pokemon_form.name
        )
        expected = {"data": {"pokemonForm": {"idName": pokemon_form.name}}}
        self.assertEqual(executed, expected)
