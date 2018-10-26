import graphene as g
from ..loader_key import LoaderKey
from .. import interfaces as i  # pylint: disable=unused-import
from .. import base


class Version(g.ObjectType):
    """Versions of the games, e.g., Red, Blue or Yellow."""

    pk = None
    version_group_id = None
    # version_group = g.Field(
    #     g.lazy_import("graphql_api.version_group.types.VersionGroup"),
    #     description="The version group this version belongs to.",
    # )
    name = g.ID(description="The name of this resource.")
    names = base.TranslationList(
        lambda: VersionName,
        description="The name of this resource listed in different languages.",
    )

    def resolve_version_group(self, info):
        return info.context.loaders.version.load(self.version_group_id)

    def resolve_names(self, info, **kwargs):
        key = LoaderKey(self.pk, **kwargs)
        return info.context.loaders.version_names.load(key)


class VersionName(base.BaseTranslation, interfaces=[i.Translation]):
    name = g.String(
        name="text", description="The localized resource name in a specific language."
    )
