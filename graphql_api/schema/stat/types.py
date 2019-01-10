import graphene as g
# from pokemon_v2 import models
from graphql_api.utils import load, load_with_args  #, get_page
# from ..move.types import Move
from .. import interfaces as i  # pylint: disable=unused-import
from .. import base


class Stat(g.ObjectType):
    """
    Stats determine certain aspects of battles. Each Pokémon has a value for each stat which grows as they gain levels and can be altered momentarily by effects in battles.
    """

    pk = None
    # affecting_moves = g.relay.ConnectionField(
    #     lambda: StatAffectMoveConnection,
    #     description="A list of moves which affect this stat.",
    #     where=g.Argument(lambda: StatAffectMoveWhere),
    #     order_by=g.List(lambda: StatAffectMoveSort)
    # )
    characteristics = g.List(
        g.lazy_import("graphql_api.schema.characteristic.types.Characteristic"),
        description="A list of characteristics that are set on a Pokémon when its highest base stat is this stat.",
        resolver=load("stat_characteristics", using="pk"),
    )
    game_index = g.Int(description="ID the games use for this stat.")
    is_battle_only = g.Boolean(
        description="Whether this stat only exists within a battle."
    )
    move_damage_class_id = None
    # move_damage_class = g.Field(
    #     g.lazy_import("graphql_api.schema.move_damage_class.types.MoveDamageClass"),
    #     description="The class of damage this stat is directly related to.",
    #     resolver=load("movedamageclass", using="move_damage_class_id"),
    # )
    name = g.ID(name="idName", description="The name of this resource.")
    names = base.TranslationList(
        lambda: StatName,
        description="The name of this resource listed in different languages.",
        resolver=load_with_args("stat_names", using="pk"),
    )
    negative_affecting_natures = g.List(
        g.lazy_import("graphql_api.schema.nature.types.Nature"),
        description="A list of natures which affect this stat negatively.",
        resolver=load("decreasedstat_natures", using="pk"),
    )
    positive_affecting_natures = g.List(
        g.lazy_import("graphql_api.schema.nature.types.Nature"),
        description="A list of natures which affect this stat positively.",
        resolver=load("increasedstat_natures", using="pk"),
    )

    # def resolve_affecting_moves(self, info, **kwargs):
    #     q = models.MoveMetaStatChange.objects.filter(stat_id=self.pk)
    #     q = q.select_related("move")
    #     q = StatAffectMoveWhere.apply(q, **kwargs.get("where", {}))

    #     page = get_page(q, StatAffectMoveConnection.__name__, **kwargs)
    #     return StatAffectMoveConnection(
    #         edges=[
    #             StatAffectMoveConnection.Edge(
    #                 node=entry.move,
    #                 change=entry.change,
    #                 cursor=page.get_cursor(entry),
    #             ) for entry in page
    #         ],
    #         page_info=page.page_info,
    #         total_count=page.total_count,
    #     )


class StatName(base.BaseTranslation, interfaces=[i.Translation]):
    name = g.String(
        name="text", description="The localized resource name in a specific language."
    )


# class StatAffectMoveConnection(base.BaseConnection, g.relay.Connection, node=Move):
#     class Edge:
#         change = g.Int(
#             description="The maximum amount of change to the referenced stat."
#         )


class StatAffectMoveSort(base.BaseSort):
    field = g.InputField(
        g.Enum("StatPokemonSortOptions", [("CHANGE", "change")]),
        description="The field to sort by.",
    )

class StatAffectMoveWhere(base.BaseWhere):
    """Filtering options for stat affect move connections. To include only moves with a positive stat change, set `change_gt` to `0`. You can create separate queries for positive and negative stat changes using [aliases](https://graphql.org/learn/queries/#aliases)."""

    change__gt = g.Int(
        name="change_gt",
        description="Only include moves that have a stat change greater than _x_."
    )
    change__lt = g.Int(
        name="change_lt",
        description="Only include moves that have a stat change less than _x_."
    )
