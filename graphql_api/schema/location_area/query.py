import graphene as g
from pokemon_v2 import models
from graphql_api.utils import get_connection
from . import types
from . import connection as conn
from ..base import BaseQuery


class Query(BaseQuery):
    location_area = g.Field(types.LocationArea, name=g.ID(required=True))
    location_areas = g.relay.ConnectionField(
        conn.LocationAreaConnection,
        description="A list of locations that can be visited within games.",
        order_by=g.List(conn.LocationAreaSort),
        where=g.Argument(conn.LocationAreaWhere)
    )

    def resolve_location_area(self, info, name):
        return info.context.loaders.n_locationarea.load(name)

    def resolve_location_areas(self, info, where=None, order_by=None, **kwargs):
        where = where or {}
        q = models.LocationArea.objects.all()
        q = conn.LocationAreaWhere.apply(q, **where)
        q = conn.LocationAreaSort.apply(q, order_by)
        return get_connection(q, conn.LocationAreaConnection, **kwargs)
