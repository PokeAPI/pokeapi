import graphene as g
from pokemon_v2 import models
from . import types
from . import connection as conn
from ..base import BaseQuery
from ..utils import get_connection


class Query(BaseQuery):
    location = g.Field(types.Location, name=g.ID(required=True))
    locations = g.relay.ConnectionField(
        conn.LocationConnection,
        description="A list of locations that can be visited within games.",
        order_by=g.List(conn.LocationSort),
        where=g.Argument(conn.LocationWhere)
    )

    def resolve_location(self, info, name):
        return info.context.loaders.n_location.load(name)

    def resolve_locations(self, info, where=None, order_by=None, **kwargs):
        where = where or {}
        q = models.Location.objects.all()
        q = conn.LocationWhere.apply(q, **where)
        q = conn.LocationSort.apply(q, order_by)
        return get_connection(q, conn.LocationConnection, **kwargs)
