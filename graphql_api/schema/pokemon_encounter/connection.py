import graphene as g
from .. import base
from . import types  # pylint: disable=unused-import


class PokemonEncounterConnection(
    g.relay.Connection, base.BaseConnection, node=types.PokemonEncounter
):
    pass


# class PokemonEncounterWhere(base.BaseWhere):
#     max_level__gt = g.Int()
#     min_level__gt = g.Int()
#     encountermethod__name = g.ID(name="encounterMethod")
#     locationarea__name = g.ID(name="locationArea")
#     pokemon__name = g.ID(name="pokemon")
#     version__name = g.ID(name="version")


# class PokemonEncounterSort(base.BaseSort):
#     field = g.InputField(
#         g.Enum(
#             "PokemonEncounterSortOptions",
#             [
#                 ("CHANCE", "chance"),
#                 ("LOCATION_AREA", "location_area"),
#                 ("MAX_LEVEL", "max_level"),
#                 ("MIN_LEVEL", "min_level"),
#                 ("POKEMON", "pokemon"),
#                 ("VERSION", "version"),
#             ],
#         ),
#         description="The field to sort by.",
#     )
