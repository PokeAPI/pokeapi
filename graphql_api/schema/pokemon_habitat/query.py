import graphene as g
from pokemon_v2 import models
from . import types
from ..base import BaseQuery


class Query(BaseQuery):
    pokemon_habitat = g.Field(types.PokemonHabitat, name=g.ID(required=True))
    pokemon_habitats = g.List(
        types.PokemonHabitat,
        description="A list of habitats that Pokémon can be found in (e.g. cave).",
    )

    def resolve_pokemon_habitat(self, info, name):
        return info.context.loaders.n_pokemonhabitat.load(name)

    def resolve_pokemon_habitats(self, info):
        return models.PokemonHabitat.objects.all()
