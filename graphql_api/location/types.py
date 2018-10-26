import graphene as g
from ..loader_key import LoaderKey
from .. import interfaces as i  # pylint: disable=unused-import
from .. import base


class Location(g.ObjectType):
    """
    Locations that can be visited within the games. Locations make up sizable portions of regions, like cities or routes.
    """

    pk = None
    areas = g.List(
        g.lazy_import("graphql_api.location_area.types.LocationArea"),
        description="Areas that can be found within this location.",
    )
    game_indices = g.List(
        lambda: LocationGameIndex,
        description="A list of game indices relevent to this location by generation."
    )
    name = g.ID(description="The name of this resource.")
    names = base.TranslationList(
        lambda: LocationName,
        description="The name of this resource listed in different languages.",
    )
    region_id = None
    region = g.Field(
        g.lazy_import('graphql_api.region.types.Region'),
        description="The region this location can be found in."
    )

    def resolve_areas(self, info):
        return info.context.loaders.location_locationareas.load(self.pk)

    def resolve_game_indices(self, info):
        return info.context.loaders.location_gameindices.load(self.pk)

    def resolve_names(self, info, **kwargs):
        return info.context.loaders.location_names.load(LoaderKey(self.pk, **kwargs))

    def resolve_region(self, info):
        return info.context.loaders.region.load(self.region_id)


class LocationName(base.BaseTranslation, interfaces=[i.Translation]):
    name = g.String(
        name="text", description="The localized resource name in a specific language."
    )


class LocationGameIndex(g.ObjectType):
    game_index = g.Int(
        description="The internal id of an API resource within game data."
    )
    generation_id = None
    generation = g.Field(
        g.lazy_import("graphql_api.generation.types.Generation"),
        description="The generation relevent to this game index.",
    )

    def resolve_generation(self, info):
        return info.context.loaders.generation.load(self.generation_id)
