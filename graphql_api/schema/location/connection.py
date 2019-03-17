import graphene as g
from pokemon_v2 import models
from .types import Location  # pylint: disable=unused-import
from .. import base
from ...utils import text_annotate


class LocationConnection(g.relay.Connection, base.BaseConnection, node=Location):
    pass


class LocationWhere(base.BaseWhere):
    locationname__name = g.Argument(base.TextFilter, name="name")
    region__name = g.List(g.ID, name="region__idName")


class LocationSort(base.BaseSort):
    field = g.InputField(
        g.Enum(
            "LocationSortOptions",
            [("REGION", "region__id"), ("NAME", "name_annotation")],
        ),
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
                    model=models.LocationName,
                    id_attr="location_id",
                    text_resource="name",
                    prefix=prefix,
                )
                order_by2.append(o)
            else:
                order_by2.append(o)

        return super().apply(query_set, order_by2)
