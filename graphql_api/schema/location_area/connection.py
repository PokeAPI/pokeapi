import graphene as g
from pokemon_v2 import models
from .. import base
from . import types  # pylint: disable=unused-import
from ...utils import text_annotate


class LocationAreaConnection(
    g.relay.Connection, base.BaseConnection, node=types.LocationArea
):
    pass


class LocationAreaWhere(base.BaseWhere):
    locationareaname__name = g.Argument(base.TextFilter, name="name")
    location__name = g.List(g.ID, name="location__idName")


class LocationAreaSort(base.BaseSort):
    field = g.InputField(
        g.Enum("LocationAreaSortOptions", [("NAME", "name_annotation")]),
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
                    model=models.LocationAreaName,
                    id_attr="location_area_id",
                    text_resource="name",
                    prefix=prefix,
                )
                order_by2.append(o)
            else:
                order_by2.append(o)

        return super().apply(query_set, order_by2)
