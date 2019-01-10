import graphene as g
from pokemon_v2 import models
from graphql_api.utils import get_connection
from . import types
from . import connection as conn
from ..base import BaseQuery


class Query(BaseQuery):
    pokemon_species = g.Field(types.PokemonSpecies, id_name=g.ID(required=True))
    pokemon_speciess = g.relay.ConnectionField(
        conn.PokemonSpeciesConnection,
        description="A list of Pokémon species.",
        order_by=g.List(conn.PokemonSpeciesSort),
        where=g.Argument(conn.PokemonSpeciesWhere),
    )

    def resolve_pokemon_species(self, info, id_name):
        return info.context.loaders.n_pokemonspecies.load(id_name)

    def resolve_pokemon_speciess(self, info, where=None, order_by=None, **kwargs):
        where = where or {}
        q = models.PokemonSpecies.objects.all()
        q = conn.PokemonSpeciesWhere.apply(q, **where)
        q = conn.PokemonSpeciesSort.apply(q, order_by)
        return get_connection(q, conn.PokemonSpeciesConnection, **kwargs)
