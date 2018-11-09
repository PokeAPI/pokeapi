import graphene as g
from pokemon_v2 import models
from graphql_api.utils import load, load_with_args, get_connection
from .. import interfaces as i  # pylint: disable=unused-import
from .. import base


class Region(g.ObjectType):
    """
    Regions that can be visited within the games. Regions make up sizable portions of regions, like cities or routes.
    """

    pk = None
    locations = g.relay.ConnectionField(
        g.lazy_import("graphql_api.schema.location.connection.LocationConnection"),
        description="A list of locations that can be found in this region.",
    )
    main_generation = g.Field(
        g.lazy_import("graphql_api.schema.generation.types.Generation"),
        description="The generation this region was introduced in.",
        resolver=load("region_generation", using="pk"),
    )
    name = g.ID(description="The name of this resource.")
    names = base.TranslationList(
        lambda: RegionName,
        description="The name of this resource listed in different languages.",
        resolver=load_with_args("region_names", using="pk"),
    )
    pokedexes = g.List(
        g.lazy_import("graphql_api.schema.pokedex.types.Pokedex"),
        description="A lists of pokédexes that catalogue Pokémon in this region.",
        resolver=load("region_pokedexes", using="pk"),
    )
    version_groups = g.List(
        g.lazy_import("graphql_api.schema.version_group.types.VersionGroup"),
        description="A list of version groups where this region can be visited.",
        resolver=load("region_versiongroups", using="pk"),
    )

    def resolve_locations(self, info, **kwargs):
        from ..location.connection import LocationConnection

        q = models.Location.objects.filter(region_id=self.pk)
        return get_connection(q, LocationConnection, **kwargs)


class RegionName(base.BaseTranslation, interfaces=[i.Translation]):
    name = g.String(
        name="text", description="The localized resource name in a specific language."
    )
