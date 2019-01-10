import graphene as g
from graphql_api.utils import load, load_with_args
from .. import interfaces as i  # pylint: disable=unused-import
from .. import base


class Version(g.ObjectType):
    """Versions of the games, e.g., Red, Blue or Yellow."""

    pk = None
    version_group_id = None
    version_group = g.Field(
        g.lazy_import("graphql_api.schema.version_group.types.VersionGroup"),
        description="The version group this version belongs to.",
        resolver=load("versiongroup", using="version_group_id"),
    )
    name = g.ID(name="idName", description="The name of this resource.")
    names = base.TranslationList(
        lambda: VersionName,
        description="The name of this resource listed in different languages.",
        resolver=load_with_args("version_names", using="pk"),
    )


class VersionName(base.BaseTranslation, interfaces=[i.Translation]):
    name = g.String(
        name="text", description="The localized resource name in a specific language."
    )
