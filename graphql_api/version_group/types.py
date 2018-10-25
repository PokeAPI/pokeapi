import graphene as g
from ..loader_key import LoaderKey

class VersionGroup(g.ObjectType):
    """Versions of the games, e.g., Red, Blue or Yellow."""

    pk = None
    generation_id = None
    generation = g.Field(
        g.lazy_import("graphql_api.generation.types.Generation"),
        description="The generation this version was introduced in.",
    )
    name = g.ID(description="The name of this resource.")
    order = g.Int(
        description="Order for sorting. Almost by date of release, except similar versions are grouped together."
    )
    versions = g.List(
        g.lazy_import("graphql_api.version.types.Version"),
        description="The versions this version group owns.",
    )

    def resolve_generation(self, info):
        return info.context.loaders.generation.load(self.generation_id)

    def resolve_versions(self, info):
        return info.context.loaders.versiongroup_versions.load(LoaderKey(self.pk))
