from pokemon_v2.tests import APIData as A
from graphql_api.graphql_test import GraphQLTest


class PokemonSpeciesTests(GraphQLTest):
    def setUp(self):
        self.pokemon_species = []
        for n in range(4):
            evolution_chain = A.setup_evolution_chain_data()
            previous = None
            for x in range(n + 1):
                pokemon_species = A.setup_pokemon_species_data(
                    name=f"pkmn spcs {n}.{x}",
                    evolution_chain=evolution_chain,
                    evolves_from_species=previous,
                )
                self.pokemon_species.append(pokemon_species)
                A.setup_pokemon_evolution_data(evolved_species=pokemon_species)

        egg_group = None
        pokedex = None
        for i, ps in enumerate(self.pokemon_species):
            A.setup_pokemon_species_name_data(ps, name=f"{ps.name} name")
            A.setup_pokemon_species_form_description_data(
                ps, description=f"frm dscr for {ps.name}"
            )
            A.setup_pokemon_species_flavor_text_data(
                ps, flavor_text=f"flvr txt for {ps.name}"
            )
            A.setup_pal_park_data(pokemon_species=ps)

            for x in range(2):
                A.setup_pokemon_data(pokemon_species=ps, name=f"pkm {x} for {ps.name}")

            if egg_group is None or (i % 3 == 0):
                egg_group = A.setup_egg_group_data()
            if pokedex is None or (i % 2 == 0):
                pokedex = A.setup_pokedex_data()

            A.setup_pokemon_dex_entry_data(
                pokemon_species=ps, pokedex=pokedex, entry_number=i * 13
            )
            A.setup_pokemon_egg_group_data(pokemon_species=ps, egg_group=egg_group)

    def test_pokemon_speciess(self):
        executed = self.execute_query(
            """
            query {
                pokemonSpeciess(first: 100) {
                    edges {
                        node {
                            baseHappiness
                            captureRate
                            color {idName}
                            eggGroups {idName}
                            evolvesFromSpecies {idName}
                            flavorTextEntries {text}
                            formDescriptions {text}
                            isFormsSwitchable
                            genderRate
                            genera {text}
                            generation {idName}
                            growthRate {idName}
                            habitat {idName}
                            hasGenderDifferences
                            hatchCounter
                            isBaby
                            isGenderless
                            idName
                            names {
                                text
                                language {idName}
                            }
                            order
                            pokedexNumbers {
                                entryNumber
                            }
                            palParkEncounters {
                                baseScore
                                rate
                            }
                            shape {idName}
                            varieties {idName}
                        }
                    }
                }
            }
            """
        )
        expected = {
            "data": {
                "pokemonSpeciess": {
                    "edges": [
                        {
                            "node": {
                                "baseHappiness": ps.base_happiness,
                                "captureRate": ps.capture_rate,
                                "color": {"idName": ps.pokemon_color.name},
                                "eggGroups": [
                                    {"idName": peg.egg_group.name}
                                    for peg in ps.pokemonegggroup.all()
                                ],
                                "evolvesFromSpecies": {
                                    "idName": ps.evolves_from_species.name
                                }
                                if ps.evolves_from_species
                                else None,
                                "flavorTextEntries": [
                                    {"text": ft.flavor_text}
                                    for ft in ps.pokemonspeciesflavortext.all()
                                ],
                                "formDescriptions": [
                                    {"text": d.description}
                                    for d in ps.pokemonspeciesdescription.all()
                                ],
                                "isFormsSwitchable": ps.forms_switchable,
                                "genderRate": (
                                    ps.gender_rate * 12.5 if ps.gender_rate != -1 else None
                                ),
                                "genera": [
                                    {"text": n.genus}
                                    for n in ps.pokemonspeciesname.all()
                                ],
                                "generation": {"idName": ps.generation.name},
                                "growthRate": {"idName": ps.growth_rate.name},
                                "habitat": {"idName": ps.pokemon_habitat.name},
                                "hasGenderDifferences": ps.has_gender_differences,
                                "hatchCounter": ps.hatch_counter,
                                "isBaby": ps.is_baby,
                                "isGenderless": ps.gender_rate == -1,
                                "idName": ps.name,
                                "names": [
                                    {
                                        "text": n.name,
                                        "language": {"idName": n.language.name},
                                    }
                                    for n in ps.pokemonspeciesname.all()
                                ],
                                "order": ps.order,
                                "pokedexNumbers": [
                                    {
                                        "entryNumber": pn.pokedex_number,
                                        # "pokedex": {"idName": pn.pokedex.name},
                                    }
                                    for pn in ps.pokemondexnumber.all()
                                ],
                                "palParkEncounters": [
                                    {
                                        "baseScore": ppe.base_score,
                                        "rate": ppe.rate,
                                        # "palParkArea": {"idName": ppe.pal_park_area.name},
                                    }
                                    for ppe in ps.palpark.all()
                                ],
                                "shape": {"idName": ps.pokemon_shape.name},
                                "varieties": [
                                    {"idName": p.name} for p in ps.pokemon.all()
                                ],
                            }
                        }
                        for ps in self.pokemon_species
                    ]
                }
            }
        }
        self.assertEqual(executed, expected)

    def test_pokemon_species(self):
        ps = self.pokemon_species[1]
        executed = self.execute_query(
            """
            query {
                pokemonSpecies(idName: "%s") {
                    idName
                }
            }
            """
            % ps.name
        )
        expected = {"data": {"pokemonSpecies": {"idName": ps.name}}}
        self.assertEqual(executed, expected)