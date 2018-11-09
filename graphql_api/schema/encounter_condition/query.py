import graphene as g
from pokemon_v2 import models
from . import types
from ..base import BaseQuery


class Query(BaseQuery):
    encounter_condition = g.Field(types.EncounterCondition, name=g.ID(required=True))
    encounter_conditions = g.List(
        types.EncounterCondition,
        description="A list of conditions which affect what Pokémon might appear in the wild.",
    )

    def resolve_encounter_condition(self, info, name):
        return info.context.loaders.n_encountercondition.load(name)

    def resolve_encounter_conditions(self, info):
        return models.EncounterCondition.objects.all()
