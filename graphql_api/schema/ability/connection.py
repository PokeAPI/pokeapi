import graphene as g
from pokemon_v2 import models
from .. import base
from . import types  # pylint: disable=unused-import
from ...utils import text_annotate


class AbilityConnection(g.relay.Connection, base.BaseConnection, node=types.Ability):
    pass


class AbilityWhere(base.BaseWhere):
    abilityname__name = g.Argument(base.TextFilter, name="name")
    is_main_series = g.Boolean()


class AbilitySort(base.BaseSort):
    field = g.InputField(
        g.Enum("AbilitySortOptions", [("NAME", "name_annotation")]),
        description="The field to sort by.",
    )

    @classmethod
    def apply(cls, query_set, order_by, prefix=""):
        order_by = order_by or []
        order_by2 = []
        for o in order_by:
            if o.field == prefix + "__name_annotation":
                query_set, o.field = text_annotate(
                    query_set,
                    lang=o.lang,
                    model=models.AbilityName,
                    id_attr="ability_id",
                    text_resource="name",
                    prefix=prefix,
                )
                order_by2.append(o)
            else:
                order_by2.append(o)

        return super().apply(query_set, order_by2)