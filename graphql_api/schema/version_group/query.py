import graphene as g
from pokemon_v2 import models
from . import types
from ..base import BaseQuery


class Query(BaseQuery):
    version_group = g.Field(types.VersionGroup, id_name=g.ID(required=True))
    version_groups = g.List(
        types.VersionGroup,
        description="A list of highly similar versions of the games.",
    )

    def resolve_version_group(self, info, id_name):
        return info.context.loaders.n_versiongroup.load(id_name)

    def resolve_version_groups(self, info):
        return models.VersionGroup.objects.all()
