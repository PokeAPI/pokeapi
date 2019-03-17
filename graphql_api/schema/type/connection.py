import graphene as g
from pokemon_v2 import models
from .. import base
from . import types  # pylint: disable=unused-import
from ...utils import text_annotate


class TypeConnection(g.relay.Connection, base.BaseConnection, node=types.Type):
    pass


class TypeWhere(base.BaseWhere):
    typename__name = g.Argument(base.TextFilter, name="name")


class TypeSort(base.BaseSort):
    field = g.InputField(
        g.Enum("TypeSortOptions", [("NAME", "name_annotation")]),
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
                    model=models.TypeName,
                    id_attr="type_id",
                    text_resource="name",
                    prefix=prefix,
                )
                order_by2.append(o)
            else:
                order_by2.append(o)

        return super().apply(query_set, order_by2)
