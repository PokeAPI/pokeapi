import graphene as g
from graphql_api.utils import load, load_with_args
from .. import interfaces as i  # pylint: disable=unused-import
from .. import base


def calculate_gender_rate(root, info):
    if root.gender_rate == -1:
        return None
    return root.gender_rate * 12.5


class PokemonSpecies(g.ObjectType):
    """
    A Pokémon Species forms the basis for at least one Pokémon. Attributes of a Pokémon species are shared across all varieties of Pokémon within the species. A good example is Wormadam; Wormadam is the species which can be found in three different varieties, Wormadam-Trash, Wormadam-Sandy and Wormadam-Plant.
    """

    pk = None
    base_happiness = g.Int(
        description="The happiness when caught by a normal Pokéball; up to 255. The higher the number, the happier the Pokémon."
    )
    capture_rate = g.Int(
        description="The base capture rate; up to 255. The higher the number, the easier the catch."
    )
    pokemon_color_id = None
    color = g.Field(
        g.lazy_import("graphql_api.schema.pokemon_color.types.PokemonColor"),
        description="The color of this Pokémon for Pokédex search.",
        resolver=load("pokemoncolor", using="pokemon_color_id"),
    )
    egg_groups = g.List(
        g.lazy_import("graphql_api.schema.egg_group.types.EggGroup"),
        description="A list of egg groups this Pokémon species is a member of.",
        resolver=load("pokemonspecies_egggroups", using="pk"),
    )
    evolution_chain_id = None
    # evolution_chain = g.Field(
    #     g.lazy_import("graphql_api.schema.evolution_chain.types.EvolutionChain"),
    #     description="The evolution chain this Pokémon species is a member of.",
    #     resolver=load("evolutionchain", using="evolution_chain_id"),
    # )
    evolves_from_species_id = None
    evolves_from_species = g.Field(
        lambda: PokemonSpecies,
        description="The Pokémon species that evolves into this Pokemon_species.",
        resolver=load("pokemonspecies", using="evolves_from_species_id"),
    )
    flavor_text_entries = base.TranslationList(
        lambda: PokemonSpeciesFlavorText,
        description="A list of flavor text entries for this Pokémon species.",
        resolver=load_with_args("pokemonspecies_flavortextentries", using="pk"),
    )
    form_descriptions = base.TranslationList(
        lambda: PokemonSpeciesDescription,
        description="Descriptions of different forms Pokémon take on within the Pokémon species.",
        resolver=load_with_args("pokemonspecies_descriptions", using="pk"),
    )
    forms_switchable = g.Boolean(
        name="isFormsSwitchable",
        description="Whether or not this Pokémon has multiple forms and can switch between them.",
    )
    gender_rate = g.Float(
        description="The percent chance of this Pokémon being female, or null for genderless. A gender rate of 100% indicates that all Pokémon of this species are female, and 0% that all are male. A gender rate of 50% means that males and females are equally likely to occur. This value was originally stored as a single byte, with seven possible values (0, 12.5, 25, 50, 75, 87.5, 100, and null).",
        resolver=calculate_gender_rate,
    )
    genera = base.TranslationList(
        lambda: PokemonSpeciesGenus,
        description="The genus of this Pokémon species listed in multiple languages.",
        resolver=load_with_args("pokemonspecies_names", using="pk"),
    )
    generation_id = None
    generation = g.Field(
        g.lazy_import("graphql_api.schema.generation.types.Generation"),
        description="The generation this Pokémon species was introduced in.",
        resolver=load("generation", using="generation_id"),
    )
    growth_rate_id = None
    growth_rate = g.Field(
        g.lazy_import("graphql_api.schema.growth_rate.types.GrowthRate"),
        description="The rate at which this Pokémon species gains levels.",
        resolver=load("growthrate", using="growth_rate_id"),
    )
    pokemon_habitat_id = None
    habitat = g.Field(
        g.lazy_import("graphql_api.schema.pokemon_habitat.types.PokemonHabitat"),
        description="The habitat this Pokémon species can be encountered in.",
        resolver=load("pokemonhabitat", using="pokemon_habitat_id"),
    )
    has_gender_differences = g.Boolean(
        description="Whether or not this Pokémon has visual gender differences."
    )
    hatch_counter = g.Int(
        description="Initial hatch counter: one must walk 255 × (hatch_counter + 1) steps before this Pokémon's egg hatches, unless utilizing bonuses like Flame Body's."
    )
    is_baby = g.Boolean(description="Whether or not this is a baby Pokémon.")
    is_genderless = g.Boolean(
        description="Whether this Pokémon can have a gender. Genderless Pokémon do not have a gender rate.",
        resolver=lambda root, info: root.gender_rate == -1,
    )
    name = g.ID(name="idName", description="The name of this resource.")
    names = base.TranslationList(
        lambda: PokemonSpeciesName,
        description="The name of this resource listed in different languages.",
        resolver=load_with_args("pokemonspecies_names", using="pk"),
    )
    order = g.Int(
        description="The order in which species should be sorted. Based on National Dex order, except families are grouped together and sorted by stage."
    )
    pal_park_encounters = g.List(
        lambda: PokemonSpeciesPalParkEncounter,
        description="A list of encounters that can be had with this Pokémon species in pal park.",
        resolver=load("pokemonspecies_palparks", using="pk"),
    )
    pokedex_numbers = g.List(
        lambda: PokemonSpeciesPokedexEntry,
        description="A list of Pokedexes and the indexes reserved within them for this Pokémon species.",
        resolver=load("pokemonspecies_dexnumbers", using="pk"),
    )
    pokemon_shape_id = None
    shape = g.Field(
        g.lazy_import("graphql_api.schema.pokemon_shape.types.PokemonShape"),
        description="The shape of this Pokémon for Pokédex search.",
        resolver=load("pokemonshape", using="pokemon_shape_id"),
    )
    varieties = g.List(
        g.lazy_import("graphql_api.schema.pokemon.types.Pokemon"),
        description="A list of the Pokémon that exist within this Pokémon species.",
        resolver=load("pokemonspecies_pokemons", using="pk"),
    )


class PokemonSpeciesName(base.BaseTranslation, interfaces=[i.Translation]):
    name = g.String(
        name="text", description="The localized resource name in a specific language."
    )


class PokemonSpeciesFlavorText(base.BaseTranslation, interfaces=[i.Translation]):
    flavor_text = g.String(
        name="text",
        description="The localized flavor text for a resource in a specific language.",
    )
    version_id = None
    version = g.Field(
        g.lazy_import("graphql_api.schema.version.types.Version"),
        description="The version relevent to this flavor text.",
        resolver=load("version", using="version_id"),
    )


class PokemonSpeciesDescription(base.BaseTranslation, interfaces=[i.Translation]):
    description = g.String(
        name="text",
        description="The localized description for a resource in a specific language.",
    )


class PokemonSpeciesGenus(base.BaseTranslation, interfaces=[i.Translation]):
    genus = g.String(
        name="text",
        description="The localized genus for the referenced Pokémon species.",
    )


class PokemonSpeciesPokedexEntry(g.ObjectType):
    pokedex_number = g.Int(
        name="entryNumber", description="The index number within the Pokédex."
    )
    pokedex_id = None
    pokedex = g.Field(
        g.lazy_import("graphql_api.schema.pokedex.types.Pokedex"),
        description="The Pokédex the referenced Pokémon species can be found in.",
        resolver=load("pokedex", using="pokedex_id"),
    )


class PokemonSpeciesPalParkEncounter(g.ObjectType):
    base_score = g.Int(
        description="The base score given to the player when the referenced Pokémon is caught during a pal park run."
    )
    rate = g.Int(
        description="The base rate for encountering the referenced Pokémon in this pal park area."
    )
    pal_park_area_id = None
    # pal_park_area = g.Field(
    #     g.lazy_import("graphql_api.schema.pal_park_area.types.PalParkArea"),
    #     description="The pal park area where this encounter happens.",
    #     resolver=load("palparkarea", using="pal_park_area_id"),
    # )


class PokemonSpeciesPokedexEntry(g.ObjectType):
    pokedex_number = g.Int(
        name="entryNumber", description="The index number within the Pokédex."
    )
    pokedex_id = None
    pokedex = g.Field(
        g.lazy_import("graphql_api.schema.pokedex.types.Pokedex"),
        description="The Pokédex the referenced Pokémon species can be found in.",
        resolver=load("pokedex", using="pokedex_id"),
    )
