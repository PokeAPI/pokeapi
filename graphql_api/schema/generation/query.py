import graphene as g
from pokemon_v2 import models
from graphql_api.utils import get_connection
from . import types
from . import connection as conn
from ..base import BaseQuery


class Query(BaseQuery):
    generation = g.Field(types.Generation, name=g.ID(required=True))
    generations = g.relay.ConnectionField(
        conn.GenerationConnection,
        description="A list of generations (groupings of games based on the Pokémon they include).",
        order_by=g.List(conn.GenerationSort),
        where=g.Argument(conn.GenerationWhere),
    )

    def resolve_generation(self, info, name):
        return info.context.loaders.n_generation.load(name)

    def resolve_generations(self, info, where=None, order_by=None, **kwargs):
        where = where or {}
        q = models.Generation.objects.all()
        q = conn.GenerationWhere.apply(q, **where)
        q = conn.GenerationSort.apply(q, order_by)
        return get_connection(q, conn.GenerationConnection, **kwargs)
