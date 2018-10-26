import graphene as g
from ..utils import load

class VersionGroup(g.ObjectType):
    """Versions of the games, e.g., Red, Blue or Yellow."""

    pk = None
    generation_id = None
    generation = g.Field(
        g.lazy_import("graphql_api.generation.types.Generation"),
        description="The generation this version was introduced in.",
        resolver=load("generation", using="generation_id"),
    )
    name = g.ID(description="The name of this resource.")
    order = g.Int(
        description="Order for sorting. Almost by date of release, except similar versions are grouped together."
    )
    versions = g.List(
        g.lazy_import("graphql_api.version.types.Version"),
        description="The versions this version group owns.",
        resolver=load("versiongroup_versions", using="pk"),
    )
