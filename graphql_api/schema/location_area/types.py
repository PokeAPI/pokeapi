import graphene as g
from pokemon_v2 import models
from graphql_api.utils import load, load_with_args, get_connection
from .. import interfaces as i  # pylint: disable=unused-import
from .. import base


class LocationArea(g.ObjectType):
    """
    Location areas are sections of areas, such as floors in a building or cave. Each area has its own set of possible Pokémon encounters.
    """

    pk = None
    encounter_method_rates = g.List(
        lambda: EncounterMethodRate,
        description="A list of methods in which Pokémon may be encountered in this area and how likely the method will occur depending on the version of the game.",
    )
    game_index = g.Int(
        description="The internal id of an API resource within game data."
    )
    location_id = None
    location = g.Field(
        g.lazy_import("graphql_api.schema.location.types.Location"),
        description="The location this area can be found in.",
        resolver=load("location", using="location_id"),
    )
    name = g.ID(description="The name of this resource.")
    names = base.TranslationList(
        lambda: LocationAreaName,
        description="The name of this resource listed in different languages.",
        resolver=load_with_args("locationarea_names", using="pk"),
    )
    pokemon_encounters = g.relay.ConnectionField(
        g.lazy_import(
            "graphql_api.schema.pokemon_encounter.connection.PokemonEncounterConnection"
        ),
        description="A list of Pokémon encounters for this location area.",
    )

    def resolve_encounter_method_rates(self, info):
        def convert(encounter_rates):
            encounter_method_ids = {er.encounter_method_id for er in encounter_rates}
            em_rates = []
            for em_id in encounter_method_ids:
                emr = EncounterMethodRate()
                emr.location_area_id = self.pk
                emr.encounter_method_id = em_id
                em_rates.append(emr)

            # Ensure that results are always in a consistent order
            em_rates.sort(key=lambda emr: emr.encounter_method_id)

            return em_rates

        return info.context.loaders.locationarea_encounterrates.load(self.pk).then(
            convert
        )

    def resolve_pokemon_encounters(self, info, **kwargs):
        from ..pokemon_encounter import types, connection as conn

        def convert(pokemon):
            pe = types.PokemonEncounter()
            pe.location_area_id = self.pk
            pe.pokemon_id = pokemon.pk
            return pe

        q = models.Pokemon.objects.filter(encounter__location_area_id=self.pk)
        q = q.distinct()
        return get_connection(q, conn.PokemonEncounterConnection, convert, **kwargs)


class LocationAreaName(base.BaseTranslation, interfaces=[i.Translation]):
    name = g.String(
        name="text", description="The localized resource name in a specific language."
    )


class EncounterMethodRate(g.ObjectType):
    location_area_id = None
    encounter_method_id = None
    encounter_method = g.Field(
        g.lazy_import("graphql_api.schema.encounter_method.types.EncounterMethod"),
        description="The method in which Pokémon may be encountered in an area.",
        resolver=load("encountermethod", using="encounter_method_id"),
    )
    version_details = g.List(
        lambda: EncounterVersionDetails,
        description="The chance of the encounter to occur on a version of the game.",
    )

    def resolve_version_details(self, info):
        def convert(encounter_rates):
            version_ids = {
                (er.version_id, er.rate)
                for er in encounter_rates
                if er.encounter_method_id == self.encounter_method_id
            }
            encounter_version_details = []
            for version_id, rate in version_ids:
                evd = EncounterVersionDetails()
                evd.version_id = version_id
                evd.rate = rate
                encounter_version_details.append(evd)
            return encounter_version_details

        return info.context.loaders.locationarea_encounterrates.load(
            self.location_area_id
        ).then(convert)


class EncounterVersionDetails(g.ObjectType):
    rate = g.Int(description="The chance that an encounter will occur.")
    version_id = None
    version = g.Field(
        g.lazy_import("graphql_api.schema.version.types.Version"),
        description="The version of the game in which the encounter can occur with the given chance.",
        resolver=load("version", using="version_id"),
    )
