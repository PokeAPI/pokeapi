import graphene as g
from django.db.models import OuterRef, Subquery
from pokemon_v2 import models
from .. import base
from . import types  # pylint: disable=unused-import


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
    def apply(cls, query_set, order_by):
        order_by = order_by or []
        for o in order_by:
            if o.field == "name_annotation":
                cls.check_lang(o)
                # Add an annotation with the name to sort by
                subquery = models.TypeName.objects.filter(
                    type_id=OuterRef("pk"), language__name=o.lang
                )
                query_set = query_set.annotate(
                    name_annotation=Subquery(subquery.values("name")[:1])
                )

        return super().apply(query_set, order_by)
