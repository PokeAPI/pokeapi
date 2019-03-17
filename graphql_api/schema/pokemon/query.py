import graphene as g
from pokemon_v2 import models
from graphql_api.utils import get_connection
from . import types
from .sort import PokemonSort
from .where import PokemonWhere
from ..base import BaseQuery


class Query(BaseQuery):
    pokemon = g.Field(types.Pokemon, id_name=g.ID(required=True))
    pokemons = g.relay.ConnectionField(
        types.PokemonConnection,
        description="A list of Pokémon.",
        order_by=g.List(PokemonSort),
        where=g.Argument(PokemonWhere),
    )

    def resolve_pokemon(self, info, id_name):
        return info.context.loaders.n_pokemon.load(id_name)

    def resolve_pokemons(self, info, where=None, order_by=None, **kwargs):
        where = where or {}
        q = models.Pokemon.objects.all()
        q = PokemonWhere.apply(q, **where)
        q, order_by = PokemonSort.apply(q, order_by)
        return get_connection(q, order_by, types.PokemonConnection, **kwargs)
