import graphene as g
from django.db.models import OuterRef, Subquery
from pokemon_v2 import models
from .. import base
from . import types  # pylint: disable=unused-import


class PokemonConnection(g.relay.Connection, base.BaseConnection, node=types.Pokemon):
    pass


class PokemonWhere(base.BaseWhere):
    name = g.Argument(base.TextSearch)

    @classmethod
    def apply(cls, query_set, name=None, **where):
        # Unfortunately, Pokemon doesn't have a 'names' property,
        # so searching against the 'name' property will have to do.
        if name:
            if name.case_sensitive:
                query_set = query_set.filter(name__contains=name.query)
            else:
                query_set = query_set.filter(name__icontains=name.query)

        return super().apply(query_set, **where)


class PokemonSort(base.BaseSort):
    field = g.InputField(
        g.Enum(
            "PokemonSortOptions",
            [
                ("ORDER", "order"),
                ("HEIGHT", "height"),
                ("IS_DEFAULT", "is_default"),
                ("WEIGHT", "weight"),
                ("NAME", "name"),
            ],
        ),
        description="The field to sort by.",
    )

    # @classmethod
    # def apply(cls, query_set, order_by):
    #     order_by = order_by or []
    #     for o in order_by:
    #         if o.field == "name_annotation":
    #             cls.check_lang(o)
    #             # Add an annotation with the name to sort by
    #             subquery = models.PokemonName.objects.filter(
    #                 location_area_id=OuterRef("pk"), language__name=o.lang
    #             )
    #             query_set = query_set.annotate(
    #                 name_annotation=Subquery(subquery.values("name")[:1])
    #             )

    #     return super().apply(query_set, order_by)
