import graphene as g
from pokemon_v2 import models
from . import types
from ..base import BaseQuery


class Query(BaseQuery):
    encounter_method = g.Field(types.EncounterMethod, id_name=g.ID(required=True))
    encounter_methods = g.List(
        types.EncounterMethod,
        description="A list of methods by which a player might encounter Pokémon in the wild.",
    )

    def resolve_encounter_method(self, info, id_name):
        return info.context.loaders.n_encountermethod.load(id_name)

    def resolve_encounter_methods(self, info):
        return models.EncounterMethod.objects.all()
