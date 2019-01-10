import graphene as g
from pokemon_v2 import models
from graphql_api.utils import get_connection
from . import types
from . import connection as conn
from ..base import BaseQuery


class Query(BaseQuery):
    pokemon = g.Field(types.Pokemon, id_name=g.ID(required=True))
    pokemons = g.relay.ConnectionField(
        conn.PokemonConnection,
        description="A list of Pokémon.",
        order_by=g.List(conn.PokemonSort),
        where=g.Argument(conn.PokemonWhere)
    )

    def resolve_pokemon(self, info, id_name):
        return info.context.loaders.n_pokemon.load(id_name)

    def resolve_pokemons(self, info, where=None, order_by=None, **kwargs):
        where = where or {}
        q = models.Pokemon.objects.all()
        q = conn.PokemonWhere.apply(q, **where)
        q = conn.PokemonSort.apply(q, order_by)
        return get_connection(q, conn.PokemonConnection, **kwargs)
