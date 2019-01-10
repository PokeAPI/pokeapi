import graphene as g
from pokemon_v2 import models
from . import types
from ..base import BaseQuery


class Query(BaseQuery):
    nature = g.Field(types.Nature, id_name=g.ID(required=True))
    natures = g.List(
        types.Nature,
        description="A list of natures that influence how a Pokémon's natures grow.",
    )

    def resolve_nature(self, info, id_name):
        return info.context.loaders.n_nature.load(id_name)

    def resolve_natures(self, info):
        return models.Nature.objects.all()
