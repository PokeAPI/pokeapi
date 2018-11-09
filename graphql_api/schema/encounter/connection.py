import graphene as g
from .. import base
from . import types  # pylint: disable=unused-import


class EncounterConnection(
    g.relay.Connection, base.BaseConnection, node=types.Encounter
):
    pass


class EncounterWhere(base.BaseWhere):
    # max_level__gt = g.Int()
    # min_level__gt = g.Int()
    encountermethod__name = g.ID(name="encounterMethod")
    locationarea__name = g.ID(name="locationArea")
    pokemon__name = g.ID(name="pokemon")
    version__name = g.ID(name="version")


class EncounterSort(base.BaseSort):
    field = g.InputField(
        g.Enum(
            "EncounterSortOptions",
            [
                ("CHANCE", "chance"),
                ("LOCATION_AREA", "location_area"),
                ("MAX_LEVEL", "max_level"),
                ("MIN_LEVEL", "min_level"),
                ("POKEMON", "pokemon"),
                ("VERSION", "version"),
            ],
        ),
        description="The field to sort by.",
    )
