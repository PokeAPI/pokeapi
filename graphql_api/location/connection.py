import graphene as g
from django.db.models import OuterRef, Subquery
from pokemon_v2 import models
from .. import base
from .types import Location  # pylint: disable=unused-import


class LocationConnection(g.relay.Connection, base.BaseConnection, node=Location):
    pass


class LocationWhere(base.BaseWhere):
    name = g.Argument(base.TextSearch)

    @classmethod
    def apply(cls, query_set, name=None, **where):
        if name:
            query_set = cls.text_filter(query_set, name, "locationname", "name")

        return super().apply(query_set, **where)


class LocationSort(base.BaseSort):
    field = g.InputField(
        g.Enum(
            "LocationSortOptions",
            [("REGION", "region__id"), ("NAME", "name_annotation")],
        ),
        description="The field to sort by.",
    )

    @classmethod
    def apply(cls, query_set, order_by):
        order_by = order_by or []
        for o in order_by:
            if o.field == "name_annotation":
                cls.check_lang(o)
                # Add an annotation with the name to sort by
                subquery = models.LocationName.objects.filter(
                    location_id=OuterRef("pk"), language__name=o["lang"]
                )
                query_set = query_set.annotate(
                    name_annotation=Subquery(subquery.values("name")[:1])
                )

        return super().apply(query_set, order_by)
