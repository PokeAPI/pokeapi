import graphene as g
from pokemon_v2 import models
from .. import base
from ...utils import text_annotate


sort_options = [("name", "name_annotation")]


class PokemonColorSort(base.BaseSort):
    field = g.InputField(
        g.Enum("PokemonColorSortOptions", sort_options),
        description="The field to sort by.",
    )

    @classmethod
    def apply(cls, query_set, order_by, prefix=""):
        order_by = order_by or []
        order_by2 = []
        for o in order_by:
            if o.field == prefix + "name_annotation":
                query_set, o.field = text_annotate(
                    query_set,
                    lang=o.lang,
                    model=models.PokemonColorName,
                    id_attr="pokemon_color_id",
                    text_resource="name",
                    prefix=prefix,
                )
                order_by2.append(o)
            else:
                order_by2.append(o)

        return super().apply(query_set, order_by2)
