import graphene as g
from django.db.models import Sum
from pokemon_v2 import models
from graphql_api.utils import load  #, get_connection
# from ..encounter import connection as conn


class PokemonEncounter(g.ObjectType):
    """A list of encounters by version for a specific Location Area and Pokémon."""

    pk = None
    location_area_id = None
    location_area = g.Field(
        g.lazy_import("graphql_api.schema.location_area.types.LocationArea"),
        description="The location area the referenced Pokémon can be encountered in.",
        resolver=load("locationarea", using="location_area_id"),
    )
    pokemon_id = None
    pokemon = g.Field(
        g.lazy_import("graphql_api.schema.pokemon.types.Pokemon"),
        description="The Pokémon being encountered.",
        resolver=load("pokemon", using="pokemon_id"),
    )
    version_details = g.List(
        lambda: VersionEncounterDetail,
        description="A list of versions and encounters with Pokémon that might happen in the referenced location area.",
    )

    def resolve_version_details(self, info):
        def create_version_details(encounters):
            version_ids = {e.version_id for e in encounters}
            details = []
            for version_id in version_ids:
                detail = VersionEncounterDetail()
                detail.location_area_id = self.location_area_id
                detail.pokemon_id = self.pokemon_id
                detail.version_id = version_id
                details.append(detail)
            return details

        key = (self.location_area_id, self.pokemon_id)
        return info.context.loaders.encounters_by_locationarea_and_pokemon.load(
            key
        ).then(create_version_details)


class VersionEncounterDetail(g.ObjectType):
    """A list of encounters for a specific Location Area, Pokémon, and Version."""

    encounters = g.List(
        g.lazy_import("graphql_api.schema.encounter.types.Encounter"),
        description="A list of encounters and their specifics.",
    )
    location_area_id = None
    max_chance = g.Int(description="The total sum of all encounter potential.")
    pokemon_id = None
    version_id = None
    version = g.Field(
        g.lazy_import("graphql_api.schema.version.types.Version"),
        description="The game version this encounter happens in.",
        resolver=load("version", using="version_id"),
    )

    def resolve_max_chance(self, info):
        return models.Encounter.objects.filter(
            location_area_id=self.location_area_id,
            pokemon_id=self.pokemon_id,
            version_id=self.version_id,
        ).aggregate(Sum("encounter_slot__rarity"))["encounter_slot__rarity__sum"]

    def resolve_encounters(self, info):
        key = (self.location_area_id, self.pokemon_id, self.version_id)
        return info.context.loaders.encounters_by_parts.load(key)

    # def resolve_encounters(self, info, where=None, order_by=None, **kwargs):
    #     q = models.Encounter.objects.filter(
    #         location_area_id=self.location_area_id,
    #         pokemon_id=self.pokemon_id,
    #         version_id=self.version_id,
    #     ).select_related("encounter_slot")

    #     where = where or {}
    #     q = conn.EncounterSort.apply(q, order_by)
    #     q = conn.EncounterWhere.apply(q, **where)

    #     return get_connection(q, conn.EncounterConnection, **kwargs)
