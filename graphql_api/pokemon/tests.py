import json
from pokemon_v2.tests import APIData as A
from ..graphql_test import GraphQLTest
from ..constants import IMAGE_HOST


class PokemonTests(GraphQLTest):
    def setUp(self):
        self.pokemons = []

        # Some species have more than one Pokémon
        for n in range(4):
            pokemon_species = A.setup_pokemon_species_data(
                name=f"pkmn spcs for pkmn {n}"
            )
            for m in range(1 + n):
                self.pokemons.append(
                    A.setup_pokemon_data(
                        pokemon_species=pokemon_species, name=f"pkm {n}.{m}"
                    )
                )

        move = None
        version_group = None
        encounter_method = A.setup_encounter_method_data()

        for i, p in enumerate(self.pokemons):
            A.setup_pokemon_form_data(p, name=f"pkmn form for {p.name}")
            A.setup_pokemon_ability_data(pokemon=p)
            A.setup_pokemon_stat_data(pokemon=p)
            A.setup_pokemon_type_data(pokemon=p)
            A.setup_pokemon_item_data(pokemon=p)
            A.setup_pokemon_sprites_data(pokemon=p)
            A.setup_pokemon_game_index_data(pokemon=p, game_index=i)

            # Some Pokémon have the same moves and version_group
            if not move or (i % 3 == 0):
                move = A.setup_move_data(name=f"mv {(i + 3) / 3}")
            if not version_group or (i % 5 == 0):
                version_group = A.setup_version_group_data(name=f"mv {(i + 5) / 5}")
            A.setup_pokemon_move_data(
                pokemon=p, move=move, version_group=version_group, level=i
            )

            for x in range(2):
                encounter_slot = A.setup_encounter_slot_data(
                    encounter_method, slot=i * 2 + x, rarity=x + 30
                )
                location_area = A.setup_location_area_data(
                    name=f"lctn area {x} for {p.name}"
                )
                A.setup_encounter_data(
                    location_area=location_area,
                    pokemon=p,
                    encounter_slot=encounter_slot,
                    min_level=x + 30,
                    max_level=x + 35,
                )

    def test_pokemons(self):
        executed = self.execute_query(
            """
            query {
                pokemons(first: 100) {
                    edges {
                        node {
                            abilities {
                                isHidden
                                order
                            }
                            baseExperience
                            gameIndices {
                                gameIndex
                                version {name}
                            }
                            height
                            isDefault
                            name
                            order
                            sprites {
                                frontDefault
                                frontShiny
                                frontFemale
                                frontShinyFemale
                                backDefault
                                backShiny
                                backFemale
                                backShinyFemale
                            }
                            stats {
                                baseValue
                                effortPoints
                            }
                            types {
                                order
                            }
                            weight
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
                "frontFemale": get_uri(data["front_female"]),
                "frontShinyFemale": get_uri(data["front_shiny_female"]),
                "backDefault": get_uri(data["back_default"]),
                "backShiny": get_uri(data["back_shiny"]),
                "backFemale": get_uri(data["back_female"]),
                "backShinyFemale": get_uri(data["back_shiny_female"]),
            }

        expected = {
            "data": {
                "pokemons": {
                    "edges": [
                        {
                            "node": {
                                "abilities": [
                                    {
                                        "isHidden": pa.is_hidden,
                                        "order": pa.slot,
                                        # "ability": {"name": pa.ability.name},
                                    }
                                    for pa in p.pokemonability.all()
                                ],
                                "baseExperience": p.base_experience,
                                "gameIndices": [
                                    {
                                        "gameIndex": pgi.game_index,
                                        "version": {"name": pgi.version.name},
                                    }
                                    for pgi in p.pokemongameindex.all()
                                ],
                                "height": p.height,
                                "isDefault": p.is_default,
                                "name": p.name,
                                "order": p.order,
                                "sprites": get_sprites(
                                    json.loads(p.pokemonsprites.all()[0].sprites)
                                ),
                                "stats": [
                                    {
                                        "baseValue": ps.base_stat,
                                        "effortPoints": ps.effort,
                                        # "stat": {"name": ps.stat.name}
                                    }
                                    for ps in p.pokemonstat.all()
                                ],
                                "types": [
                                    {
                                        "order": pt.slot,
                                        # "type": {"name": pt.type.name},
                                    }
                                    for pt in p.pokemontype.all()
                                ],
                                "weight": p.weight,
                            }
                        }
                        for p in self.pokemons
                    ]
                }
            }
        }
        self.assertEqual(executed, expected)

    def test_pokemon(self):
        p = self.pokemons[1]
        executed = self.execute_query(
            """
            query {
                pokemon(name: "%s") {
                    name
                }
            }
            """
            % p.name
        )
        expected = {"data": {"pokemon": {"name": p.name}}}
        self.assertEqual(executed, expected)
