import graphene as g
from pokemon_v2 import models
from . import types
from ..base import BaseQuery


class Query(BaseQuery):
    pokemon_shape = g.Field(types.PokemonShape, name=g.ID(required=True))
    pokemon_shapes = g.List(
        types.PokemonShape,
        description="A list of shapes that Pokémon can be found in (e.g. cave).",
    )

    def resolve_pokemon_shape(self, info, name):
        return info.context.loaders.n_pokemonshape.load(name)

    def resolve_pokemon_shapes(self, info):
        return models.PokemonShape.objects.all()
