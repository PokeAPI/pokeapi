import graphene as g
from pokemon_v2 import models
from graphql_api.utils import get_connection
from . import types
from . import connection as conn
from ..base import BaseQuery


class Query(BaseQuery):
    encounter = g.Field(types.Encounter, id_name=g.ID(required=True))
    encounters = g.relay.ConnectionField(
        conn.EncounterConnection,
        description="A list of situations in which a player might encounter Pokémon in the wild.",
        order_by=g.List(conn.EncounterSort),
        where=g.Argument(conn.EncounterWhere),
    )

    def resolve_encounter(self, info, id_name):
        return info.context.loaders.encounter.load(id_name)

    def resolve_encounters(self, info, where=None, order_by=None, **kwargs):
        where = where or {}
        q = models.Encounter.objects.all().select_related("encounter_slot")
        q = conn.EncounterWhere.apply(q, **where)
        q = conn.EncounterSort.apply(q, order_by)
        return get_connection(q, conn.EncounterConnection, **kwargs)
