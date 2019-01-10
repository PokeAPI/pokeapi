import graphene as g
from pokemon_v2 import models
from . import types
from ..base import BaseQuery


class Query(BaseQuery):
    pokedex = g.Field(types.Pokedex, id_name=g.ID(required=True))
    pokedexes = g.List(
        types.Pokedex,
        description="A list of handheld devices that store information about Pokémon.",
        is_main_series=g.Boolean()
    )

    def resolve_pokedex(self, info, id_name):
        return info.context.loaders.n_pokedex.load(id_name)

    def resolve_pokedexes(self, info, is_main_series=None):
        q = models.Pokedex.objects.all()
        if is_main_series is not None:
            q = q.filter(is_main_series=is_main_series)
        return q
