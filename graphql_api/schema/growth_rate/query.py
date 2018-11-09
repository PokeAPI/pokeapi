import graphene as g
from pokemon_v2 import models
from . import types
from ..base import BaseQuery


class Query(BaseQuery):
    growth_rate = g.Field(types.GrowthRate, name=g.ID(required=True))
    growth_rates = g.List(
        types.GrowthRate,
        description="A list of growth rates at which Pokémon can gain levels through experience.",
    )

    def resolve_growth_rate(self, info, name):
        return info.context.loaders.n_growthrate.load(name)

    def resolve_growth_rates(self, info):
        return models.GrowthRate.objects.all()
