import graphene as g
from .. import base
from ..pokemon_species import sort as species
from ...utils import add_prefix


sort_options = [
    ("order", "order"),
    ("height", "height"),
    ("isDefault", "is_default"),
    ("weight", "weight"),
] + add_prefix(species.sort_options, "species", "pokemon_species")


class PokemonSort(base.BaseSort):
    field = g.InputField(
        g.Enum("PokemonSortOptions", sort_options), description="The field to sort by."
    )

    @classmethod
    def apply(cls, query_set, order_by):
        order_by = order_by or []
        order_by2 = []
        for o in order_by:
            if o.field.startswith("pokemon_species"):
                query_set, o2 = species.PokemonSpeciesSort.apply(
                    query_set, [o], "pokemon_species"
                )
                query_set = query_set.prefetch_related("pokemon_species")
                order_by2.extend(o2)
            else:
                order_by2.append(o)

        return super().apply(query_set, order_by2)
