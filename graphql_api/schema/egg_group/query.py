import graphene as g
from pokemon_v2 import models
from . import types
from ..base import BaseQuery


class Query(BaseQuery):
    egg_group = g.Field(types.EggGroup, id_name=g.ID(required=True))
    egg_groups = g.List(
        types.EggGroup,
        description="A list of egg groups, which are categories that determine which Pokémon are able to interbreed.",
    )

    def resolve_egg_group(self, info, id_name):
        return info.context.loaders.n_egggroup.load(id_name)

    def resolve_egg_groups(self, info):
        return models.EggGroup.objects.all()
