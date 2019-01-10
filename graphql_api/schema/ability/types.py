import graphene as g
from pokemon_v2 import models
from graphql_api.utils import load, load_with_args, get_page
from ..pokemon.types import Pokemon  # pylint: disable=unused-import
from .. import interfaces as i  # pylint: disable=unused-import
from .. import base


class Ability(g.ObjectType):
    """
    Abilities provide passive effects for Pokémon in battle or in the overworld. Pokémon have multiple possible abilities but can have only one ability at a time. Check out [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Ability) for greater detail.
    """

    pk = None
    is_main_series = g.Boolean(
        description="Whether or not this ability originated in the main series of the video games."
    )
    effect_entries = base.TranslationList(
        lambda: AbilityEffect,
        description="The effect of this ability listed in different languages.",
        resolver=load_with_args("ability_effectentries", using="pk"),
    )
    generation_id = None
    generation = g.Field(
        g.lazy_import("graphql_api.schema.generation.types.Generation"),
        description="The generation this ability originated in.",
        resolver=load("generation", using="generation_id"),
    )
    effect_history = g.List(
        lambda: AbilityEffectChange,
        description="The list of previous effects this ability has had across version groups.",
        resolver=load("ability_changes", using="pk"),
    )
    flavor_text_entries = base.TranslationList(
        lambda: AbilityFlavorText,
        description="The in-game description of this ability's effects listed in different languages.",
        resolver=load_with_args("ability_flavortextentries", using="pk"),
    )
    name = g.ID(name="idName", description="The name of this resource.")
    names = base.TranslationList(
        lambda: AbilityName,
        description="The name of this resource listed in different languages.",
        resolver=load_with_args("ability_names", using="pk"),
    )
    pokemons = g.relay.ConnectionField(
        lambda: AbilityPokemonConnection,
        description="A list of Pokémon that could potentially have this ability.",
        where=g.Argument(lambda: AbilityPokemonWhere),
        order_by=g.List(lambda: AbilityPokemonSort),
    )

    def resolve_pokemons(self, info, where=None, order_by=None, **kwargs):
        where = where or {}
        q = models.PokemonAbility.objects.filter(ability_id=self.pk)
        q = q.select_related("pokemon")
        q = AbilityPokemonWhere.apply(q, **where)
        q = AbilityPokemonSort.apply(q, order_by)

        page = get_page(q, AbilityPokemonConnection.__name__, **kwargs)
        edges = []
        for entry in page:
            edges.append(
                AbilityPokemonConnection.Edge(
                    node=entry.pokemon,
                    is_hidden=entry.is_hidden,
                    order=entry.slot,
                    cursor=page.get_cursor(entry),
                )
            )
        return AbilityPokemonConnection(
            edges=edges, page_info=page.page_info, total_count=page.total_count
        )


class AbilityEffect(base.BaseTranslation, interfaces=[i.Translation]):
    effect = g.String(
        name="text",
        description="The localized resource effect text in a specific language.",
    )
    short_effect = g.String(
        name="shortText", description="The localized effect text in brief."
    )


class AbilityEffectChange(g.ObjectType):
    pk = None
    effect_entries = base.TranslationList(
        lambda: AbilityChangeEffectText,
        description="The previous effect of this ability listed in different languages.",
        resolver=load_with_args("abilitychange_effectentries", using="pk"),
    )
    version_group_id = None
    version_group = g.Field(
        g.lazy_import("graphql_api.schema.version_group.types.VersionGroup"),
        description="The version group in which this effect changed. The effect change applies to version groups before this one.",
        resolver=load("versiongroup", using="version_group_id"),
    )


class AbilityChangeEffectText(base.BaseTranslation, interfaces=[i.Translation]):
    effect = g.String(
        name="text",
        description="The localized resource effect text in a specific language.",
    )


class AbilityFlavorText(base.BaseTranslation, interfaces=[i.Translation]):
    """The in-game description of an ability's effect."""

    flavor_text = g.String(
        name="text",
        description="The localized flavor text for a resource in a specific language.",
    )
    version_group_id = None
    version_group = g.Field(
        g.lazy_import("graphql_api.schema.version_group.types.VersionGroup"),
        description="The version group that uses this flavor text.",
        resolver=load("versiongroup", using="version_group_id"),
    )


class AbilityName(base.BaseTranslation, interfaces=[i.Translation]):
    name = g.String(
        name="text", description="The localized resource name in a specific language."
    )


class AbilityPokemonConnection(base.BaseConnection, g.relay.Connection, node=Pokemon):
    class Edge:
        is_hidden = g.Boolean(
            description="Whether or not this is a hidden ability for the referenced Pokémon. Hidden abilities are found on Pokémon from the Dream World and Dream Radar, as well as a few Pokémon from specific in-game encounters."
        )
        order = g.Int(
            description="The order in which a Pokémon's abilities should be sorted. Pokémon can have up to 3 different abilities."
        )


class AbilityPokemonSort(base.BaseSort):
    sort = g.InputField(
        g.Enum(
            "AbilityPokemonSortOptions", [("IS_HIDDEN", "is_hidden"), ("ORDER", "slot")]
        ),
        description="The field to sort by.",
    )


class AbilityPokemonWhere(base.BaseWhere):
    is_hidden = g.Boolean()
