import graphene as g
from pokemon_v2 import models
from . import types
from ..base import BaseQuery


class Query(BaseQuery):
    encounter_method = g.Field(types.EncounterMethod, name=g.ID(required=True))
    encounter_methods = g.List(
        types.EncounterMethod,
        description="A list of methods by which a player might encounter Pokémon in the wild.",
    )

    def resolve_encounter_method(self, info, name):
        return info.context.loaders.n_encountermethod.load(name)

    def resolve_encounter_methods(self, info):
        return models.EncounterMethod.objects.all()
