import graphene as g
from pokemon_v2 import models
from graphql_api.utils import get_connection
from . import types  # pylint: disable=unused-import
from . import connection as conn
from ..base import BaseQuery


class Query(BaseQuery):
    type = g.Field(types.Type, id_name=g.ID(required=True))
    types = g.relay.ConnectionField(
        conn.TypeConnection,
        description="A list of types Pokémon and moves can have.",
        order_by=g.List(conn.TypeSort),
        where=g.Argument(conn.TypeWhere)
    )

    def resolve_type(self, info, id_name):
        return info.context.loaders.n_type.load(id_name)

    def resolve_types(self, info, where=None, order_by=None, **kwargs):
        where = where or {}
        q = models.Type.objects.all()
        q = conn.TypeWhere.apply(q, **where)
        q, order_by = conn.TypeSort.apply(q, order_by)
        return get_connection(q, order_by, conn.TypeConnection, **kwargs)
