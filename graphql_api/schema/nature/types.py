import graphene as g
from graphql_api.utils import load, load_with_args
from .. import interfaces as i  # pylint: disable=unused-import
from .. import base


class Nature(g.ObjectType):
    """
    Natures influence how a Pokémon's stats grow. See [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Nature) for greater detail.
    """

    pk = None
    decreased_stat_id = None
    decreased_stat = g.Field(
        g.lazy_import("graphql_api.schema.stat.types.Stat"),
        description="The stat decreased by 10% in Pokémon with this nature.",
        resolver=load("stat", using="decreased_stat_id"),
    )
    increased_stat_id = None
    increased_stat = g.Field(
        g.lazy_import("graphql_api.schema.stat.types.Stat"),
        description="The stat increased by 10% in Pokémon with this nature.",
        resolver=load("stat", using="increased_stat_id"),
    )
    # hates_flavor_id = None
    # hates_flavor = g.Field(
    #     lazy_import("pokemon_graphql.berry_flavor.types.BerryFlavor"),
    #     description="The berry flavour hated by Pokémon with this nature.",
    #     resolver=load("berryflavor", using="hates_flavor_id"),
    # )
    # likes_flavor_id = None
    # likes_flavor = g.Field(
    #     lazy_import("pokemon_graphql.berry_flavor.types.BerryFlavor"),
    #     description="The berry flavour liked by Pokémon with this nature."
    #     resolver=load("berryflavor", using="likes_flavor_id"),
    # )
    move_battle_style_preferences = g.List(
        lambda: MoveBattleStylePreference,
        description="A list of battle styles and how likely a Pokémon with this nature is to use them in the Battle Palace or Battle Tent.",
        resolver=load("nature_battlestylepreferences", using="pk"),
    )
    name = g.ID(name="idName", description="The name of this resource.")
    names = base.TranslationList(
        lambda: NatureName,
        description="The name of this resource listed in different languages.",
        resolver=load_with_args("nature_names", using="pk"),
    )
    pokeathlon_stat_changes = g.List(
        lambda: NatureStatChange,
        description="A list of Pokéathlon stats this nature effects and how much it effects them.",
        resolver=load("nature_pokeathlonstats", using="pk"),
    )


class MoveBattleStylePreference(g.ObjectType):
    low_hp_preference = g.Int(
        name="lowHPPreference",
        description="Chance of using the move, in percent, if HP is under one half.",
    )
    high_hp_preference = g.Int(
        name="highHPPreference",
        description="Chance of using the move, in percent, if HP is over one half.",
    )
    move_battle_style_id = None
    # move_battle_style = g.Field(
    #     g.lazy_import("graphql_api.schema.move_battle_style.types.MoveBattleStyle"),
    #     description="The move battle style.",
    #     resolver=load("movebattlestyle", using="move_battle_style_id"),
    # )


class NatureName(base.BaseTranslation, interfaces=[i.Translation]):
    name = g.String(
        name="text", description="The localized resource name in a specific language."
    )


class NatureStatChange(g.ObjectType):
    max_change = g.Int(description="The amount of change.")
    pokeathlon_stat_id = None
    # pokeathlon_stat = g.Field(
    #     g.lazy_import("graphql_api.schema.pokeathlon_stat.types.PokeathlonStat"),
    #     description="The stat being affected.",
    #     resolver=load("pokeathlonstat", using="pokeathlon_stat_id"),
    # )
