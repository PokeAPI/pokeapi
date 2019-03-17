import graphene as g
from .. import base
from ..pokemon_species.where import PokemonSpeciesWhere


class PokemonWhere(base.BaseWhere):
    base_experience = g.Argument(base.IntFilter)
    height = g.Argument(base.IntFilter)
    is_default = g.Boolean()
    species = g.Argument(PokemonSpeciesWhere)
    pokemontype__type__name = g.Argument(base.ListFilter, name="types")
    weight = g.Argument(base.IntFilter)

    @classmethod
    def apply(cls, qs, prefix="", species=None, weight=None, **where):
        if species:
            qs = PokemonSpeciesWhere.apply(
                qs, **species, prefix=prefix + "pokemon_species__"
            )
        if weight:
            filters = {
                prefix + "weight__" + operator: value * 10
                for operator, value in weight.items()
                if value is not None
            }
            qs = qs.filter(**filters)

        return super().apply(qs, **where, prefix=prefix)
