import graphene as g
from pokemon_v2 import models
from ..loader_key import LoaderKey
from ..utils import get_connection
from .. import interfaces as i  # pylint: disable=unused-import
from .. import base


class Region(g.ObjectType):
    """
    Regions that can be visited within the games. Regions make up sizable portions of regions, like cities or routes.
    """

    pk = None
    locations = g.relay.ConnectionField(
        g.lazy_import("graphql_api.location.connection.LocationConnection"),
        description="A list of locations that can be found in this region.",
    )
    main_generation = g.Field(
        g.lazy_import("graphql_api.generation.types.Generation"),
        description="The generation this region was introduced in.",
    )
    name = g.ID(description="The name of this resource.")
    names = base.TranslationList(
        lambda: RegionName,
        description="The name of this resource listed in different languages.",
    )
    # pokedexes = g.List(
    #     g.lazy_import("graphql_api.pokedex.types.Pokedex"),
    #     description="A lists of pokédexes that catalogue Pokémon in this region.",
    # )
    version_groups = g.List(
        g.lazy_import("graphql_api.version_group.types.VersionGroup"),
        description="A list of version groups where this region can be visited.",
    )

    def resolve_locations(self, info, **kwargs):
        from ..location.connection import LocationConnection
        q = models.Location.objects.filter(region_id=self.pk)
        return get_connection(q, LocationConnection, **kwargs)

    def resolve_main_generation(self, info):
        return info.context.loaders.generation_by_region.load(self.pk)

    def resolve_names(self, info, **kwargs):
        return info.context.loaders.region_names.load(LoaderKey(self.pk, **kwargs))

    def resolve_version_groups(self, info):
        return info.context.loaders.region_versiongroups.load(LoaderKey(self.pk))


class RegionName(base.BaseTranslation, interfaces=[i.Translation]):
    name = g.String(
        name="text", description="The localized resource name in a specific language."
    )
