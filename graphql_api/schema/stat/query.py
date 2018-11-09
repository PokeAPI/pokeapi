import graphene as g
from pokemon_v2 import models
from . import types
from ..base import BaseQuery


class Query(BaseQuery):
    stat = g.Field(types.Stat, name=g.ID(required=True))
    stats = g.List(
        types.Stat,
        description="A list of stats that determine certain aspects of battle.",
    )

    def resolve_stat(self, info, name):
        return info.context.loaders.n_stat.load(name)

    def resolve_stats(self, info):
        return models.Stat.objects.all()
