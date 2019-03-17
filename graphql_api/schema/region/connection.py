import graphene as g
from pokemon_v2 import models
from .. import base
from . import types  # pylint: disable=unused-import
from ...utils import text_annotate


class RegionConnection(g.relay.Connection, base.BaseConnection, node=types.Region):
    pass


class RegionWhere(base.BaseWhere):
    regionname__name = g.Argument(base.TextFilter, name="name")


class RegionSort(base.BaseSort):
    field = g.InputField(
        g.Enum("RegionSortOptions", [("NAME", "name_annotation")]),
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
                    model=models.RegionName,
                    id_attr="region_id",
                    text_resource="name",
                    prefix=prefix,
                )
                order_by2.append(o)
            else:
                order_by2.append(o)

        return super().apply(query_set, order_by2)
