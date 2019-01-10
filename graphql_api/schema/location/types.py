import graphene as g
from graphql_api.utils import load, load_with_args
from .. import interfaces as i  # pylint: disable=unused-import
from .. import base


class Location(g.ObjectType):
    """
    Locations that can be visited within the games. Locations make up sizable portions of regions, like cities or routes.
    """

    pk = None
    areas = g.List(
        g.lazy_import("graphql_api.schema.location_area.types.LocationArea"),
        description="Areas that can be found within this location.",
        resolver=load("location_locationareas", using="pk"),
    )
    game_indices = g.List(
        lambda: LocationGameIndex,
        description="A list of game indices relevent to this location by generation.",
        resolver=load("location_gameindices", using="pk"),
    )
    name = g.ID(name="idName", description="The name of this resource.")
    names = base.TranslationList(
        lambda: LocationName,
        description="The name of this resource listed in different languages.",
        resolver=load_with_args("location_names", using="pk"),
    )
    region_id = None
    region = g.Field(
        g.lazy_import("graphql_api.schema.region.types.Region"),
        description="The region this location can be found in.",
        resolver=load("region", using="region_id"),
    )


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
        g.lazy_import("graphql_api.schema.generation.types.Generation"),
        description="The generation relevent to this game index.",
        resolver=load("generation", using="generation_id"),
    )
