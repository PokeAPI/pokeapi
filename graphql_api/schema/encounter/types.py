import graphene as g
from graphql_api.utils import load


# This type relies on the private field 'encounter_slot' being pre-loaded for performance,
# e.g. using 'select_related' on a Django query set


class Encounter(g.ObjectType):
    """
    An encounter is a set of conditions that must be met in order to meet a particular Pokémon in a particular game version, and the likelihood that the encounter will occur if the conditions are met.
    """

    encounter_slot = None
    chance = g.Float(
        description="The chance that this encounter will occur, out of 1.",
        resolver=lambda root, info: root.encounter_slot.rarity / 100,
    )
    condition_values = g.List(
        g.lazy_import(
            "graphql_api.schema.encounter_condition.types.EncounterConditionValue"
        ),
        description="A list of condition values that must be in effect for this encounter to occur.",
        resolver=load("encounter_conditionvalues", using="pk"),
    )
    location_area_id = None
    location_area = g.Field(
        g.lazy_import("graphql_api.schema.location_area.types.LocationArea"),
        description="The location area this encounter occurs in.",
        resolver=load("locationarea", using="location_area_id"),
    )
    max_level = g.Int(
        description="The highest level the Pokémon can be encountered at."
    )
    method = g.Field(
        g.lazy_import("graphql_api.schema.encounter_method.types.EncounterMethod"),
        description="The method by which this encounter happens.",
    )
    min_level = g.Int(description="The lowest level the Pokémon can be encountered at.")
    pk = g.ID(name="name", description="The name of this resource.")
    pokemon_id = None
    pokemon = g.Field(
        g.lazy_import("graphql_api.schema.pokemon.types.Pokemon"),
        description="The Pokémon that is encountered.",
        resolver=load("pokemon", using="pokemon_id"),
    )
    version_id = None
    version = g.Field(
        g.lazy_import("graphql_api.schema.version.types.Version"),
        description="The game version this encounter occurs in.",
        resolver=load("version", using="version_id"),
    )

    def resolve_method(self, info):
        encounter_method_id = self.encounter_slot.encounter_method_id
        return info.context.loaders.encountermethod.load(encounter_method_id)
