import graphene as g
from pokemon_v2 import models
from .. import base
from ..pokemon_color import sort as color
from ...utils import text_annotate, add_prefix


sort_options = [
    ("baseHappiness", "base_happiness"),
    ("captureRate", "capture_rate"),
    ("genderRate", "gender_rate"),
    ("hasGenderDifferences", "has_gender_differences"),
    ("hatchCounter", "hatch_counter"),
    ("isBaby", "is_baby"),
    ("isFormsSwitchable", "forms_switchable"),
    ("order", "order"),
    ("name", "name_annotation"),
] + add_prefix(color.sort_options, "color", "pokemon_color")


class PokemonSpeciesSort(base.BaseSort):
    field = g.InputField(
        g.Enum("PokemonSpeciesSortOptions", sort_options),
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
                    model=models.PokemonSpeciesName,
                    id_attr="pokemon_species_id",
                    text_resource="name",
                    prefix=prefix,
                )
                order_by2.append(o)
            elif o.field.startswith("pokemon_color"):
                query_set, o2 = color.PokemonColorSort.apply(
                    query_set, [o], "pokemon_color"
                )
                # query_set = query_set.prefetch_related("pokemon_color")
                order_by2.extend(o2)
            else:
                order_by2.append(o)

        return super().apply(query_set, order_by2)
