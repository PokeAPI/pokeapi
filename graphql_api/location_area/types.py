import graphene as g
# from pokemon_v2 import models
from ..utils import load, load_with_args  #, get_connection
from .. import interfaces as i  # pylint: disable=unused-import
from .. import base


class LocationArea(g.ObjectType):
    """
    Location areas are sections of areas, such as floors in a building or cave. Each area has its own set of possible Pokémon encounters.
    """

    pk = None
    # encounter_method_rates = g.List(
    #     g.lazy_import("graphql_api.encounter_method_rate.types.EncounterMethodRate"),
    #     description="A list of methods in which Pokémon may be encountered in this area and how likely the method will occur depending on the version of the game.",
    #     resolver=load("locationarea_encounterrates", using="pk"),
    # )
    game_index = g.Int(
        description="The internal id of an API resource within game data."
    )
    location_id = None
    location = g.Field(
        g.lazy_import("graphql_api.location.types.Location"),
        description="The location this area can be found in.",
        resolver=load("location", using="location_id")
    )
    name = g.ID(description="The name of this resource.")
    names = base.TranslationList(
        lambda: LocationAreaName,
        description="The name of this resource listed in different languages.",
        resolver=load_with_args("locationarea_names", using="pk"),
    )
    # pokemon_encounters = g.relay.ConnectionField(
    #     g.lazy_import(
    #         "graphql_api.pokemon_encounter.connection.PokemonEncounterConnection"
    #     ),
    #     description="A list of Pokémon encounters for this location area.",
    # )

    # def resolve_pokemon_encounters(self, info):
    #     from ..pokemon_encounter.connection import PokemonEncounterConnection

    #     q = models.Pokemon.objects.filter(encounter__location_area_id=self.pk)
    #     q = q.distinct()

    #     return get_connection(
    #         q, conn.PokemonEncounterConnection, LocationArea.get_pkmn_encounter
    #     )

    # @staticmethod
    # def get_pkmn_encounter(root, pokemon):
    #     from ..pokemon_encounter.types import PokemonEncounter

    #     pkmn_encounter = PokemonEncounter()
    #     pkmn_encounter.location_area_id = root.pk
    #     pkmn_encounter.pokemon_id = pokemon.pk
    #     return pkmn_encounter


class LocationAreaName(base.BaseTranslation, interfaces=[i.Translation]):
    name = g.String(
        name="text", description="The localized resource name in a specific language."
    )
