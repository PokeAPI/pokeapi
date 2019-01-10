import graphene as g
from pokemon_v2 import models
from graphql_api.utils import get_connection
from . import types
from . import connection as conn
from ..base import BaseQuery


class Query(BaseQuery):
    ability = g.Field(types.Ability, id_name=g.ID(required=True))
    abilities = g.relay.ConnectionField(
        conn.AbilityConnection,
        description="A list of abilities Pokémon can have.",
        order_by=g.List(conn.AbilitySort),
        where=g.Argument(conn.AbilityWhere),
    )

    def resolve_ability(self, info, id_name):
        return info.context.loaders.n_ability.load(id_name)

    def resolve_abilities(self, info, where=None, order_by=None, **kwargs):
        where = where or {}
        q = models.Ability.objects.all()
        q = conn.AbilityWhere.apply(q, **where)
        q = conn.AbilitySort.apply(q, order_by)
        return get_connection(q, conn.AbilityConnection, **kwargs)
