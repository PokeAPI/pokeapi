import json
import graphene as g
from graphql_api.constants import IMAGE_HOST
from graphql_api.utils import load, load_with_args
from .. import interfaces as i  # pylint: disable=unused-import
from .. import base


class PokemonForm(g.ObjectType):
    """
    Some Pokémon have the ability to take on different forms. At times, these differences are purely cosmetic and have no bearing on the difference in the Pokémon's stats from another; however, several Pokémon differ in stats (other than HP), type, and Ability depending on their form.
    """

    pk = None
    form_name = g.String(description="The name of this form.")
    form_order = g.Int(
        description="The order in which forms should be sorted within a species' forms."
    )
    is_battle_only = g.Boolean(
        description="Whether or not this form can only happen during battle."
    )
    is_default = g.Boolean(
        description="True for exactly one form used as the default for each Pokémon."
    )
    is_mega = g.Boolean(description="Whether or not this form requires mega evolution.")
    name = g.ID(name="idName", description="The name of this resource.")
    names = base.TranslationList(
        lambda: PokemonFormName,
        description="The name of this resource listed in different languages.",
        resolver=load_with_args("pokemonform_names", using="pk"),
    )
    order = g.Int(
        description="The order in which forms should be sorted within all forms. Multiple forms may have equal order, in which case they should fall back on sorting by name."
    )
    pokemon_id = None
    pokemon = g.Field(
        g.lazy_import("graphql_api.schema.pokemon.types.Pokemon"),
        description="The Pokémon that can take on this form.",
        resolver=load("pokemon", using="pokemon_id"),
    )
    sprites = g.Field(
        lambda: PokemonFormSprites,
        description="A set of sprites used to depict this Pokémon form in the game.",
        resolver=load("pokemonformsprites", using="pk"),
    )
    version_group_id = None
    version_group = g.Field(
        g.lazy_import("graphql_api.schema.version_group.types.VersionGroup"),
        description="The version group this Pokémon form was introduced in.",
        resolver=load("versiongroup", using="version_group_id"),
    )


class PokemonFormName(base.BaseTranslation, interfaces=[i.Translation]):
    pokemon_name = g.String(
        name="text",
        description='The full localized name for a Pokémon form in a specific language, e.g. "Unown A".',
    )
    name = g.String(
        name="shortText",
        description='The form-specific localized name for a Pokémon form in a specific language, e.g. "A" for Unown A.',
    )


def get_sprite(sprite_name):
    def inner(root, info):
        sprites_data = json.loads(root.sprites)
        if sprites_data[sprite_name]:
            return IMAGE_HOST + sprites_data[sprite_name].replace("/media/", "")
        return None

    return inner


class PokemonFormSprites(g.ObjectType):
    """Image sprites depicting Pokémon forms in battle."""

    sprites = None
    front_default = base.URI(resolver=get_sprite("front_default"))
    front_shiny = base.URI(resolver=get_sprite("front_shiny"))
    back_default = base.URI(resolver=get_sprite("back_default"))
    back_shiny = base.URI(resolver=get_sprite("back_shiny"))
