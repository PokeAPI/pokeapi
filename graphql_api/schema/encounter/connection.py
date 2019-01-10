import graphene as g
from .. import base
from . import types  # pylint: disable=unused-import


class EncounterConnection(
    g.relay.Connection, base.BaseConnection, node=types.Encounter
):
    pass


class EncounterWhere(base.BaseWhere):
    chance = g.Argument(base.IntFilter)
    encounterconditionvaluemap__encounter_condition_value__name = g.Argument(
        base.ListFilter, name="conditions"
    )
    encountermethod__name = g.List(g.ID, name="encounterMethod_idName")
    locationarea__name = g.List(g.ID, name="locationArea_idName")
    location_area = g.Argument(
        g.lazy_import("graphql_api.schema.location_area.connection.LocationAreaWhere")
    )
    max_level = g.Argument(base.IntFilter)
    min_level = g.Argument(base.IntFilter)
    pokemon = g.Argument(
        g.lazy_import("graphql_api.schema.pokemon.connection.PokemonWhere")
    )
    pokemon__name = g.List(g.ID, name="pokemon_idName")
    version__name = g.List(g.ID, name="version_idName")

    @classmethod
    def apply(cls, qs, prefix="", pokemon=None, location_area=None, **where):
        from graphql_api.schema.pokemon.connection import PokemonWhere
        from graphql_api.schema.location_area.connection import LocationAreaWhere

        if pokemon:
            qs = PokemonWhere.apply(qs, **pokemon, prefix=prefix + "pokemon__")
        if location_area:
            qs = LocationAreaWhere.apply(
                qs, **location_area, prefix=prefix + "location_area__"
            )

        return super().apply(qs, **where)


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
