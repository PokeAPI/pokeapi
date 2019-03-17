import graphene as g
from pokemon_v2 import models
from graphql_api.utils import get_connection
from . import types
from . import connection as conn
from ..base import BaseQuery


class Query(BaseQuery):
    pokemon_form = g.Field(types.PokemonForm, id_name=g.ID(required=True))
    pokemon_forms = g.relay.ConnectionField(
        conn.PokemonFormConnection,
        description="A list of Pokémon varieties.",
        order_by=g.List(conn.PokemonFormSort),
        where=g.Argument(conn.PokemonFormWhere)
    )

    def resolve_pokemon_form(self, info, id_name):
        return info.context.loaders.n_pokemonform.load(id_name)

    def resolve_pokemon_forms(self, info, where=None, order_by=None, **kwargs):
        where = where or {}
        q = models.PokemonForm.objects.all()
        q = conn.PokemonFormWhere.apply(q, **where)
        q, order_by = conn.PokemonFormSort.apply(q, order_by)
        return get_connection(q, order_by, conn.PokemonFormConnection, **kwargs)
