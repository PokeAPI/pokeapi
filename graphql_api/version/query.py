import graphene as g
from pokemon_v2 import models
from . import types
from ..base import BaseQuery


class Query(BaseQuery):
    version = g.Field(types.Version, name=g.ID(required=True))
    versions = g.List(
        types.Version,
        description="A list of versions of the games, e.g., Red, Blue or Yellow.",
    )

    def resolve_version(self, info, name):
        return info.context.loaders.n_version.load(name)

    def resolve_versions(self, info):
        return models.Version.objects.all()
