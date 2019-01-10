import graphene as g
from pokemon_v2 import models
from . import types
from ..base import BaseQuery


class Query(BaseQuery):
    pokemon_color = g.Field(types.PokemonColor, id_name=g.ID(required=True))
    pokemon_colors = g.List(
        types.PokemonColor,
        description="A list of colors used for sorting Pokémon in a Pokédex.",
    )

    def resolve_pokemon_color(self, info, id_name):
        return info.context.loaders.n_pokemoncolor.load(id_name)

    def resolve_pokemon_colors(self, info):
        return models.PokemonColor.objects.all()
