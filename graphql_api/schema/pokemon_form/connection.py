import graphene as g
from pokemon_v2 import models
from .. import base
from . import types  # pylint: disable=unused-import
from ...utils import text_annotate


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
    version_group__name = g.List(g.ID, name="versionGroup__idName")


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
    def apply(cls, query_set, order_by, prefix=""):
        order_by = order_by or []
        order_by2 = []
        for o in order_by:
            if o.field == prefix + "__name_annotation":
                query_set, o.field = text_annotate(
                    query_set,
                    lang=o.lang,
                    model=models.PokemonFormName,
                    id_attr="pokemon_form_id",
                    text_resource="name",
                    prefix=prefix,
                )
                order_by2.append(o)
            else:
                order_by2.append(o)

        return super().apply(query_set, order_by2)
