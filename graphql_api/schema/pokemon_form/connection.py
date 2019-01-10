import graphene as g
from django.db.models import OuterRef, Subquery
from pokemon_v2 import models
from .. import base
from . import types  # pylint: disable=unused-import


class PokemonFormConnection(
    g.relay.Connection, base.BaseConnection, node=types.PokemonForm
):
    pass


class PokemonFormWhere(base.BaseWhere):
    is_battle_only = g.Boolean()
    is_default = g.Boolean()
    is_mega = g.Boolean()
    pokemonformname__name = g.Argument(base.TextFilter, name="name")
    version_group = g.ID()
    version_group__name = g.List(g.ID, name="versionGroup_idName")


class PokemonFormSort(base.BaseSort):
    field = g.InputField(
        g.Enum(
            "PokemonFormSortOptions",
            [
                ("ORDER", "order"),
                ("FORM_ORDER", "form_order"),
                ("IS_DEFAULT", "is_default"),
                ("IS_BATTLE_ONLY", "is_battle_only"),
                ("IS_MEGA", "is_mega"),
                ("NAME", "name_annotation"),
            ],
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
                subquery = models.PokemonFormName.objects.filter(
                    pokemon_form_id=OuterRef("pk"), language__name=o.lang
                )
                query_set = query_set.annotate(
                    name_annotation=Subquery(subquery.values("name")[:1])
                )

        return super().apply(query_set, order_by)
