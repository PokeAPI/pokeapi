import graphene as g
from django.db.models import OuterRef, Subquery
from pokemon_v2 import models
from .. import base
from . import types  # pylint: disable=unused-import


class AbilityConnection(g.relay.Connection, base.BaseConnection, node=types.Ability):
    pass


class AbilityWhere(base.BaseWhere):
    name = g.Argument(base.TextSearch)
    is_main_series = g.Boolean()

    @classmethod
    def apply(cls, query_set, name=None, **where):
        if name:
            query_set = cls.text_filter(query_set, name, "generationname", "name")

        return super().apply(query_set, **where)


class AbilitySort(base.BaseSort):
    field = g.InputField(
        g.Enum("AbilitySortOptions", [("NAME", "name_annotation")]),
        description="The field to sort by.",
    )

    @classmethod
    def apply(cls, query_set, order_by):
        order_by = order_by or []
        for o in order_by:
            if o.field == "name_annotation":
                cls.check_lang(o)
                # Add an annotation with the name to sort by
                subquery = models.AbilityName.objects.filter(
                    ability_id=OuterRef("pk"), language__name=o.lang
                )
                query_set = query_set.annotate(
                    name_annotation=Subquery(subquery.values("name")[:1])
                )

        return super().apply(query_set, order_by)
