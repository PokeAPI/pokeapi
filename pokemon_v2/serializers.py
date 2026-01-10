from collections import OrderedDict
import json
from django.urls import reverse
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

# pylint: disable=redefined-builtin

# PokeAPI v2 serializers in order of dependency

from .models import *


#########################
#  SUMMARY SERIALIZERS  #
#########################

# Summary serializers are just for list and reference behavior

# Putting summary serializers up top so there are no conflicts
# with reference accross models due to script running order


class AbilitySummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ability
        fields = ("name", "url")


class BerryFirmnessSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BerryFirmness
        fields = ("name", "url")


class BerryFlavorSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BerryFlavor
        fields = ("name", "url")


class BerrySummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Berry
        fields = ("name", "url")


class CharacteristicSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Characteristic
        fields = ("url",)


class ContestEffectSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ContestEffect
        fields = ("url",)


class ContestTypeSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ContestType
        fields = ("name", "url")


class EggGroupSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EggGroup
        fields = ("name", "url")


class EncounterConditionSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EncounterCondition
        fields = ("name", "url")


class EncounterConditionValueSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EncounterConditionValue
        fields = ("name", "url")


class EncounterMethodSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EncounterMethod
        fields = ("name", "url")


class EvolutionTriggerSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EvolutionTrigger
        fields = ("name", "url")


class EvolutionChainSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EvolutionChain
        fields = ("url",)


class GenerationSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Generation
        fields = ("name", "url")


class GenderSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Gender
        fields = ("name", "url")


class GrowthRateSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GrowthRate
        fields = ("name", "url")


class ItemPocketSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ItemPocket
        fields = ("name", "url")


class ItemCategorySummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ItemCategory
        fields = ("name", "url")


class ItemAttributeSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ItemAttribute
        fields = ("name", "url")


class ItemFlingEffectSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ItemFlingEffect
        fields = ("name", "url")


class ItemSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = ("name", "url")


class LanguageSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Language
        fields = ("name", "url")


class LocationSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = ("name", "url")


class LocationAreaSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LocationArea
        fields = ("name", "url")


class MachineSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Machine
        fields = ("url",)


class MoveBattleStyleSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MoveBattleStyle
        fields = ("name", "url")


class MoveDamageClassSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MoveDamageClass
        fields = ("name", "url")


class MoveMetaAilmentSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MoveMetaAilment
        fields = ("name", "url")


class MoveMetaCategorySummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MoveMetaCategory
        fields = ("name", "url")


class MoveTargetSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MoveTarget
        fields = ("name", "url")


class MoveSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Move
        fields = ("name", "url")


class MoveLearnMethodSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MoveLearnMethod
        fields = ("name", "url")


class NatureSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Nature
        fields = ("name", "url")


class PalParkAreaSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PalParkArea
        fields = ("name", "url")


class PokeathlonStatSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PokeathlonStat
        fields = ("name", "url")


class PokedexSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pokedex
        fields = ("name", "url")


class PokemonColorSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PokemonColor
        fields = ("name", "url")


class PokemonHabitatSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PokemonHabitat
        fields = ("name", "url")


class PokemonShapeSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PokemonShape
        fields = ("name", "url")


class PokemonSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pokemon
        fields = ("name", "url")


class PokemonSpeciesSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PokemonSpecies
        fields = ("name", "url")


class PokemonFormSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PokemonForm
        fields = ("name", "url")


class RegionSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Region
        fields = ("name", "url")


class StatSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Stat
        fields = ("name", "url")


class SuperContestEffectSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SuperContestEffect
        fields = ("url",)


class TypeSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Type
        fields = ("name", "url")


class VersionSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Version
        fields = ("name", "url")


class VersionGroupSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VersionGroup
        fields = ("name", "url")


#####################
#  MAP SERIALIZERS  #
#####################


class BerryFlavorMapSerializer(serializers.ModelSerializer):
    berry = BerrySummarySerializer()
    flavor = BerryFlavorSummarySerializer(source="berry_flavor")

    class Meta:
        model = BerryFlavorMap
        fields = ("potency", "berry", "flavor")


class ItemAttributeMapSerializer(serializers.ModelSerializer):
    item = ItemSummarySerializer()
    attribute = ItemAttributeSummarySerializer(source="item_attribute")

    class Meta:
        model = ItemAttributeMap
        fields = (
            "item",
            "attribute",
        )


class MoveMetaStatChangeSerializer(serializers.ModelSerializer):
    stat = StatSummarySerializer()
    move = MoveSummarySerializer()

    class Meta:
        model = MoveMetaStatChange
        fields = ("change", "move", "stat")


class NaturePokeathlonStatSerializer(serializers.ModelSerializer):
    pokeathlon_stat = PokeathlonStatSummarySerializer()
    nature = NatureSummarySerializer()

    class Meta:
        model = NaturePokeathlonStat
        fields = ("max_change", "nature", "pokeathlon_stat")


class PokemonAbilitySerializer(serializers.ModelSerializer):
    pokemon = PokemonSummarySerializer()
    ability = AbilitySummarySerializer()

    class Meta:
        model = PokemonAbility
        fields = ("is_hidden", "slot", "ability", "pokemon")


class PokemonAbilityPastSerializer(serializers.ModelSerializer):
    generation = GenerationSummarySerializer()
    ability = AbilitySummarySerializer()

    class Meta:
        model = PokemonAbilityPast
        fields = ("is_hidden", "pokemon", "generation", "slot", "ability")


class PokemonDexEntrySerializer(serializers.ModelSerializer):
    entry_number = serializers.IntegerField(source="pokedex_number")
    pokedex = PokedexSummarySerializer()

    class Meta:
        model = PokemonDexNumber
        fields = ("entry_number", "pokedex")


class PokemonTypeSerializer(serializers.ModelSerializer):
    pokemon = PokemonSummarySerializer()
    type = TypeSummarySerializer()

    class Meta:
        model = PokemonType
        fields = ("slot", "pokemon", "type")


class PokemonFormTypeSerializer(serializers.ModelSerializer):
    pokemon_form = PokemonFormSummarySerializer()
    type = TypeSummarySerializer()

    class Meta:
        model = PokemonFormType
        fields = ("slot", "pokemon_form", "type")


class PokemonTypePastSerializer(serializers.ModelSerializer):
    generation = GenerationSummarySerializer()
    type = TypeSummarySerializer()

    class Meta:
        model = PokemonTypePast
        fields = ("pokemon", "generation", "slot", "type")


class PokedexVersionGroupSerializer(serializers.ModelSerializer):
    pokedex = PokedexSummarySerializer()
    version_group = VersionGroupSummarySerializer()

    class Meta:
        model = PokedexVersionGroup
        fields = ("pokedex", "version_group")


class VersionGroupMoveLearnMethodSerializer(serializers.ModelSerializer):
    version_group = VersionGroupSummarySerializer()
    move_learn_method = MoveLearnMethodSummarySerializer()

    class Meta:
        model = ItemAttributeMap
        fields = ("version_group", "move_learn_method")


class VersionGroupRegionSerializer(serializers.ModelSerializer):
    version_group = VersionGroupSummarySerializer()
    region = RegionSummarySerializer()

    class Meta:
        model = ItemAttributeMap
        fields = (
            "version_group",
            "region",
        )


class EncounterConditionValueMapSerializer(serializers.ModelSerializer):
    condition_value = EncounterConditionValueSummarySerializer(
        source="encounter_condition_value"
    )

    class Meta:
        model = EncounterConditionValueMap
        fields = ("condition_value",)


################################
#  CHARACTERISTIC SERIALIZERS  #
################################


class CharacteristicDescriptionSerializer(serializers.ModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = CharacteristicDescription
        fields = ("description", "language")


class CharacteristicDetailSerializer(serializers.ModelSerializer):
    descriptions = CharacteristicDescriptionSerializer(
        many=True, read_only=True, source="characteristicdescription"
    )
    highest_stat = StatSummarySerializer(source="stat")
    gene_modulo = serializers.IntegerField(source="gene_mod_5")
    possible_values = serializers.SerializerMethodField("get_values")

    class Meta:
        model = Characteristic
        fields = (
            "id",
            "gene_modulo",
            "possible_values",
            "highest_stat",
            "descriptions",
        )

    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "integer",
                "format": "int32",
            },
            "examples": [[0, 5, 10, 15, 20, 25, 30]],
        }
    )
    def get_values(self, obj):
        mod = obj.gene_mod_5
        values = []
        while mod <= 31:
            values.append(mod)
            mod += 5

        return values


#########################
#  CONTEST SERIALIZERS  #
#########################


class SuperContestEffectFlavorTextSerializer(serializers.ModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = SuperContestEffectFlavorText
        fields = ("flavor_text", "language")


class SuperContestEffectDetailSerializer(serializers.ModelSerializer):
    flavor_text_entries = SuperContestEffectFlavorTextSerializer(
        many=True, read_only=True, source="supercontesteffectflavortext"
    )
    moves = MoveSummarySerializer(many=True, read_only=True, source="move")

    class Meta:
        model = SuperContestEffect
        fields = ("id", "appeal", "flavor_text_entries", "moves")


class ContestEffectEffectTextSerializer(serializers.ModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = ContestEffectEffectText
        fields = ("effect", "language")


class ContestEffectFlavorTextSerializer(serializers.ModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = ContestEffectFlavorText
        fields = ("flavor_text", "language")


class ContestEffectDetailSerializer(serializers.ModelSerializer):
    effect_entries = ContestEffectEffectTextSerializer(
        many=True, read_only=True, source="contesteffecteffecttext"
    )
    flavor_text_entries = ContestEffectFlavorTextSerializer(
        many=True, read_only=True, source="contesteffectflavortext"
    )

    class Meta:
        model = ContestEffect
        fields = ("id", "appeal", "jam", "effect_entries", "flavor_text_entries")


class ContestTypeNameSerializer(serializers.ModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = ContestTypeName
        fields = ("name", "color", "language")


class ContestTypeDetailSerializer(serializers.ModelSerializer):
    names = ContestTypeNameSerializer(
        many=True, read_only=True, source="contesttypename"
    )
    berry_flavor = BerryFlavorSummarySerializer(read_only=True, source="berryflavor")

    class Meta:
        model = ContestType
        fields = ("id", "name", "berry_flavor", "names")


class SuperContestComboSerializer(serializers.ModelSerializer):
    first_move = MoveSummarySerializer()
    second_move = MoveSummarySerializer()

    class Meta:
        model = SuperContestCombo
        fields = ("first_move", "second_move")


class ContestComboSerializer(serializers.ModelSerializer):
    first_move = MoveSummarySerializer()
    second_move = MoveSummarySerializer()

    class Meta:
        model = ContestCombo
        fields = ("first_move", "second_move")


########################
#  REGION SERIALIZERS  #
########################


class RegionNameSerializer(serializers.ModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = RegionName
        fields = ("name", "language")


class RegionDetailSerializer(serializers.ModelSerializer):
    names = RegionNameSerializer(many=True, read_only=True, source="regionname")
    locations = LocationSummarySerializer(many=True, read_only=True, source="location")
    version_groups = serializers.SerializerMethodField("get_region_version_groups")
    pokedexes = PokedexSummarySerializer(many=True, read_only=True, source="pokedex")
    main_generation = GenerationSummarySerializer(read_only=True, source="generation")

    class Meta:
        model = Region
        fields = (
            "id",
            "name",
            "locations",
            "main_generation",
            "names",
            "pokedexes",
            "version_groups",
        )

    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name", "url"],
                "properties": {
                    "name": {"type": "string", "examples": ["red-blue"]},
                    "url": {
                        "type": "string",
                        "format": "uri",
                        "examples": ["https://pokeapi.co/api/v2/version-group/1/"],
                    },
                },
            },
        }
    )
    def get_region_version_groups(self, obj):
        vg_regions = VersionGroupRegion.objects.filter(region=obj)
        data = VersionGroupRegionSerializer(
            vg_regions, many=True, context=self.context
        ).data
        groups = []

        for group in data:
            groups.append(group["version_group"])

        return groups


############################
#  GENERATION SERIALIZERS  #
############################


class GenerationNameSerializer(serializers.ModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = GenerationName
        fields = ("name", "language")


class GenerationDetailSerializer(serializers.ModelSerializer):
    main_region = RegionSummarySerializer(source="region")
    names = GenerationNameSerializer(many=True, read_only=True, source="generationname")
    abilities = AbilitySummarySerializer(many=True, read_only=True, source="ability")
    moves = MoveSummarySerializer(many=True, read_only=True, source="move")
    pokemon_species = PokemonSpeciesSummarySerializer(
        many=True, read_only=True, source="pokemonspecies"
    )
    types = TypeSummarySerializer(many=True, read_only=True, source="type")
    version_groups = VersionGroupSummarySerializer(
        many=True, read_only=True, source="versiongroup"
    )

    class Meta:
        model = Generation
        fields = (
            "id",
            "name",
            "abilities",
            "main_region",
            "moves",
            "names",
            "pokemon_species",
            "types",
            "version_groups",
        )


########################
#  GENDER SERIALIZERS  #
########################


class GenderDetailSerializer(serializers.ModelSerializer):
    pokemon_species_details = serializers.SerializerMethodField("get_species")
    required_for_evolution = serializers.SerializerMethodField("get_required")

    class Meta:
        model = Gender
        fields = ("id", "name", "pokemon_species_details", "required_for_evolution")

    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["rate", "pokemon_species"],
                "properties": {
                    "rate": {"type": "integer", "format": "int32", "examples": [1]},
                    "pokemon_species": {
                        "type": "object",
                        "required": ["name", "url"],
                        "properties": {
                            "name": {"type": "string", "examples": ["bulbasaur"]},
                            "url": {
                                "type": "string",
                                "format": "uri",
                                "examples": [
                                    "https://pokeapi.co/api/v2/pokemon-species/1/"
                                ],
                            },
                        },
                    },
                },
            },
        }
    )
    def get_species(self, obj):
        species_objects = []

        if obj.name == "female":
            species_objects = PokemonSpecies.objects.filter(gender_rate__gt=0)
        elif obj.name == "male":
            species_objects = PokemonSpecies.objects.filter(gender_rate__range=[0, 7])
        elif obj.name == "genderless":
            species_objects = PokemonSpecies.objects.filter(gender_rate=-1)

        details = []

        for species in species_objects:
            detail = OrderedDict()
            detail["rate"] = species.gender_rate
            detail["pokemon_species"] = PokemonSpeciesSummarySerializer(
                species, context=self.context
            ).data
            details.append(detail)

        return details

    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name", "url"],
                "properties": {
                    "name": {"type": "string", "examples": ["wormadam"]},
                    "url": {
                        "type": "string",
                        "format": "uri",
                        "examples": ["https://pokeapi.co/api/v2/pokemon-species/413/"],
                    },
                },
            },
        }
    )
    def get_required(self, obj):
        evo_objects = PokemonEvolution.objects.filter(gender=obj)
        species_list = []

        for evo in evo_objects:
            species = PokemonSpeciesSummarySerializer(
                evo.evolved_species, context=self.context
            ).data
            species_list.append(species)

        return species_list


#############################
#  GROWTH RATE SERIALIZERS  #
#############################


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ("level", "experience")


class GrowthRateDescriptionSerializer(serializers.ModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = GrowthRateDescription
        fields = ("description", "language")


class GrowthRateDetailSerializer(serializers.ModelSerializer):
    descriptions = GrowthRateDescriptionSerializer(
        many=True, read_only=True, source="growthratedescription"
    )
    levels = ExperienceSerializer(many=True, read_only=True, source="experience")
    pokemon_species = PokemonSpeciesSummarySerializer(
        many=True, read_only=True, source="pokemonspecies"
    )

    class Meta:
        model = GrowthRate
        fields = ("id", "name", "formula", "descriptions", "levels", "pokemon_species")


##########################
#  LANGUAGE SERIALIZERS  #
##########################


class LanguageNameSerializer(serializers.ModelSerializer):
    language = LanguageSummarySerializer(source="local_language")

    class Meta:
        model = LanguageName
        fields = ("name", "language")


class LanguageDetailSerializer(serializers.ModelSerializer):
    names = LanguageNameSerializer(
        many=True, read_only=True, source="languagename_language"
    )

    class Meta:
        model = Language
        fields = ("id", "name", "official", "iso639", "iso3166", "names")


########################################
#  LOCATION AND ENCOUNTER SERIALIZERS  #
########################################


class EncounterConditionNameSerializer(serializers.ModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = EncounterConditionName
        fields = ("name", "language")


class EncounterConditionDetailSerializer(serializers.ModelSerializer):
    names = EncounterConditionNameSerializer(
        many=True, read_only=True, source="encounterconditionname"
    )
    values = EncounterConditionValueSummarySerializer(
        many=True, read_only=True, source="encounterconditionvalue"
    )

    class Meta:
        model = EncounterCondition
        fields = ("id", "name", "values", "names")


class EncounterConditionValueNameSerializer(serializers.ModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = EncounterConditionValueName
        fields = ("name", "language")


class EncounterConditionValueDetailSerializer(serializers.ModelSerializer):
    condition = EncounterConditionSummarySerializer(source="encounter_condition")
    names = EncounterConditionValueNameSerializer(
        many=True, read_only=True, source="encounterconditionvaluename"
    )

    class Meta:
        model = EncounterConditionValue
        fields = ("id", "name", "condition", "names")


class EncounterMethodNameSerializer(serializers.ModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = EncounterMethodName
        fields = ("name", "language")


class EncounterMethodDetailSerializer(serializers.ModelSerializer):
    names = EncounterMethodNameSerializer(
        many=True, read_only=True, source="encountermethodname"
    )

    class Meta:
        model = EncounterMethod
        fields = ("id", "name", "order", "names")


class EncounterSlotSerializer(serializers.ModelSerializer):
    encounter_method = EncounterMethodSummarySerializer()
    chance = serializers.IntegerField(source="rarity")

    class Meta:
        model = EncounterSlot
        fields = ("id", "slot", "chance", "encounter_method", "version_group")


class EncounterDetailSerializer(serializers.ModelSerializer):
    version = VersionSummarySerializer()
    location_area = LocationAreaSummarySerializer()
    pokemon = PokemonSummarySerializer()
    condition_values = serializers.SerializerMethodField("get_encounter_conditions")

    class Meta:
        model = Encounter
        fields = (
            "min_level",
            "max_level",
            "version",
            "encounter_slot",
            "pokemon",
            "location_area",
            "condition_values",
        )

    def get_encounter_conditions(self, obj):
        condition_values = EncounterConditionValueMap.objects.filter(encounter=obj)
        data = EncounterConditionValueMapSerializer(
            condition_values, many=True, context=self.context
        ).data
        values = []

        for map in data:
            values.append(map["condition_value"])

        return values


class LocationAreaEncounterRateSerializer(serializers.ModelSerializer):
    encounter_method = EncounterMethodSummarySerializer()
    version = VersionSummarySerializer()

    class Meta:
        model = LocationAreaEncounterRate
        fields = ("rate", "encounter_method", "version")


class LocationAreaNameSerializer(serializers.ModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = LocationAreaName
        fields = ("name", "language")


class LocationAreaDetailSerializer(serializers.ModelSerializer):
    location = LocationSummarySerializer()
    encounter_method_rates = serializers.SerializerMethodField("get_method_rates")
    pokemon_encounters = serializers.SerializerMethodField("get_encounters")
    names = LocationAreaNameSerializer(
        many=True, read_only=True, source="locationareaname"
    )

    class Meta:
        model = LocationArea
        fields = (
            "id",
            "name",
            "game_index",
            "encounter_method_rates",
            "location",
            "names",
            "pokemon_encounters",
        )

    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["encounter_method", "version_details"],
                "properties": {
                    "encounter_method": {
                        "type": "object",
                        "required": ["name", "url"],
                        "properties": {
                            "name": {"type": "string", "examples": ["old-rod"]},
                            "url": {
                                "type": "string",
                                "format": "uri",
                                "examples": [
                                    "https://pokeapi.co/api/v2/encounter-method/2/"
                                ],
                            },
                        },
                    },
                    "version_details": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["rate", "version"],
                            "properties": {
                                "rate": {
                                    "type": "integer",
                                    "format": "int32",
                                    "examples": [5],
                                },
                                "version": {
                                    "type": "object",
                                    "required": ["name", "url"],
                                    "properties": {
                                        "name": {
                                            "type": "string",
                                            "examples": ["platinum"],
                                        },
                                        "url": {
                                            "type": "string",
                                            "format": "uri",
                                            "examples": [
                                                "https://pokeapi.co/api/v2/version/14/"
                                            ],
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        }
    )
    def get_method_rates(self, obj):
        # Get encounters related to this area and pull out unique encounter methods
        encounter_rates = LocationAreaEncounterRate.objects.filter(
            location_area=obj
        ).order_by("encounter_method_id")
        method_ids = encounter_rates.values("encounter_method_id").distinct()
        encounter_rate_list = []

        for id in method_ids:
            encounter_rate_details = OrderedDict()

            # Get each Unique Item by ID
            encounter_method_object = EncounterMethod.objects.get(
                pk=id["encounter_method_id"]
            )
            encounter_method_data = EncounterMethodSummarySerializer(
                encounter_method_object, context=self.context
            ).data
            encounter_rate_details["encounter_method"] = encounter_method_data

            # Get Versions associated with each unique item
            area_encounter_objects = encounter_rates.filter(
                encounter_method_id=id["encounter_method_id"]
            )
            serializer = LocationAreaEncounterRateSerializer(
                area_encounter_objects, many=True, context=self.context
            )
            encounter_rate_details["version_details"] = []

            for area_encounter in serializer.data:
                version_detail = OrderedDict()

                version_detail["rate"] = area_encounter["rate"]
                version_detail["version"] = area_encounter["version"]

                encounter_rate_details["version_details"].append(version_detail)

            encounter_rate_list.append(encounter_rate_details)

        return encounter_rate_list

    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["pokemon", "version_details"],
                "properties": {
                    "pokemon": {
                        "type": "object",
                        "required": ["name", "url"],
                        "properties": {
                            "name": {"type": "string", "examples": ["tentacool"]},
                            "url": {
                                "type": "string",
                                "format": "uri",
                                "examples": ["https://pokeapi.co/api/v2/pokemon/72/"],
                            },
                        },
                    },
                    "version_details": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["version", "max_chance", "encounter_details"],
                            "properties": {
                                "version": {
                                    "type": "object",
                                    "required": ["name", "url"],
                                    "properties": {
                                        "name": {
                                            "type": "string",
                                            "examples": ["diamond"],
                                        },
                                        "url": {
                                            "type": "string",
                                            "format": "uri",
                                            "examples": [
                                                "https://pokeapi.co/api/v2/version/12/"
                                            ],
                                        },
                                    },
                                },
                                "max_chance": {
                                    "type": "integer",
                                    "format": "int32",
                                    "examples": [60],
                                },
                                "encounter_details": {
                                    "type": "object",
                                    "required": [
                                        "min_level",
                                        "max_level",
                                        "condition_value",
                                        "chance",
                                        "method",
                                    ],
                                    "properties": {
                                        "min_level": {
                                            "type": "integer",
                                            "format": "int32",
                                            "examples": [20],
                                        },
                                        "max_level": {
                                            "type": "integer",
                                            "format": "int32",
                                            "examples": [30],
                                        },
                                        "condition_values": {
                                            "type": "object",
                                            "required": ["name", "url"],
                                            "properties": {
                                                "name": {
                                                    "type": "string",
                                                    "examples": ["slot2-sapphire"],
                                                },
                                                "url": {
                                                    "type": "string",
                                                    "format": "uri",
                                                    "examples": [
                                                        "https://pokeapi.co/api/v2/encounter-condition-value/10/"
                                                    ],
                                                },
                                            },
                                        },
                                        "chance": {
                                            "type": "integer",
                                            "format": "int32",
                                            "examples": [60],
                                        },
                                        "method": {
                                            "type": "object",
                                            "required": ["name", "url"],
                                            "properties": {
                                                "name": {
                                                    "type": "string",
                                                    "examples": ["surf"],
                                                },
                                                "url": {
                                                    "type": "string",
                                                    "format": "uri",
                                                    "examples": [
                                                        "https://pokeapi.co/api/v2/encounter-method/5/"
                                                    ],
                                                },
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        }
    )
    def get_encounters(self, obj):
        # get versions for later use
        version_objects = Version.objects.all()
        version_data = VersionSummarySerializer(
            version_objects, many=True, context=self.context
        ).data

        # all encounters associated with location area
        all_encounters = Encounter.objects.filter(location_area=obj).order_by("pokemon")
        encounters_list = []

        # break encounters into pokemon groupings
        for poke in all_encounters.values("pokemon").distinct():
            pokemon_object = Pokemon.objects.get(pk=poke["pokemon"])

            pokemon_detail = OrderedDict()
            pokemon_detail["pokemon"] = PokemonSummarySerializer(
                pokemon_object, context=self.context
            ).data
            pokemon_detail["version_details"] = []

            poke_encounters = all_encounters.filter(pokemon=poke["pokemon"]).order_by(
                "version"
            )

            # each pokemon has multiple versions it could be encountered in
            for ver in poke_encounters.values("version").distinct():
                version_detail = OrderedDict()
                version_detail["version"] = version_data[ver["version"] - 1]
                version_detail["max_chance"] = 0
                version_detail["encounter_details"] = []

                poke_data = EncounterDetailSerializer(
                    poke_encounters.filter(version=ver["version"]),
                    many=True,
                    context=self.context,
                ).data

                # each version has multiple ways a pokemon can be encountered
                for encounter in poke_data:
                    slot = EncounterSlot.objects.get(pk=encounter["encounter_slot"])
                    slot_data = EncounterSlotSerializer(slot, context=self.context).data
                    del encounter["pokemon"]
                    del encounter["encounter_slot"]
                    del encounter["location_area"]
                    del encounter["version"]
                    encounter["chance"] = slot_data["chance"]
                    version_detail["max_chance"] += slot_data["chance"]
                    encounter["method"] = slot_data["encounter_method"]

                    version_detail["encounter_details"].append(encounter)

                pokemon_detail["version_details"].append(version_detail)

            encounters_list.append(pokemon_detail)

        return encounters_list


class LocationGameIndexSerializer(serializers.ModelSerializer):
    generation = GenerationSummarySerializer()

    class Meta:
        model = LocationGameIndex
        fields = ("game_index", "generation")


class LocationNameSerializer(serializers.ModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = LocationName
        fields = ("name", "language")


class LocationDetailSerializer(serializers.ModelSerializer):
    region = RegionSummarySerializer()
    names = LocationNameSerializer(many=True, read_only=True, source="locationname")
    game_indices = LocationGameIndexSerializer(
        many=True, read_only=True, source="locationgameindex"
    )
    areas = LocationAreaSummarySerializer(
        many=True, read_only=True, source="locationarea"
    )

    class Meta:
        model = Location
        fields = ("id", "name", "region", "names", "game_indices", "areas")


#########################
#  ABILITY SERIALIZERS  #
#########################


class AbilityEffectTextSerializer(serializers.ModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = AbilityEffectText
        fields = ("effect", "short_effect", "language")


class AbilityFlavorTextSerializer(serializers.ModelSerializer):
    flavor_text = serializers.CharField()
    language = LanguageSummarySerializer()
    version_group = VersionGroupSummarySerializer()

    class Meta:
        model = AbilityFlavorText
        fields = ("flavor_text", "language", "version_group")


class AbilityChangeEffectTextSerializer(serializers.ModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = AbilityChangeEffectText
        fields = (
            "effect",
            "language",
        )


class AbilityChangeSerializer(serializers.ModelSerializer):
    version_group = VersionGroupSummarySerializer()
    effect_entries = AbilityChangeEffectTextSerializer(
        many=True, read_only=True, source="abilitychangeeffecttext"
    )

    class Meta:
        model = AbilityChange
        fields = ("version_group", "effect_entries")


class AbilityNameSerializer(serializers.ModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = AbilityName
        fields = ("name", "language")


class AbilityDetailSerializer(serializers.ModelSerializer):
    effect_entries = AbilityEffectTextSerializer(
        many=True, read_only=True, source="abilityeffecttext"
    )
    flavor_text_entries = AbilityFlavorTextSerializer(
        many=True, read_only=True, source="abilityflavortext"
    )
    names = AbilityNameSerializer(many=True, read_only=True, source="abilityname")
    generation = GenerationSummarySerializer()
    effect_changes = AbilityChangeSerializer(
        many=True, read_only=True, source="abilitychange"
    )
    pokemon = serializers.SerializerMethodField("get_ability_pokemon")

    class Meta:
        model = Ability
        fields = (
            "id",
            "name",
            "is_main_series",
            "generation",
            "names",
            "effect_entries",
            "effect_changes",
            "flavor_text_entries",
            "pokemon",
        )

    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["is_hidden", "slot", "pokemon"],
                "properties": {
                    "is_hidden": {"type": "boolean"},
                    "slot": {"type": "integer", "format": "int32", "examples": [3]},
                    "pokemon": {
                        "type": "object",
                        "required": ["name", "url"],
                        "properties": {
                            "name": {"type": "string", "examples": ["gloom"]},
                            "url": {
                                "type": "string",
                                "format": "uri",
                                "examples": ["https://pokeapi.co/api/v2/pokemon/44/"],
                            },
                        },
                    },
                },
            },
        }
    )
    def get_ability_pokemon(self, obj):
        pokemon_ability_objects = PokemonAbility.objects.filter(ability=obj)
        data = PokemonAbilitySerializer(
            pokemon_ability_objects, many=True, context=self.context
        ).data
        pokemon = []

        for poke in data:
            del poke["ability"]
            pokemon.append(poke)

        return pokemon


######################
#  STAT SERIALIZERS  #
######################


class StatNameSerializer(serializers.ModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = StatName
        fields = ("name", "language")


class StatDetailSerializer(serializers.ModelSerializer):
    names = StatNameSerializer(many=True, read_only=True, source="statname")
    move_damage_class = MoveDamageClassSummarySerializer()
    characteristics = CharacteristicSummarySerializer(
        many=True, read_only=True, source="characteristic"
    )
    affecting_moves = serializers.SerializerMethodField("get_moves_that_affect")
    affecting_natures = serializers.SerializerMethodField("get_natures_that_affect")
    affecting_items = serializers.SerializerMethodField("get_items_that_affect")

    class Meta:
        model = Stat
        fields = (
            "id",
            "name",
            "game_index",
            "is_battle_only",
            "affecting_moves",
            "affecting_natures",
            "affecting_items",
            "characteristics",
            "move_damage_class",
            "names",
        )

    @extend_schema_field(
        field={
            "type": "object",
            "required": ["decrease", "increase"],
            "properties": {
                "increase": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["change", "move"],
                        "properties": {
                            "change": {
                                "type": "integer",
                                "format": "int32",
                                "examples": [-1],
                            },
                            "move": {
                                "type": "object",
                                "required": ["name", "url"],
                                "properties": {
                                    "name": {
                                        "type": "string",
                                        "examples": ["swords-dance"],
                                    },
                                    "url": {
                                        "type": "string",
                                        "format": "uri",
                                        "examples": [
                                            "https://pokeapi.co/api/v2/move/14/"
                                        ],
                                    },
                                },
                            },
                        },
                    },
                },
                "decrease": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["change", "move"],
                        "properties": {
                            "change": {
                                "type": "integer",
                                "format": "int32",
                                "examples": [5],
                            },
                            "move": {
                                "type": "object",
                                "required": ["name", "url"],
                                "properties": {
                                    "name": {"type": "string", "examples": ["growl"]},
                                    "url": {
                                        "type": "string",
                                        "format": "uri",
                                        "examples": [
                                            "https://pokeapi.co/api/v2/move/45/"
                                        ],
                                    },
                                },
                            },
                        },
                    },
                },
            },
        }
    )
    def get_moves_that_affect(self, obj):
        stat_change_objects = MoveMetaStatChange.objects.filter(stat=obj)
        stat_changes = MoveMetaStatChangeSerializer(
            stat_change_objects, many=True, context=self.context
        ).data
        changes = OrderedDict([("increase", []), ("decrease", [])])

        for change in stat_changes:
            del change["stat"]
            if change["change"] > 0:
                changes["increase"].append(change)
            else:
                changes["decrease"].append(change)

        return changes

    @extend_schema_field(
        field={
            "type": "object",
            "required": ["increase", "decrease"],
            "properties": {
                "increase": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["name", "url"],
                        "properties": {
                            "name": {"type": "string", "examples": ["lonely"]},
                            "url": {
                                "type": "string",
                                "format": "uri",
                                "examples": ["https://pokeapi.co/api/v2/nature/6/"],
                            },
                        },
                    },
                },
                "decrease": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["name", "url"],
                        "properties": {
                            "name": {"type": "string", "examples": ["bold"]},
                            "url": {
                                "type": "string",
                                "format": "uri",
                                "examples": ["https://pokeapi.co/api/v2/nature/2/"],
                            },
                        },
                    },
                },
            },
        }
    )
    def get_natures_that_affect(self, obj):
        increase_objects = Nature.objects.filter(increased_stat=obj)
        increases = NatureSummarySerializer(
            increase_objects, many=True, context=self.context
        ).data
        decrease_objects = Nature.objects.filter(decreased_stat=obj)
        decreases = NatureSummarySerializer(
            decrease_objects, many=True, context=self.context
        ).data

        return OrderedDict([("increase", increases), ("decrease", decreases)])

    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name", "url"],
                "properties": {
                    "name": {
                        "type": "string",
                        "examples": ["protein", "x-attack"],
                    },
                    "url": {
                        "type": "string",
                        "format": "uri",
                        "examples": ["https://pokeapi.co/api/v2/item/46/"],
                    },
                },
            },
        }
    )
    def get_items_that_affect(self, obj):
        """
        Get items that affect this stat (like vitamins, X-items, etc.)
        """
        # Map stat names to their corresponding vitamin items
        stat_item_mapping = {
            "hp": ["hp-up"],
            "attack": ["protein"],
            "defense": ["iron"],
            "special-attack": ["calcium"],
            "special-defense": ["zinc"],
            "speed": ["carbos"],
        }

        # Get the stat name (lowercase)
        stat_name = obj.name.lower()

        # Find items that affect this stat
        affecting_items = []

        # Check for vitamin items
        if stat_name in stat_item_mapping:
            for item_identifier in stat_item_mapping[stat_name]:
                try:
                    item = Item.objects.get(name=item_identifier)
                    affecting_items.append(
                        ItemSummarySerializer(item, context=self.context).data
                    )
                except Item.DoesNotExist:
                    pass

        # Check for X-items (like X Attack, X Defense, etc.)
        x_item_mapping = {
            "attack": ["x-attack"],
            "defense": ["x-defense"],
            "special-attack": ["x-sp-atk"],
            "special-defense": ["x-sp-def"],
            "speed": ["x-speed"],
            "accuracy": ["x-accuracy"],
            "evasion": ["x-evasion"],
        }

        if stat_name in x_item_mapping:
            for item_identifier in x_item_mapping[stat_name]:
                try:
                    item = Item.objects.get(name=item_identifier)
                    affecting_items.append(
                        ItemSummarySerializer(item, context=self.context).data
                    )
                except Item.DoesNotExist:
                    pass

        return affecting_items


#############################
#  ITEM POCKET SERIALIZERS  #
#############################


class ItemPocketNameSerializer(serializers.ModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = ItemName
        fields = ("name", "language")


class ItemPocketDetailSerializer(serializers.ModelSerializer):
    names = ItemPocketNameSerializer(many=True, read_only=True, source="itempocketname")
    categories = ItemCategorySummarySerializer(
        many=True, read_only=True, source="itemcategory"
    )

    class Meta:
        model = ItemPocket
        fields = ("id", "name", "categories", "categories", "names")


###############################
#  ITEM CATEGORY SERIALIZERS  #
###############################
class ItemCategoryNameSerializer(serializers.ModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = ItemName
        fields = ("name", "language")


class ItemCategoryDetailSerializer(serializers.ModelSerializer):
    names = ItemCategoryNameSerializer(
        many=True, read_only=True, source="itemcategoryname"
    )
    pocket = ItemPocketSummarySerializer(source="item_pocket")
    items = ItemSummarySerializer(many=True, read_only=True, source="item")

    class Meta:
        model = ItemCategory
        fields = ("id", "name", "items", "names", "pocket")


################################
#  ITEM ATTRIBUTE SERIALIZERS  #
################################


class ItemAttributeNameSerializer(serializers.ModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = ItemAttributeName
        fields = ("name", "language")


class ItemAttributeDescriptionSerializer(serializers.ModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = ItemAttributeDescription
        fields = ("description", "language")


class ItemAttributeDetailSerializer(serializers.ModelSerializer):
    names = ItemAttributeNameSerializer(
        many=True, read_only=True, source="itemattributename"
    )
    descriptions = ItemAttributeDescriptionSerializer(
        many=True, read_only=True, source="itemattributedescription"
    )
    items = serializers.SerializerMethodField("get_attribute_items")

    class Meta:
        model = ItemAttribute
        fields = ("id", "name", "descriptions", "items", "names")

    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name", "url"],
                "properties": {
                    "name": {"type": "string", "examples": ["master-ball"]},
                    "url": {
                        "type": "string",
                        "format": "uri",
                        "examples": ["https://pokeapi.co/api/v2/item/1/"],
                    },
                },
            },
        }
    )
    def get_attribute_items(self, obj):
        item_map_objects = ItemAttributeMap.objects.filter(item_attribute=obj)
        items = []

        for map in item_map_objects:
            item_obj = Item.objects.get(pk=map.item.id)
            item = ItemSummarySerializer(item_obj, context=self.context).data
            items.append(item)

        return items


###################################
#  ITEM FLING EFFECT SERIALIZERS  #
###################################
class ItemFlingEffectEffectTextSerializer(serializers.ModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = ItemFlingEffectEffectText
        fields = ("effect", "language")


class ItemFlingEffectDetailSerializer(serializers.ModelSerializer):
    effect_entries = ItemFlingEffectEffectTextSerializer(
        many=True, read_only=True, source="itemflingeffecteffecttext"
    )
    items = ItemSummarySerializer(many=True, read_only=True, source="item")

    class Meta:
        model = ItemFlingEffect
        fields = ("id", "name", "effect_entries", "items")


#######################
#  ITEM  SERIALIZERS  #
#######################
class ItemFlavorTextSerializer(serializers.ModelSerializer):
    text = serializers.CharField(source="flavor_text")
    language = LanguageSummarySerializer()
    version_group = VersionGroupSummarySerializer()

    class Meta:
        model = ItemFlavorText
        fields = ("text", "version_group", "language")


class ItemEffectTextSerializer(serializers.ModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = ItemEffectText
        fields = ("effect", "short_effect", "language")


class ItemGameIndexSerializer(serializers.ModelSerializer):
    generation = GenerationSummarySerializer()

    class Meta:
        model = ItemGameIndex
        fields = ("game_index", "generation")


class ItemNameSerializer(serializers.ModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = ItemName
        fields = ("name", "language")


class ItemSpritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemSprites
        fields = ("sprites",)


class ItemDetailSerializer(serializers.ModelSerializer):
    names = ItemNameSerializer(many=True, read_only=True, source="itemname")
    game_indices = ItemGameIndexSerializer(
        many=True, read_only=True, source="itemgameindex"
    )
    effect_entries = ItemEffectTextSerializer(
        many=True, read_only=True, source="itemeffecttext"
    )
    flavor_text_entries = ItemFlavorTextSerializer(
        many=True, read_only=True, source="itemflavortext"
    )
    category = ItemCategorySummarySerializer(source="item_category")
    attributes = serializers.SerializerMethodField("get_item_attributes")
    fling_effect = ItemFlingEffectSummarySerializer(source="item_fling_effect")
    held_by_pokemon = serializers.SerializerMethodField(source="get_held_by_pokemon")
    baby_trigger_for = serializers.SerializerMethodField(source="get_baby_trigger_for")
    sprites = serializers.SerializerMethodField("get_item_sprites")
    machines = serializers.SerializerMethodField("get_item_machines")

    class Meta:
        model = Item
        fields = (
            "id",
            "name",
            "cost",
            "fling_power",
            "fling_effect",
            "attributes",
            "category",
            "effect_entries",
            "flavor_text_entries",
            "game_indices",
            "names",
            "held_by_pokemon",
            "sprites",
            "baby_trigger_for",
            "machines",
        )

    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["machine", "version_group"],
                "properties": {
                    "machine": {
                        "type": "string",
                        "format": "uri",
                        "examples": ["https://pokeapi.co/api/v2/machine/1/"],
                    },
                    "version_group": {
                        "type": "object",
                        "required": ["name", "url"],
                        "properties": {
                            "name": {"type": "string", "examples": ["sword-shield"]},
                            "url": {
                                "type": "string",
                                "format": "uri",
                                "examples": [
                                    "https://pokeapi.co/api/v2/version-group/20/"
                                ],
                            },
                        },
                    },
                },
            },
        }
    )
    def get_item_machines(self, obj):
        machine_objects = Machine.objects.filter(item=obj)

        machines = []

        for machine_object in machine_objects:
            machine_data = MachineSummarySerializer(
                machine_object, context=self.context
            ).data

            version_group_data = VersionGroupSummarySerializer(
                machine_object.version_group, context=self.context
            ).data

            machines.append(
                {"machine": machine_data, "version_group": version_group_data}
            )

        return machines

    @extend_schema_field(
        field={
            "type": "object",
            "required": ["default"],
            "properties": {
                "default": {
                    "type": "string",
                    "format": "uri",
                    "examples": [
                        "https://pokeapi.co/media/sprites/items/master-ball.png"
                    ],
                }
            },
        }
    )
    def get_item_sprites(self, obj):
        sprites_object = ItemSprites.objects.get(item_id=obj)
        return sprites_object.sprites

    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name", "url"],
                "properties": {
                    "name": {"type": "string", "examples": ["countable"]},
                    "url": {
                        "type": "string",
                        "format": "uri",
                        "examples": ["https://pokeapi.co/api/v2/item-attribute/1/"],
                    },
                },
            },
        }
    )
    def get_item_attributes(self, obj):
        item_attribute_maps = ItemAttributeMap.objects.filter(item=obj)
        serializer = ItemAttributeMapSerializer(
            item_attribute_maps, many=True, context=self.context
        )
        data = serializer.data

        attributes = []

        for map in data:
            attribute = OrderedDict()
            attribute["name"] = map["attribute"]["name"]
            attribute["url"] = map["attribute"]["url"]
            attributes.append(attribute)

        return attributes

    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["pokemon", "version-details"],
                "properties": {
                    "pokemon": {
                        "type": "object",
                        "required": ["name", "url"],
                        "properties": {
                            "name": {"type": "string", "examples": ["farfetchd"]},
                            "url": {
                                "type": "string",
                                "format": "uri",
                                "examples": ["https://pokeapi.co/api/v2/pokemon/83/"],
                            },
                        },
                    },
                    "version-details": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["rarity", "version"],
                            "properties": {
                                "rarity": {
                                    "type": "integer",
                                    "format": "int32",
                                    "examples": [5],
                                },
                                "version": {
                                    "type": "object",
                                    "required": ["name", "url"],
                                    "properties": {
                                        "name": {
                                            "type": "string",
                                            "examples": ["ruby"],
                                        },
                                        "url": {
                                            "type": "string",
                                            "format": "uri",
                                            "examples": [
                                                "https://pokeapi.co/api/v2/version/7/"
                                            ],
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        }
    )
    def get_held_by_pokemon(self, obj):
        pokemon_items = PokemonItem.objects.filter(item=obj).order_by("pokemon_id")
        pokemon_ids = pokemon_items.values("pokemon_id").distinct()
        pokemon_list = []

        for id in pokemon_ids:
            item_pokemon_details = OrderedDict()

            # Get each Unique Item by ID
            pokemon_object = Pokemon.objects.get(pk=id["pokemon_id"])
            pokemon_data = PokemonSummarySerializer(
                pokemon_object, context=self.context
            ).data
            item_pokemon_details["pokemon"] = pokemon_data

            # Get Versions associated with each unique item
            pokemon_item_objects = pokemon_items.filter(pokemon_id=id["pokemon_id"])
            serializer = PokemonItemSerializer(
                pokemon_item_objects, many=True, context=self.context
            )
            item_pokemon_details["version_details"] = []

            for pokemon in serializer.data:
                version_detail = OrderedDict()
                version_detail["rarity"] = pokemon["rarity"]
                version_detail["version"] = pokemon["version"]
                item_pokemon_details["version_details"].append(version_detail)

            pokemon_list.append(item_pokemon_details)

        return pokemon_list

    @extend_schema_field(
        field={
            "type": "object",
            "required": ["url"],
            "properties": {
                "url": {
                    "type": "string",
                    "format": "uri",
                    "examples": ["https://pokeapi.co/api/v2/evolution-chain/51/"],
                }
            },
        }
    )
    def get_baby_trigger_for(self, obj):
        try:
            chain_object = EvolutionChain.objects.get(baby_trigger_item=obj)
            data = EvolutionChainSummarySerializer(
                chain_object, context=self.context
            ).data
        except EvolutionChain.DoesNotExist:
            data = None

        return data


########################
#  NATURE SERIALIZERS  #
########################


class NatureBattleStylePreferenceSerializer(serializers.ModelSerializer):
    move_battle_style = MoveBattleStyleSummarySerializer()

    class Meta:
        model = NatureBattleStylePreference
        fields = (
            "low_hp_preference",
            "high_hp_preference",
            "move_battle_style",
        )


class NatureNameSerializer(serializers.ModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = NatureName
        fields = ("name", "language")


class NatureDetailSerializer(serializers.ModelSerializer):
    names = NatureNameSerializer(many=True, read_only=True, source="naturename")
    decreased_stat = StatSummarySerializer()
    increased_stat = StatSummarySerializer()
    likes_flavor = BerryFlavorSummarySerializer()
    hates_flavor = BerryFlavorSummarySerializer()
    berries = BerrySummarySerializer(many=True, read_only=True, source="berry")
    pokeathlon_stat_changes = serializers.SerializerMethodField("get_pokeathlon_stats")
    move_battle_style_preferences = NatureBattleStylePreferenceSerializer(
        many=True, read_only=True, source="naturebattlestylepreference"
    )

    class Meta:
        model = Nature
        fields = (
            "id",
            "name",
            "decreased_stat",
            "increased_stat",
            "likes_flavor",
            "hates_flavor",
            "berries",
            "pokeathlon_stat_changes",
            "move_battle_style_preferences",
            "names",
        )

    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["max_change", "pokeathlon_stat"],
                "properties": {
                    "max_change": {
                        "type": "integer",
                        "format": "int32",
                        "examples": [1],
                    },
                    "pokeathlon_stat": {
                        "type": "object",
                        "required": ["name", "url"],
                        "properties": {
                            "name": {"type": "string", "examples": ["power"]},
                            "url": {
                                "type": "string",
                                "format": "uri",
                                "examples": [
                                    "https://pokeapi.co/api/v2/pokeathlon-stat/2/"
                                ],
                            },
                        },
                    },
                },
            },
        }
    )
    def get_pokeathlon_stats(self, obj):
        pokeathlon_stat_objects = NaturePokeathlonStat.objects.filter(nature=obj)
        pokeathlon_stats = NaturePokeathlonStatSerializer(
            pokeathlon_stat_objects, many=True, context=self.context
        ).data

        for stat in pokeathlon_stats:
            del stat["nature"]

        return pokeathlon_stats


#######################
#  BERRY SERIALIZERS  #
#######################


class BerryFirmnessNameSerializer(serializers.ModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = BerryFirmnessName
        fields = ("name", "language")


class BerryFirmnessDetailSerializer(serializers.ModelSerializer):
    names = BerryFirmnessNameSerializer(
        many=True, read_only=True, source="berryfirmnessname"
    )
    berries = BerrySummarySerializer(many=True, read_only=True, source="berry")

    class Meta:
        model = BerryFirmness
        fields = ("id", "name", "berries", "names")


class BerryFlavorNameSerializer(serializers.ModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = BerryFlavorName
        fields = ("name", "language")


class BerryFlavorDetailSerializer(serializers.ModelSerializer):
    names = BerryFlavorNameSerializer(
        many=True, read_only=True, source="berryflavorname"
    )
    contest_type = ContestTypeSummarySerializer()
    berries = serializers.SerializerMethodField("get_berries_with_flavor")

    class Meta:
        model = BerryFlavor
        fields = ("id", "name", "berries", "contest_type", "names")

    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["potency", "berry"],
                "properties": {
                    "potency": {"type": "integer", "examples": [10]},
                    "berry": {
                        "type": "object",
                        "require": ["name", "url"],
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "The name of the berry",
                                "examples": ["rowap"],
                            },
                            "url": {
                                "type": "string",
                                "format": "uri",
                                "description": "The URL to get more information about the berry",
                                "examples": ["https://pokeapi.co/api/v2/berry/64/"],
                            },
                        },
                    },
                },
            },
        }
    )
    def get_berries_with_flavor(self, obj):
        flavor_map_objects = BerryFlavorMap.objects.filter(
            berry_flavor=obj, potency__gt=0
        ).order_by("potency")
        flavor_maps = BerryFlavorMapSerializer(
            flavor_map_objects, many=True, context=self.context
        ).data

        for map in flavor_maps:
            del map["flavor"]

        return flavor_maps


class BerryDetailSerializer(serializers.ModelSerializer):
    item = ItemSummarySerializer()
    natural_gift_type = TypeSummarySerializer()
    firmness = BerryFirmnessSummarySerializer(source="berry_firmness")
    flavors = serializers.SerializerMethodField("get_berry_flavors")

    class Meta:
        model = Berry
        fields = (
            "id",
            "name",
            "growth_time",
            "max_harvest",
            "natural_gift_power",
            "size",
            "smoothness",
            "soil_dryness",
            "firmness",
            "flavors",
            "item",
            "natural_gift_type",
        )

    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["potency", "flavor"],
                "properties": {
                    "potency": {"type": "integer", "examples": [10]},
                    "flavor": {
                        "type": "object",
                        "require": ["name", "url"],
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "The name of the flavor",
                                "examples": ["spicy"],
                            },
                            "url": {
                                "type": "string",
                                "format": "uri",
                                "description": "The URL to get more information about the flavor",
                                "examples": [
                                    "https://pokeapi.co/api/v2/berry-flavor/1/"
                                ],
                            },
                        },
                    },
                },
            },
        }
    )
    def get_berry_flavors(self, obj):
        flavor_map_objects = BerryFlavorMap.objects.filter(berry=obj)
        flavor_maps = BerryFlavorMapSerializer(
            flavor_map_objects, many=True, context=self.context
        ).data
        flavors = []

        for map in flavor_maps:
            del map["berry"]
            flavors.append(map)

        return flavors


###########################
#  EGG GROUP SERIALIZERS  #
###########################
class PokemonEggGroupSerializer(serializers.ModelSerializer):
    species = PokemonSpeciesSummarySerializer(source="pokemon_species")
    egg_group = EggGroupSummarySerializer()

    class Meta:
        model = PokemonEggGroup
        fields = ("species", "egg_group")


class EggGroupNameSerializer(serializers.ModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = EggGroupName
        fields = ("name", "language")


class EggGroupDetailSerializer(serializers.ModelSerializer):
    names = EggGroupNameSerializer(many=True, read_only=True, source="egggroupname")
    pokemon_species = serializers.SerializerMethodField("get_species")

    class Meta:
        model = EggGroup
        fields = ("id", "name", "names", "pokemon_species")

    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["potency", "flavor"],
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Pokemon species name.",
                        "examples": ["bulbasaur"],
                    },
                    "url": {
                        "type": "string",
                        "format": "uri",
                        "description": "The URL to get more information about the species",
                        "examples": ["https://pokeapi.co/api/v2/pokemon-species/1/"],
                    },
                },
            },
        }
    )
    def get_species(self, obj):
        results = PokemonEggGroup.objects.filter(egg_group=obj)
        data = PokemonEggGroupSerializer(results, many=True, context=self.context).data
        associated_species = []
        for species in data:
            associated_species.append(species["species"])

        return associated_species


######################
#  TYPE SERIALIZERS  #
######################
# https://stackoverflow.com/a/45987450/3482533
class TypeEfficacySerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeEfficacy
        fields = "__all__"


class TypeEfficacyPastSerializer(serializers.ModelSerializer):
    generation = GenerationSummarySerializer()

    class Meta:
        model = TypeEfficacyPast
        fields = ("target_type", "damage_type", "damage_factor", "generation")


class TypeGameIndexSerializer(serializers.ModelSerializer):
    generation = GenerationSummarySerializer()

    class Meta:
        model = TypeGameIndex
        fields = ("game_index", "generation")


class TypeNameSerializer(serializers.ModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = TypeName
        fields = ("name", "language")


class TypeSpriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeSprites
        fields = ("sprites",)


class TypeDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for the Type resource
    """

    generation = GenerationSummarySerializer()
    names = AbilityNameSerializer(many=True, read_only=True, source="typename")
    game_indices = TypeGameIndexSerializer(
        many=True, read_only=True, source="typegameindex"
    )
    move_damage_class = MoveDamageClassSummarySerializer()
    damage_relations = serializers.SerializerMethodField("get_type_relationships")
    past_damage_relations = serializers.SerializerMethodField(
        "get_type_past_relationships"
    )
    pokemon = serializers.SerializerMethodField("get_type_pokemon")
    moves = MoveSummarySerializer(many=True, read_only=True, source="move")
    sprites = serializers.SerializerMethodField("get_type_sprites")

    class Meta:
        model = Type
        fields = (
            "id",
            "name",
            "damage_relations",
            "past_damage_relations",
            "game_indices",
            "generation",
            "move_damage_class",
            "names",
            "pokemon",
            "moves",
            "sprites",
        )

    @extend_schema_field(
        field={
            "type": "object",
            "additionalProperties": {
                "type": "object",
                "additionalProperties": {
                    "type": "object",
                    "properties": {
                        "name-icon": {
                            "type": "string",
                            "format": "uri",
                            "examples": [
                                "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/types/generation-iii/colosseum/1.png"
                            ],
                        }
                    },
                    "examples": [
                        {
                            "colosseum": {
                                "name_icon": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/types/generation-iii/colosseum/1.png"
                            }
                        }
                    ],
                },
                "examples": [
                    {
                        "generation-ix": {
                            "scarlet-violet": {
                                "name_icon": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/types/generation-ix/scarlet-violet/1.png"
                            }
                        }
                    }
                ],
            },
            "examples": [
                {
                    "sprites": {
                        "generation-iii": {
                            "colosseum": {
                                "name_icon": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/types/generation-iii/colosseum/1.png"
                            },
                            "emerald": {
                                "name_icon": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/types/generation-iii/emerald/1.png"
                            },
                            "firered-leafgreen": {
                                "name_icon": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/types/generation-iii/firered-leafgreen/1.png"
                            },
                            "ruby-sapphire": {
                                "name_icon": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/types/generation-iii/ruby-sapphire/1.png"
                            },
                            "xd": {
                                "name_icon": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/types/generation-iii/xd/1.png"
                            },
                        }
                    }
                }
            ],
        }
    )
    def get_type_sprites(self, obj):
        sprites_object = TypeSprites.objects.get(type_id=obj)
        return sprites_object.sprites

    # adds an entry for the given type with the given damage
    # factor in the given direction to the set of relations

    def add_type_entry(self, relations, type, damage_factor, direction="_damage_to"):
        if damage_factor == 200:
            relations["double" + direction].append(
                TypeSummarySerializer(type, context=self.context).data
            )
        elif damage_factor == 50:
            relations["half" + direction].append(
                TypeSummarySerializer(type, context=self.context).data
            )
        elif damage_factor == 0:
            relations["no" + direction].append(
                TypeSummarySerializer(type, context=self.context).data
            )

    @extend_schema_field(
        field={
            "type": "object",
            "required": [
                "no_damage_to",
                "half_damage_to",
                "double_damage_to",
                "no_damage_from",
                "half_damage_from",
                "double_damage_from",
            ],
            "properties": {
                "no_damage_to": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["name", "url"],
                        "properties": {
                            "name": {"type": "string", "examples": ["flying"]},
                            "url": {
                                "type": "string",
                                "format": "uri",
                                "examples": ["https://pokeapi.co/api/v2/type/3/"],
                            },
                        },
                    },
                },
                "half_damage_to": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["name", "url"],
                        "properties": {
                            "name": {"type": "string", "examples": ["bug"]},
                            "url": {
                                "type": "string",
                                "format": "uri",
                                "examples": ["https://pokeapi.co/api/v2/type/7/"],
                            },
                        },
                    },
                },
                "double_damage_to": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["name", "url"],
                        "properties": {
                            "name": {"type": "string", "examples": ["poison"]},
                            "url": {
                                "type": "string",
                                "format": "uri",
                                "examples": ["https://pokeapi.co/api/v2/type/4/"],
                            },
                        },
                    },
                },
                "no_damage_from": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["name", "url"],
                        "properties": {
                            "name": {"type": "string", "examples": ["electric"]},
                            "url": {
                                "type": "string",
                                "format": "uri",
                                "examples": ["https://pokeapi.co/api/v2/type/13/"],
                            },
                        },
                    },
                },
                "half_damage_from": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["name", "url"],
                        "properties": {
                            "name": {"type": "string", "examples": ["poison"]},
                            "url": {
                                "type": "string",
                                "format": "uri",
                                "examples": ["https://pokeapi.co/api/v2/type/4/"],
                            },
                        },
                    },
                },
                "double_damage_from": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["name", "url"],
                        "properties": {
                            "name": {"type": "string", "examples": ["water"]},
                            "url": {
                                "type": "string",
                                "format": "uri",
                                "examples": ["https://pokeapi.co/api/v2/type/11/"],
                            },
                        },
                    },
                },
            },
        }
    )
    def get_type_relationships(self, obj):
        relations = OrderedDict()
        relations["no_damage_to"] = []
        relations["half_damage_to"] = []
        relations["double_damage_to"] = []

        relations["no_damage_from"] = []
        relations["half_damage_from"] = []
        relations["double_damage_from"] = []

        # Damage To
        results = TypeEfficacy.objects.filter(damage_type=obj)
        serializer = TypeEfficacySerializer(results, many=True, context=self.context)

        for relation in serializer.data:
            type = Type.objects.get(pk=relation["target_type"])
            damage_factor = relation["damage_factor"]
            self.add_type_entry(relations, type, damage_factor, direction="_damage_to")

        # Damage From
        results = TypeEfficacy.objects.filter(target_type=obj)
        serializer = TypeEfficacySerializer(results, many=True, context=self.context)

        for relation in serializer.data:
            type = Type.objects.get(pk=relation["damage_type"])
            damage_factor = relation["damage_factor"]
            self.add_type_entry(
                relations, type, damage_factor, direction="_damage_from"
            )

        return relations

    # takes a list of past type relations by generation and
    # returns a list of lists where each list has the entries
    # for a single generation
    def group_relations_by_generation(self, serializer_data):
        data_by_gen = []

        current_generation = ""
        generation_data = []
        for relation in serializer_data:
            gen_name = relation["generation"]["name"]
            if gen_name != current_generation:
                # first item for this generation so create its list
                current_generation = gen_name
                generation_data = [relation]
                data_by_gen.append(generation_data)
            else:
                # add to this generation's list
                generation_data.append(relation)

        return data_by_gen

    # removes the entry for the given type in
    # the given direction from the set of relations
    def remove_type_entry(self, relations, type, direction="_damage_to"):
        for k in ["double", "half", "no"]:
            rel_list = relations[k + direction]
            for i, o in enumerate(rel_list):
                if o["name"] == type.name:
                    del rel_list[i]
                    return

    # returns past type relationships for the given type object
    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["generation", "damage_relations"],
                "properties": {
                    "generation": {
                        "type": "object",
                        "required": ["name", "url"],
                        "properties": {
                            "name": {"type": "string", "examples": ["generation-v"]},
                            "url": {
                                "type": "string",
                                "format": "uri",
                                "examples": ["https://pokeapi.co/api/v2/generation/5/"],
                            },
                        },
                    },
                    "damage_relations": {
                        "type": "object",
                        "required": [
                            "no_damage_to",
                            "half_damage_to",
                            "double_damage_to",
                            "no_damage_from",
                            "half_damage_from",
                            "double_damage_from",
                        ],
                        "properties": {
                            "no_damage_to": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "required": ["name", "url"],
                                    "properties": {
                                        "name": {
                                            "type": "string",
                                            "examples": ["flying"],
                                        },
                                        "url": {
                                            "type": "string",
                                            "format": "uri",
                                            "examples": [
                                                "https://pokeapi.co/api/v2/type/3/"
                                            ],
                                        },
                                    },
                                },
                            },
                            "half_damage_to": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "required": ["name", "url"],
                                    "properties": {
                                        "name": {"type": "string", "examples": ["bug"]},
                                        "url": {
                                            "type": "string",
                                            "format": "uri",
                                            "examples": [
                                                "https://pokeapi.co/api/v2/type/7/"
                                            ],
                                        },
                                    },
                                },
                            },
                            "double_damage_to": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "required": ["name", "url"],
                                    "properties": {
                                        "name": {
                                            "type": "string",
                                            "examples": ["poison"],
                                        },
                                        "url": {
                                            "type": "string",
                                            "format": "uri",
                                            "examples": [
                                                "https://pokeapi.co/api/v2/type/4/"
                                            ],
                                        },
                                    },
                                },
                            },
                            "no_damage_from": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "required": ["name", "url"],
                                    "properties": {
                                        "name": {
                                            "type": "string",
                                            "examples": ["electric"],
                                        },
                                        "url": {
                                            "type": "string",
                                            "format": "uri",
                                            "examples": [
                                                "https://pokeapi.co/api/v2/type/13/"
                                            ],
                                        },
                                    },
                                },
                            },
                            "half_damage_from": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "required": ["name", "url"],
                                    "properties": {
                                        "name": {
                                            "type": "string",
                                            "examples": ["poison"],
                                        },
                                        "url": {
                                            "type": "string",
                                            "format": "uri",
                                            "examples": [
                                                "https://pokeapi.co/api/v2/type/4/"
                                            ],
                                        },
                                    },
                                },
                            },
                            "double_damage_from": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "required": ["name", "url"],
                                    "properties": {
                                        "name": {
                                            "type": "string",
                                            "examples": ["water"],
                                        },
                                        "url": {
                                            "type": "string",
                                            "format": "uri",
                                            "examples": [
                                                "https://pokeapi.co/api/v2/type/11/"
                                            ],
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        }
    )
    def get_type_past_relationships(self, obj):
        # collect data from DB
        damage_type_results = list(TypeEfficacyPast.objects.filter(damage_type=obj))
        target_type_results = list(TypeEfficacyPast.objects.filter(target_type=obj))
        serializer = TypeEfficacyPastSerializer(
            damage_type_results + target_type_results, many=True, context=self.context
        )

        # group data by generation
        data_by_gen = self.group_relations_by_generation(serializer.data)

        # process each generation's data in turn
        final_data = []
        past_relations = {}
        for gen_data in data_by_gen:
            # create past relations object for this generation
            past_relations = OrderedDict()

            # set generation
            past_relations["generation"] = gen_data[0]["generation"]

            # use current damage relations object
            past_relations["damage_relations"] = self.get_type_relationships(obj)
            relations = past_relations["damage_relations"]

            current_gen = Generation.objects.get(name=gen_data[0]["generation"]["name"])

            # remove types not yet introduced
            # e.g. Poison has no effect on Steel, but Steel was not present in generation I
            # so it should be absent from the list
            relations["no_damage_to"] = self.remove_newer_types(
                relations["no_damage_to"], current_gen
            )
            relations["half_damage_to"] = self.remove_newer_types(
                relations["half_damage_to"], current_gen
            )
            relations["double_damage_to"] = self.remove_newer_types(
                relations["double_damage_to"], current_gen
            )
            relations["no_damage_from"] = self.remove_newer_types(
                relations["no_damage_from"], current_gen
            )
            relations["half_damage_from"] = self.remove_newer_types(
                relations["half_damage_from"], current_gen
            )
            relations["double_damage_from"] = self.remove_newer_types(
                relations["double_damage_from"], current_gen
            )

            # populate offensive relations
            results = list(filter(lambda x: x["damage_type"] == obj.id, gen_data))
            for relation in results:
                type = Type.objects.get(pk=relation["target_type"])

                # remove conflicting entry if it exists
                self.remove_type_entry(relations, type, direction="_damage_to")

                # add entry
                damage_factor = relation["damage_factor"]
                self.add_type_entry(
                    relations, type, damage_factor, direction="_damage_to"
                )

                del relation["generation"]

            # populate defensive relations
            results = list(filter(lambda x: x["target_type"] == obj.id, gen_data))
            for relation in results:
                type = Type.objects.get(pk=relation["damage_type"])

                # remove conflicting entry if it exists
                self.remove_type_entry(relations, type, direction="_damage_from")

                # add entry
                damage_factor = relation["damage_factor"]
                self.add_type_entry(
                    relations, type, damage_factor, direction="_damage_from"
                )

                del relation["generation"]

            # add to final list
            final_data.append(past_relations)

        return final_data

    def remove_newer_types(self, relations, current_gen):
        return list(filter(lambda x: self.type_is_present(x, current_gen), relations))

    def type_is_present(self, type, current_gen):
        type_obj = Type.objects.get(name=type["name"])
        gen_introduced = Generation.objects.get(pk=type_obj.generation.id)
        return gen_introduced.id <= current_gen.id

    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["potency", "flavor"],
                "properties": {
                    "slot": {"type": "integer", "examples": [1]},
                    "pokemon": {
                        "type": "object",
                        "require": ["name", "url"],
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "The name of the pokemon",
                                "examples": ["sandshrew"],
                            },
                            "url": {
                                "type": "string",
                                "format": "uri",
                                "description": "The URL to get more information about the pokemon",
                                "examples": ["https://pokeapi.co/api/v2/pokemon/27/"],
                            },
                        },
                    },
                },
            },
        }
    )
    def get_type_pokemon(self, obj):
        poke_type_objects = PokemonType.objects.filter(type=obj)
        poke_types = PokemonTypeSerializer(
            poke_type_objects, many=True, context=self.context
        ).data

        for poke_type in poke_types:
            del poke_type["type"]

        return poke_types


#########################
#  MACHINE SERIALIZERS  #
#########################
class MachineDetailSerializer(serializers.ModelSerializer):
    item = ItemSummarySerializer()
    version_group = VersionGroupSummarySerializer()
    move = MoveSummarySerializer()

    class Meta:
        model = Machine
        fields = ("id", "item", "version_group", "move")


###################################
#  MOVE BATTLE STYLE SERIALIZERS  #
###################################
class MoveBattleStyleNameSerializer(serializers.ModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = MoveBattleStyleName
        fields = ("name", "language")


class MoveBattleStyleDetailSerializer(serializers.ModelSerializer):
    names = MoveBattleStyleNameSerializer(
        many=True, read_only=True, source="movebattlestylename"
    )

    class Meta:
        model = MoveBattleStyle
        fields = ("id", "name", "names")


###################################
#  MOVE DAMAGE CLASS SERIALIZERS  #
###################################
class MoveDamageClassNameSerializer(serializers.ModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = MoveDamageClassName
        fields = ("name", "language")


class MoveDamageClassDescriptionSerializer(serializers.ModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = MoveDamageClassDescription
        fields = ("description", "language")


class MoveDamageClassDetailSerializer(serializers.ModelSerializer):
    names = MoveDamageClassNameSerializer(
        many=True, read_only=True, source="movedamageclassname"
    )
    descriptions = MoveDamageClassDescriptionSerializer(
        many=True, read_only=True, source="movedamageclassdescription"
    )
    moves = MoveSummarySerializer(many=True, read_only=True, source="move")

    class Meta:
        model = MoveDamageClass
        fields = (
            "id",
            "name",
            "descriptions",
            "moves",
            "names",
        )


###########################
#  MOVE META SERIALIZERS  #
###########################
class MoveMetaAilmentNameSerializer(serializers.ModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = MoveMetaAilmentName
        fields = ("name", "language")


class MoveMetaAilmentDetailSerializer(serializers.ModelSerializer):
    names = MoveMetaAilmentNameSerializer(
        many=True, read_only=True, source="movemetaailmentname"
    )
    moves = serializers.SerializerMethodField("get_ailment_moves")

    class Meta:
        model = MoveMetaAilment
        fields = ("id", "name", "moves", "names")

    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name", "url"],
                "properties": {
                    "name": {"type": "string", "examples": ["thunder-punch"]},
                    "url": {
                        "type": "string",
                        "format": "uri",
                        "examples": ["https://pokeapi.co/api/v2/move/9/"],
                    },
                },
            },
        }
    )
    def get_ailment_moves(self, obj):
        move_meta_objects = MoveMeta.objects.filter(move_meta_ailment=obj)
        moves = []

        for meta in move_meta_objects:
            move_obj = Move.objects.get(pk=meta.move.id)
            data = MoveSummarySerializer(move_obj, context=self.context).data
            moves.append(data)

        return moves


class MoveMetaCategoryDescriptionSerializer(serializers.ModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = MoveMetaCategoryDescription
        fields = ("description", "language")


class MoveMetaCategoryDetailSerializer(serializers.ModelSerializer):
    descriptions = MoveMetaCategoryDescriptionSerializer(
        many=True, read_only=True, source="movemetacategorydescription"
    )
    moves = serializers.SerializerMethodField("get_category_moves")

    class Meta:
        model = MoveMetaCategory
        fields = ("id", "name", "descriptions", "moves")

    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name", "url"],
                "properties": {
                    "name": {"type": "string", "examples": ["sing"]},
                    "url": {
                        "type": "string",
                        "format": "uri",
                        "examples": ["https://pokeapi.co/api/v2/move/47/"],
                    },
                },
            },
        }
    )
    def get_category_moves(self, obj):
        move_meta_objects = MoveMeta.objects.filter(move_meta_category=obj)
        moves = []

        for meta in move_meta_objects:
            move_obj = Move.objects.get(pk=meta.move.id)
            data = MoveSummarySerializer(move_obj, context=self.context).data
            moves.append(data)

        return moves


class MoveMetaSerializer(serializers.ModelSerializer):
    ailment = MoveMetaAilmentSummarySerializer(source="move_meta_ailment")
    category = MoveMetaCategorySummarySerializer(source="move_meta_category")

    class Meta:
        model = MoveMeta
        fields = (
            "ailment",
            "category",
            "min_hits",
            "max_hits",
            "min_turns",
            "max_turns",
            "drain",
            "healing",
            "crit_rate",
            "ailment_chance",
            "flinch_chance",
            "stat_chance",
        )


#############################
#  MOVE TARGET SERIALIZERS  #
#############################
class MoveTargetNameSerializer(serializers.ModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = MoveTargetName
        fields = ("name", "language")


class MoveTargetDescriptionSerializer(serializers.ModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = MoveTargetDescription
        fields = ("description", "language")


class MoveTargetDetailSerializer(serializers.ModelSerializer):
    names = MoveTargetNameSerializer(many=True, read_only=True, source="movetargetname")
    descriptions = MoveTargetDescriptionSerializer(
        many=True, read_only=True, source="movetargetdescription"
    )
    moves = MoveSummarySerializer(many=True, read_only=True, source="move")

    class Meta:
        model = MoveTarget
        fields = ("id", "name", "descriptions", "moves", "names")


######################
#  MOVE SERIALIZERS  #
######################
class MoveNameSerializer(serializers.ModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = AbilityName
        fields = ("name", "language")


class MoveChangeSerializer(serializers.ModelSerializer):
    version_group = VersionGroupSummarySerializer()
    type = TypeSummarySerializer()
    effect_entries = serializers.SerializerMethodField("get_effects")
    effect_chance = serializers.IntegerField(source="move_effect_chance")

    class Meta:
        model = MoveChange
        fields = (
            "accuracy",
            "power",
            "pp",
            "effect_chance",
            "effect_entries",
            "type",
            "version_group",
        )

    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["effect", "short_effect", "language"],
                "properties": {
                    "effect": {
                        "type": "string",
                        "examples": [
                            "Inflicts [regular damage]{mechanic:regular-damage}."
                        ],
                    },
                    "short_effect": {
                        "type": "string",
                        "examples": [
                            "Inflicts regular damage with no additional effect."
                        ],
                    },
                    "language": {
                        "type": "object",
                        "required": ["name", "url"],
                        "properties": {
                            "name": {"type": "string", "examples": ["en"]},
                            "url": {
                                "type": "string",
                                "format": "uri",
                                "examples": ["https://pokeapi.co/api/v2/language/9/"],
                            },
                        },
                    },
                },
            },
        }
    )
    def get_effects(self, obj):
        effect_texts = MoveEffectEffectText.objects.filter(move_effect=obj.move_effect)
        data = MoveEffectEffectTextSerializer(
            effect_texts, many=True, context=self.context
        ).data

        return data


class MoveEffectEffectTextSerializer(serializers.ModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = MoveEffectEffectText
        fields = ("effect", "short_effect", "language")


class MoveEffectChangeEffectTextSerializer(serializers.ModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = MoveEffectChangeEffectText
        fields = ("effect", "language")


class MoveEffectChangeSerializer(serializers.ModelSerializer):
    version_group = VersionGroupSummarySerializer()
    effect_entries = MoveEffectChangeEffectTextSerializer(
        many=True, read_only=True, source="moveeffectchangeeffecttext"
    )

    class Meta:
        model = MoveEffectChange
        fields = ("version_group", "effect_entries")


class MoveFlavorTextSerializer(serializers.ModelSerializer):
    flavor_text = serializers.CharField()
    language = LanguageSummarySerializer()
    version_group = VersionGroupSummarySerializer()

    class Meta:
        model = MoveFlavorText
        fields = ("flavor_text", "language", "version_group")


class MoveDetailSerializer(serializers.ModelSerializer):
    generation = GenerationSummarySerializer()
    type = TypeSummarySerializer()
    target = MoveTargetSummarySerializer(source="move_target")
    contest_type = ContestTypeSummarySerializer()
    contest_effect = ContestEffectSummarySerializer()
    damage_class = MoveDamageClassSummarySerializer(source="move_damage_class")
    meta = MoveMetaSerializer(read_only=True, source="movemeta")
    names = MoveNameSerializer(many=True, read_only=True, source="movename")
    effect_entries = serializers.SerializerMethodField("get_effect_text")
    effect_chance = serializers.IntegerField(source="move_effect_chance")
    contest_combos = serializers.SerializerMethodField("get_combos")
    stat_changes = serializers.SerializerMethodField("get_move_stat_change")
    super_contest_effect = SuperContestEffectSummarySerializer()
    past_values = MoveChangeSerializer(many=True, read_only=True, source="movechange")
    effect_changes = serializers.SerializerMethodField("get_effect_change_text")
    machines = serializers.SerializerMethodField("get_move_machines")
    flavor_text_entries = MoveFlavorTextSerializer(
        many=True, read_only=True, source="moveflavortext"
    )
    learned_by_pokemon = serializers.SerializerMethodField()

    class Meta:
        model = Move
        fields = (
            "id",
            "name",
            "accuracy",
            "effect_chance",
            "pp",
            "priority",
            "power",
            "contest_combos",
            "contest_type",
            "contest_effect",
            "damage_class",
            "effect_entries",
            "effect_changes",
            "generation",
            "meta",
            "names",
            "past_values",
            "stat_changes",
            "super_contest_effect",
            "target",
            "type",
            "machines",
            "flavor_text_entries",
            "learned_by_pokemon",
        )

    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name", "url"],
                "properties": {
                    "name": {"type": "string", "examples": ["clefairy"]},
                    "url": {
                        "type": "string",
                        "format": "uri",
                        "examples": ["https://pokeapi.co/api/v2/pokemon/35/"],
                    },
                },
            },
        }
    )
    def get_learned_by_pokemon(self, obj):
        pokemon_moves = PokemonMove.objects.filter(move_id=obj).order_by("pokemon_id")

        pokemon_list = []

        pokemon_ids = pokemon_moves.values("pokemon_id").distinct()

        for id in pokemon_ids:
            pokemon_object = Pokemon.objects.get(pk=id["pokemon_id"])
            pokemon_data = PokemonSummarySerializer(
                pokemon_object, context=self.context
            ).data

            pokemon_list.append(pokemon_data)

        return pokemon_list

    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["machine", "version_group"],
                "properties": {
                    "machine": {
                        "type": "object",
                        "required": ["url"],
                        "properties": {
                            "url": {
                                "type": "string",
                                "format": "uri",
                                "examples": ["https://pokeapi.co/api/v2/machine/1/"],
                            }
                        },
                    },
                    "version_group": {
                        "type": "object",
                        "required": ["name", "url"],
                        "properties": {
                            "name": {"type": "string", "examples": ["sword-shield"]},
                            "url": {
                                "type": "string",
                                "format": "uri",
                                "examples": [
                                    "https://pokeapi.co/api/v2/version-group/1/"
                                ],
                            },
                        },
                    },
                },
            },
        }
    )
    def get_move_machines(self, obj):
        machine_objects = Machine.objects.filter(move=obj)

        machines = []

        for machine_object in machine_objects:
            machine_data = MachineSummarySerializer(
                machine_object, context=self.context
            ).data

            version_group_data = VersionGroupSummarySerializer(
                machine_object.version_group, context=self.context
            ).data

            machines.append(
                {"machine": machine_data, "version_group": version_group_data}
            )

        return machines

    @extend_schema_field(
        field={
            "type": "object",
            "required": ["normal", "super"],
            "properties": {
                "normal": {
                    "type": "object",
                    "required": ["use_before", "use_after"],
                    "properties": {
                        "use_before": {
                            "type": "array",
                            "nullable": True,
                            "items": {
                                "type": "object",
                                "required": ["name", "url"],
                                "properties": {
                                    "name": {
                                        "type": "string",
                                        "examples": ["fire-punch"],
                                    },
                                    "url": {
                                        "type": "string",
                                        "format": "uri",
                                        "examples": [
                                            "https://pokeapi.co/api/v2/move/7/"
                                        ],
                                    },
                                },
                            },
                        },
                        "use_after": {
                            "type": "array",
                            "nullable": True,
                            "items": {
                                "type": "object",
                                "required": ["name", "url"],
                                "properties": {
                                    "name": {
                                        "type": "string",
                                        "examples": ["ice-punch"],
                                    },
                                    "url": {
                                        "type": "string",
                                        "format": "uri",
                                        "examples": [
                                            "https://pokeapi.co/api/v2/move/8/"
                                        ],
                                    },
                                },
                            },
                        },
                    },
                },
                "super": {
                    "type": "object",
                    "required": ["use_before", "use_after"],
                    "properties": {
                        "use_before": {
                            "type": "array",
                            "nullable": True,
                            "items": {
                                "type": "object",
                                "required": ["name", "url"],
                                "properties": {
                                    "name": {
                                        "type": "string",
                                        "examples": ["night-slash"],
                                    },
                                    "url": {
                                        "type": "string",
                                        "format": "uri",
                                        "examples": [
                                            "https://pokeapi.co/api/v2/move/400/"
                                        ],
                                    },
                                },
                            },
                        },
                        "use_after": {
                            "type": "array",
                            "nullable": True,
                            "items": {
                                "type": "object",
                                "required": ["name", "url"],
                                "properties": {
                                    "name": {
                                        "type": "string",
                                        "examples": ["focus-energy"],
                                    },
                                    "url": {
                                        "type": "string",
                                        "format": "uri",
                                        "examples": [
                                            "https://pokeapi.co/api/v2/move/116/"
                                        ],
                                    },
                                },
                            },
                        },
                    },
                },
            },
        }
    )
    def get_combos(self, obj):
        normal_before_objects = ContestCombo.objects.filter(first_move=obj)
        normal_before_data = ContestComboSerializer(
            normal_before_objects, many=True, context=self.context
        ).data
        normal_after_objects = ContestCombo.objects.filter(second_move=obj)
        normal_after_data = ContestComboSerializer(
            normal_after_objects, many=True, context=self.context
        ).data

        super_before_objects = SuperContestCombo.objects.filter(first_move=obj)
        super_before_data = SuperContestComboSerializer(
            super_before_objects, many=True, context=self.context
        ).data
        super_after_objects = SuperContestCombo.objects.filter(second_move=obj)
        super_after_data = SuperContestComboSerializer(
            super_after_objects, many=True, context=self.context
        ).data

        details = None

        if (
            normal_before_data
            or normal_after_data
            or super_before_data
            or super_after_data
        ):
            details = OrderedDict()
            details["normal"] = OrderedDict()
            details["normal"]["use_before"] = None
            details["normal"]["use_after"] = None
            details["super"] = OrderedDict()
            details["super"]["use_before"] = None
            details["super"]["use_after"] = None

            for combo in normal_before_data:
                if details["normal"]["use_before"] is None:
                    details["normal"]["use_before"] = []
                details["normal"]["use_before"].append(combo["second_move"])

            for combo in normal_after_data:
                if details["normal"]["use_after"] is None:
                    details["normal"]["use_after"] = []
                details["normal"]["use_after"].append(combo["first_move"])

            for combo in super_before_data:
                if details["super"]["use_before"] is None:
                    details["super"]["use_before"] = []
                details["super"]["use_before"].append(combo["second_move"])

            for combo in super_after_data:
                if details["super"]["use_after"] is None:
                    details["super"]["use_after"] = []
                details["super"]["use_after"].append(combo["first_move"])

        return details

    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["effect", "short_effect", "language"],
                "properties": {
                    "effect": {
                        "type": "string",
                        "examples": [
                            "Inflicts [regular damage]{mechanic:regular-damage}."
                        ],
                    },
                    "short_effect": {
                        "type": "string",
                        "examples": [
                            "Inflicts regular damage with no additional effect."
                        ],
                    },
                    "language": {
                        "type": "object",
                        "required": ["name", "url"],
                        "properties": {
                            "name": {"type": "string", "examples": ["en"]},
                            "url": {
                                "type": "string",
                                "format": "uri",
                                "examples": ["https://pokeapi.co/api/v2/language/9/"],
                            },
                        },
                    },
                },
            },
        }
    )
    def get_effect_text(self, obj):
        effect_texts = MoveEffectEffectText.objects.filter(move_effect=obj.move_effect)
        data = MoveEffectEffectTextSerializer(
            effect_texts, many=True, context=self.context
        ).data
        if len(data) > 0:
            for key, value in data[0].items():
                if "$effect_chance%" in value:
                    data[0][key] = value.replace(
                        "$effect_chance", f"{obj.move_effect_chance}"
                    )

        return data

    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["effect_entries", "version_group"],
                "properties": {
                    "effect_entries": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["effect", "language"],
                            "properties": {
                                "effect": {
                                    "type": "string",
                                    "examples": [
                                        "Hits Pokémon under the effects of dig and fly."
                                    ],
                                },
                                "language": {
                                    "type": "object",
                                    "required": ["name", "url"],
                                    "properties": {
                                        "name": {"type": "string", "examples": ["en"]},
                                        "url": {
                                            "type": "string",
                                            "format": "uri",
                                            "examples": [
                                                "https://pokeapi.co/api/v2/language/9/"
                                            ],
                                        },
                                    },
                                },
                            },
                        },
                    },
                    "version_group": {
                        "type": "object",
                        "required": ["name", "url"],
                        "properties": {
                            "name": {"type": "string", "examples": ["gold-silver"]},
                            "url": {
                                "type": "string",
                                "format": "uri",
                                "examples": [
                                    "https://pokeapi.co/api/v2/version-group/3/"
                                ],
                            },
                        },
                    },
                },
            },
        }
    )
    def get_effect_change_text(self, obj):
        effect_changes = MoveEffectChange.objects.filter(move_effect=obj.move_effect)
        data = MoveEffectChangeSerializer(
            effect_changes, many=True, context=self.context
        ).data

        return data

    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["change", "stat"],
                "properties": {
                    "change": {"type": "integer", "format": "int32", "examples": [2]},
                    "stat": {
                        "type": "object",
                        "required": ["name", "url"],
                        "properties": {
                            "name": {"type": "string", "examples": ["attack"]},
                            "url": {
                                "type": "string",
                                "format": "uri",
                                "examples": ["https://pokeapi.co/api/v2/stat/1/"],
                            },
                        },
                    },
                },
            },
        }
    )
    def get_move_stat_change(self, obj):
        stat_change_objects = MoveMetaStatChange.objects.filter(move=obj)
        stat_changes = MoveMetaStatChangeSerializer(
            stat_change_objects, many=True, context=self.context
        ).data

        for change in stat_changes:
            del change["move"]

        return stat_changes


##########################
#  PAL PARK SERIALIZERS  #
##########################


class PalParkSerializer(serializers.ModelSerializer):
    area = PalParkAreaSummarySerializer(read_only=True, source="pal_park_area")
    pokemon_species = PokemonSpeciesSummarySerializer()

    class Meta:
        model = PalPark
        fields = ("base_score", "rate", "area", "pokemon_species")


class PalParkAreaNameSerializer(serializers.HyperlinkedModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = PalParkAreaName
        fields = ("name", "language")


class PalParkAreaDetailSerializer(serializers.ModelSerializer):
    names = PalParkAreaNameSerializer(
        many=True, read_only=True, source="palparkareaname"
    )
    pokemon_encounters = serializers.SerializerMethodField("get_encounters")

    class Meta:
        model = PalParkArea
        fields = ("id", "name", "names", "pokemon_encounters")

    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["base_score", "pokemon-species", "rate"],
                "properties": {
                    "base_score": {
                        "type": "integer",
                        "format": "int32",
                        "examples": [50],
                    },
                    "pokemon-species": {
                        "type": "object",
                        "required": ["name", "url"],
                        "properties": {
                            "name": {"type": "string", "examples": ["bulbasaur"]},
                            "url": {
                                "type": "string",
                                "format": "uri",
                                "examples": [
                                    "https://pokeapi.co/api/v2/pokemon-species/1/"
                                ],
                            },
                        },
                    },
                    "rate": {"type": "integer", "format": "int32", "examples": [30]},
                },
            },
        }
    )
    def get_encounters(self, obj):
        pal_park_objects = PalPark.objects.filter(pal_park_area=obj)
        parks = PalParkSerializer(
            pal_park_objects, many=True, context=self.context
        ).data
        encounters = []

        for encounter in parks:
            del encounter["area"]
            encounters.append(encounter)

        return encounters


###############################
#  POKEMON COLOR SERIALIZERS  #
###############################


class PokemonColorNameSerializer(serializers.HyperlinkedModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = PokemonColorName
        fields = ("name", "language")


class PokemonColorDetailSerializer(serializers.ModelSerializer):
    names = PokemonColorNameSerializer(
        many=True, read_only=True, source="pokemoncolorname"
    )
    pokemon_species = PokemonSpeciesSummarySerializer(
        many=True, read_only=True, source="pokemonspecies"
    )

    class Meta:
        model = PokemonColor
        fields = ("id", "name", "names", "pokemon_species")


##############################
#  POKEMON FORM SERIALIZERS  #
##############################
class PokemonFormSpritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PokemonFormSprites
        fields = ("sprites",)


class PokemonFormNameSerializer(serializers.ModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = PokemonFormName
        fields = ("name", "pokemon_name", "language")


class PokemonFormDetailSerializer(serializers.ModelSerializer):
    pokemon = PokemonSummarySerializer()
    version_group = VersionGroupSummarySerializer()
    sprites = serializers.SerializerMethodField("get_pokemon_form_sprites")
    form_names = serializers.SerializerMethodField("get_pokemon_form_names")
    names = serializers.SerializerMethodField("get_pokemon_form_pokemon_names")
    types = serializers.SerializerMethodField("get_pokemon_form_types")

    class Meta:
        model = PokemonForm
        fields = (
            "id",
            "name",
            "order",
            "form_order",
            "is_default",
            "is_battle_only",
            "is_mega",
            "form_name",
            "pokemon",
            "sprites",
            "version_group",
            "form_names",
            "names",
            "types",
        )

    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["language", "name"],
                "properties": {
                    "language": {
                        "type": "object",
                        "required": ["name", "url"],
                        "properties": {
                            "name": {"type": "string", "examples": ["en"]},
                            "url": {
                                "type": "string",
                                "format": "uri",
                                "examples": ["https://pokeapi.co/api/v2/language/9/"],
                            },
                        },
                    },
                    "name": {"type": "string", "examples": ["Plant Cloak"]},
                },
            },
        }
    )
    def get_pokemon_form_names(self, obj):
        form_results = PokemonFormName.objects.filter(
            pokemon_form=obj, name__regex=".+"
        )
        form_serializer = PokemonFormNameSerializer(
            form_results, many=True, context=self.context
        )

        data = form_serializer.data

        for name in data:
            del name["pokemon_name"]

        return data

    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["language", "name"],
                "properties": {
                    "language": {
                        "type": "object",
                        "required": ["name", "url"],
                        "properties": {
                            "name": {"type": "string", "examples": ["en"]},
                            "url": {
                                "type": "string",
                                "format": "uri",
                                "examples": ["https://pokeapi.co/api/v2/language/9/"],
                            },
                        },
                    },
                    "name": {"type": "string", "examples": ["Plant Cloak"]},
                },
            },
        }
    )
    def get_pokemon_form_pokemon_names(self, obj):
        form_results = PokemonFormName.objects.filter(
            pokemon_form=obj, pokemon_name__regex=".+"
        )
        form_serializer = PokemonFormNameSerializer(
            form_results, many=True, context=self.context
        )

        data = form_serializer.data

        for name in data:
            name["name"] = name["pokemon_name"]
            del name["pokemon_name"]

        return data

    @extend_schema_field(
        field={
            "type": "object",
            "properties": {
                "default": {
                    "type": "string",
                    "format": "uri",
                    "examples": [
                        "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/412.png"
                    ],
                }
            },
            "additionalProperties": {  # Stoplight Elements doesn't render this well
                "type": "string",
                "format": "uri",
                "nullable": True,
                "examples": [
                    "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/shiny/412.png"
                ],
            },
            "examples": [
                {
                    "back_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/412.png",
                    "back_female": None,
                    "back_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/shiny/412.png",
                    "back_shiny_female": None,
                    "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/412.png",
                    "front_female": None,
                    "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/412.png",
                    "front_shiny_female": None,
                }
            ],
        }
    )
    def get_pokemon_form_sprites(self, obj):
        sprites_object = PokemonFormSprites.objects.get(pokemon_form_id=obj)
        return sprites_object.sprites

    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["slot", "type"],
                "properties": {
                    "slot": {"type": "integer", "format": "int32", "examples": [1]},
                    "type": {
                        "type": "object",
                        "required": ["name", "url"],
                        "properties": {
                            "name": {"type": "string", "examples": ["bug"]},
                            "url": {
                                "type": "string",
                                "format": "uri",
                                "examples": ["https://pokeapi.co/api/v2/type/7/"],
                            },
                        },
                    },
                },
            },
        }
    )
    def get_pokemon_form_types(self, obj):
        form_type_objects = PokemonFormType.objects.filter(pokemon_form=obj)
        form_types = PokemonFormTypeSerializer(
            form_type_objects, many=True, context=self.context
        ).data

        for form_type in form_types:
            del form_type["pokemon_form"]

        # defer to parent Pokemon's types if no form-specific types
        if form_types == []:
            pokemon_object = Pokemon.objects.get(id=obj.pokemon_id)
            pokemon_type_objects = PokemonType.objects.filter(pokemon=pokemon_object)
            form_types = PokemonTypeSerializer(
                pokemon_type_objects, many=True, context=self.context
            ).data

            for form_type in form_types:
                del form_type["pokemon"]

        return form_types


#################################
#  POKEMON HABITAT SERIALIZERS  #
#################################


class PokemonHabitatNameSerializer(serializers.HyperlinkedModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = PokemonHabitatName
        fields = ("name", "language")


class PokemonHabitatDetailSerializer(serializers.ModelSerializer):
    names = PokemonHabitatNameSerializer(
        many=True, read_only=True, source="pokemonhabitatname"
    )
    pokemon_species = PokemonSpeciesSummarySerializer(
        many=True, read_only=True, source="pokemonspecies"
    )

    class Meta:
        model = PokemonHabitat
        fields = ("id", "name", "names", "pokemon_species")


##############################
#  POKEMON MOVE SERIALIZERS  #
##############################


class MoveLearnMethodNameSerializer(serializers.HyperlinkedModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = MoveLearnMethodName
        fields = ("name", "language")


class MoveLearnMethodDescriptionSerializer(serializers.HyperlinkedModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = MoveLearnMethodDescription
        fields = ("description", "language")


class MoveLearnMethodDetailSerializer(serializers.ModelSerializer):
    names = MoveLearnMethodNameSerializer(
        many=True, read_only=True, source="movelearnmethodname"
    )
    descriptions = MoveLearnMethodDescriptionSerializer(
        many=True, read_only=True, source="movelearnmethoddescription"
    )
    version_groups = serializers.SerializerMethodField("get_method_version_groups")

    class Meta:
        model = MoveLearnMethod
        fields = ("id", "name", "names", "descriptions", "version_groups")

        # "version_groups": [
        #   {
        #     "name": "red-blue",
        #     "url": "https://pokeapi.co/api/v2/version-group/1/"
        #   },

    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name", "url"],
                "properties": {
                    "name": {"type": "string", "examples": ["red-blue"]},
                    "url": {
                        "type": "string",
                        "format": "uri",
                        "examples": ["https://pokeapi.co/api/v2/version-group/1/"],
                    },
                },
            },
        }
    )
    def get_method_version_groups(self, obj):
        version_group_objects = VersionGroupMoveLearnMethod.objects.filter(
            move_learn_method=obj
        )
        version_group_data = VersionGroupMoveLearnMethodSerializer(
            version_group_objects, many=True, context=self.context
        ).data
        groups = []

        for vg in version_group_data:
            groups.append(vg["version_group"])

        return groups


# https://stackoverflow.com/a/45987450/3482533
class PokemonMoveSerializer(serializers.ModelSerializer):
    class Meta:
        model = PokemonMove
        fields = "__all__"


###############################
#  POKEMON SHAPE SERIALIZERS  #
###############################
class PokemonShapeNameSerializer(serializers.HyperlinkedModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = PokemonShapeName
        fields = ("name", "awesome_name", "language")


class PokemonShapeDetailSerializer(serializers.ModelSerializer):
    names = serializers.SerializerMethodField("get_shape_names")
    awesome_names = serializers.SerializerMethodField("get_shape_awesome_names")
    pokemon_species = PokemonSpeciesSummarySerializer(
        many=True, read_only=True, source="pokemonspecies"
    )

    class Meta:
        model = PokemonShape
        fields = ("id", "name", "awesome_names", "names", "pokemon_species")

    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["url", "name"],
                "properties": {
                    "url": {
                        "type": "string",
                        "format": "uri",
                        "examples": ["https://pokeapi.co/api/v2/language/9/"],
                    },
                    "name": {"type": "string", "examples": ["Ball"]},
                },
            },
        }
    )
    def get_shape_names(self, obj):
        results = PokemonShapeName.objects.filter(pokemon_shape_id=obj)
        serializer = PokemonShapeNameSerializer(
            results, many=True, context=self.context
        )
        data = serializer.data

        for entry in data:
            del entry["awesome_name"]

        return data

    # "awesome_names": [
    #   {
    #     "awesome_name": "Pomacé",
    #     "language": {
    #       "name": "fr",
    #       "url": "https://pokeapi.co/api/v2/language/5/"
    #     }
    #   },
    #   {
    #     "awesome_name": "Pomaceous",
    #     "language": {
    #       "name": "en",
    #       "url": "https://pokeapi.co/api/v2/language/9/"
    #     }
    #   }
    # ],
    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["awesome_name", "language"],
                "properties": {
                    "awesome_name": {"type": "string", "examples": ["Pomaceous"]},
                    "language": {
                        "type": "object",
                        "required": ["name", "url"],
                        "properties": {
                            "name": {"type": "string", "examples": ["en"]},
                            "url": {
                                "type": "string",
                                "format": "uri",
                                "examples": ["https://pokeapi.co/api/v2/language/9/"],
                            },
                        },
                    },
                },
            },
        }
    )
    def get_shape_awesome_names(self, obj):
        results = PokemonShapeName.objects.filter(pokemon_shape_id=obj)
        serializer = PokemonShapeNameSerializer(
            results, many=True, context=self.context
        )
        data = serializer.data

        for entry in data:
            del entry["name"]

        return data


##############################
#  POKEMON ITEM SERIALIZERS  #
##############################
class PokemonItemSerializer(serializers.ModelSerializer):
    version = VersionSummarySerializer()
    item = ItemSummarySerializer()

    class Meta:
        model = PokemonItem
        fields = ("rarity", "item", "version")


##############################
#  POKEMON STAT SERIALIZERS  #
##############################
class PokemonStatSerializer(serializers.ModelSerializer):
    stat = StatSummarySerializer()

    class Meta:
        model = PokemonStat
        fields = ("base_stat", "effort", "stat")


#########################
#  POKEMON SERIALIZERS  #
#########################


class PokemonGameIndexSerializer(serializers.ModelSerializer):
    version = VersionSummarySerializer()

    class Meta:
        model = PokemonGameIndex
        fields = ("game_index", "version")


class PokemonDetailSerializer(serializers.ModelSerializer):
    abilities = serializers.SerializerMethodField("get_pokemon_abilities")
    past_abilities = serializers.SerializerMethodField("get_past_pokemon_abilities")
    game_indices = PokemonGameIndexSerializer(
        many=True, read_only=True, source="pokemongameindex"
    )
    moves = serializers.SerializerMethodField("get_pokemon_moves")
    species = PokemonSpeciesSummarySerializer(source="pokemon_species")
    stats = PokemonStatSerializer(many=True, read_only=True, source="pokemonstat")
    types = serializers.SerializerMethodField("get_pokemon_types")
    past_types = serializers.SerializerMethodField("get_past_pokemon_types")
    forms = PokemonFormSummarySerializer(
        many=True, read_only=True, source="pokemonform"
    )
    held_items = serializers.SerializerMethodField("get_pokemon_held_items")
    location_area_encounters = serializers.SerializerMethodField("get_encounters")
    sprites = serializers.SerializerMethodField("get_pokemon_sprites")
    cries = serializers.SerializerMethodField("get_pokemon_cries")

    class Meta:
        model = Pokemon
        fields = (
            "id",
            "name",
            "base_experience",
            "height",
            "is_default",
            "order",
            "weight",
            "abilities",
            "past_abilities",
            "forms",
            "game_indices",
            "held_items",
            "location_area_encounters",
            "moves",
            "species",
            "sprites",
            "cries",
            "stats",
            "types",
            "past_types",
        )

    @extend_schema_field(
        field={
            "type": "object",
            "properties": {
                "front_default": {
                    "type": "string",
                    "format": "uri",
                    "exmaple": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/1.png",
                }
            },
            "additionalProperties": {  # Stoplight Elements doesn't render this well
                "type": "string",
                "format": "uri",
                "nullable": True,
                "examples": [
                    "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/shiny/1.png"
                ],
            },
            "examples": [
                {
                    "back_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/1.png",
                    "back_female": None,
                    "back_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/shiny/1.png",
                    "back_shiny_female": None,
                    "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png",
                    "front_female": None,
                    "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/1.png",
                    "front_shiny_female": None,
                }
            ],
        }
    )
    def get_pokemon_sprites(self, obj):
        sprites_object = PokemonSprites.objects.get(pokemon_id=obj)
        return sprites_object.sprites

    @extend_schema_field(
        field={
            "type": "object",
            "required": ["latest", "legacy"],
            "properties": {
                "latest": {
                    "type": "string",
                    "format": "uri",
                    "examples": [
                        "https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/latest/50.ogg"
                    ],
                },
                "legacy": {
                    "type": "string",
                    "format": "uri",
                    "examples": [
                        "https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/legacy/50.ogg"
                    ],
                },
            },
        }
    )
    def get_pokemon_cries(self, obj):
        cries_object = PokemonCries.objects.get(pokemon_id=obj)
        return cries_object.cries

    # {
    #   "move": {
    #     "name": "scratch",
    #     "url": "https://pokeapi.co/api/v2/move/10/"
    #   },
    #   "version_group_details": [
    #     {
    #       "level_learned_at": 1,
    #       "move_learn_method": {
    #         "name": "level-up",
    #         "url": "https://pokeapi.co/api/v2/move-learn-method/1/"
    #       },
    #       "version_group": {
    #         "name": "red-blue",
    #         "url": "https://pokeapi.co/api/v2/version-group/1/"
    #       }
    #     },
    #     {
    #       "level_learned_at": 1,
    #       "move_learn_method": {
    #         "name": "level-up",
    #         "url": "https://pokeapi.co/api/v2/move-learn-method/1/"
    #       },
    #       "version_group": {
    #         "name": "yellow",
    #         "url": "https://pokeapi.co/api/v2/version-group/2/"
    #       }
    #     },
    #     {
    #       "level_learned_at": 1,
    #       "move_learn_method": {
    #         "name": "level-up",
    #         "url": "https://pokeapi.co/api/v2/move-learn-method/1/"
    #       },
    #       "version_group": {
    #         "name": "gold-silver",
    #         "url": "https://pokeapi.co/api/v2/version-group/3/"
    #       }
    #     },
    #     {
    #       "level_learned_at": 1,
    #       "move_learn_method": {
    #         "name": "level-up",
    #         "url": "https://pokeapi.co/api/v2/move-learn-method/1/"
    #       },
    #       "version_group": {
    #         "name": "crystal",
    #         "url": "https://pokeapi.co/api/v2/version-group/4/"
    #       }
    #     },
    #     {
    #       "level_learned_at": 1,
    #       "move_learn_method": {
    #         "name": "level-up",
    #         "url": "https://pokeapi.co/api/v2/move-learn-method/1/"
    #       },
    #       "version_group": {
    #         "name": "ruby-sapphire",
    #         "url": "https://pokeapi.co/api/v2/version-group/5/"
    #       }
    #     },
    #     {
    #       "level_learned_at": 1,
    #       "move_learn_method": {
    #         "name": "level-up",
    #         "url": "https://pokeapi.co/api/v2/move-learn-method/1/"
    #       },
    #       "version_group": {
    #         "name": "emerald",
    #         "url": "https://pokeapi.co/api/v2/version-group/6/"
    #       }
    #     },
    #     {
    #       "level_learned_at": 1,
    #       "move_learn_method": {
    #         "name": "level-up",
    #         "url": "https://pokeapi.co/api/v2/move-learn-method/1/"
    #       },
    #       "version_group": {
    #         "name": "firered-leafgreen",
    #         "url": "https://pokeapi.co/api/v2/version-group/7/"
    #       }
    #     },
    #     {
    #       "level_learned_at": 1,
    #       "move_learn_method": {
    #         "name": "level-up",
    #         "url": "https://pokeapi.co/api/v2/move-learn-method/1/"
    #       },
    #       "version_group": {
    #         "name": "diamond-pearl",
    #         "url": "https://pokeapi.co/api/v2/version-group/8/"
    #       }
    #     },
    #     {
    #       "level_learned_at": 1,
    #       "move_learn_method": {
    #         "name": "level-up",
    #         "url": "https://pokeapi.co/api/v2/move-learn-method/1/"
    #       },
    #       "version_group": {
    #         "name": "platinum",
    #         "url": "https://pokeapi.co/api/v2/version-group/9/"
    #       }
    #     },
    #     {
    #       "level_learned_at": 1,
    #       "move_learn_method": {
    #         "name": "level-up",
    #         "url": "https://pokeapi.co/api/v2/move-learn-method/1/"
    #       },
    #       "version_group": {
    #         "name": "heartgold-soulsilver",
    #         "url": "https://pokeapi.co/api/v2/version-group/10/"
    #       }
    #     },
    #     {
    #       "level_learned_at": 1,
    #       "move_learn_method": {
    #         "name": "level-up",
    #         "url": "https://pokeapi.co/api/v2/move-learn-method/1/"
    #       },
    #       "version_group": {
    #         "name": "black-white",
    #         "url": "https://pokeapi.co/api/v2/version-group/11/"
    #       }
    #     },
    #     {
    #       "level_learned_at": 1,
    #       "move_learn_method": {
    #         "name": "level-up",
    #         "url": "https://pokeapi.co/api/v2/move-learn-method/1/"
    #       },
    #       "version_group": {
    #         "name": "colosseum",
    #         "url": "https://pokeapi.co/api/v2/version-group/12/"
    #       }
    #     },
    #     {
    #       "level_learned_at": 1,
    #       "move_learn_method": {
    #         "name": "level-up",
    #         "url": "https://pokeapi.co/api/v2/move-learn-method/1/"
    #       },
    #       "version_group": {
    #         "name": "xd",
    #         "url": "https://pokeapi.co/api/v2/version-group/13/"
    #       }
    #     },
    #     {
    #       "level_learned_at": 1,
    #       "move_learn_method": {
    #         "name": "level-up",
    #         "url": "https://pokeapi.co/api/v2/move-learn-method/1/"
    #       },
    #       "version_group": {
    #         "name": "black-2-white-2",
    #         "url": "https://pokeapi.co/api/v2/version-group/14/"
    #       }
    #     },
    #     {
    #       "level_learned_at": 1,
    #       "move_learn_method": {
    #         "name": "level-up",
    #         "url": "https://pokeapi.co/api/v2/move-learn-method/1/"
    #       },
    #       "version_group": {
    #         "name": "x-y",
    #         "url": "https://pokeapi.co/api/v2/version-group/15/"
    #       }
    #     },
    #     {
    #       "level_learned_at": 1,
    #       "move_learn_method": {
    #         "name": "level-up",
    #         "url": "https://pokeapi.co/api/v2/move-learn-method/1/"
    #       },
    #       "version_group": {
    #         "name": "omega-ruby-alpha-sapphire",
    #         "url": "https://pokeapi.co/api/v2/version-group/16/"
    #       }
    #     },
    #     {
    #       "level_learned_at": 1,
    #       "move_learn_method": {
    #         "name": "level-up",
    #         "url": "https://pokeapi.co/api/v2/move-learn-method/1/"
    #       },
    #       "version_group": {
    #         "name": "sun-moon",
    #         "url": "https://pokeapi.co/api/v2/version-group/17/"
    #       }
    #     },
    #     {
    #       "level_learned_at": 1,
    #       "move_learn_method": {
    #         "name": "level-up",
    #         "url": "https://pokeapi.co/api/v2/move-learn-method/1/"
    #       },
    #       "version_group": {
    #         "name": "ultra-sun-ultra-moon",
    #         "url": "https://pokeapi.co/api/v2/version-group/18/"
    #       }
    #     },
    #     {
    #       "level_learned_at": 1,
    #       "move_learn_method": {
    #         "name": "level-up",
    #         "url": "https://pokeapi.co/api/v2/move-learn-method/1/"
    #       },
    #       "version_group": {
    #         "name": "lets-go-pikachu-lets-go-eevee",
    #         "url": "https://pokeapi.co/api/v2/version-group/19/"
    #       }
    #     },
    #     {
    #       "level_learned_at": 1,
    #       "move_learn_method": {
    #         "name": "level-up",
    #         "url": "https://pokeapi.co/api/v2/move-learn-method/1/"
    #       },
    #       "version_group": {
    #         "name": "sword-shield",
    #         "url": "https://pokeapi.co/api/v2/version-group/20/"
    #       }
    #     },
    #     {
    #       "level_learned_at": 1,
    #       "move_learn_method": {
    #         "name": "level-up",
    #         "url": "https://pokeapi.co/api/v2/move-learn-method/1/"
    #       },
    #       "version_group": {
    #         "name": "brilliant-diamond-shining-pearl",
    #         "url": "https://pokeapi.co/api/v2/version-group/23/"
    #       }
    #     },
    #     {
    #       "level_learned_at": 1,
    #       "move_learn_method": {
    #         "name": "level-up",
    #         "url": "https://pokeapi.co/api/v2/move-learn-method/1/"
    #       },
    #       "version_group": {
    #         "name": "scarlet-violet",
    #         "url": "https://pokeapi.co/api/v2/version-group/25/"
    #       }
    #     }
    #   ]
    # },

    #   "move": {
    #     "name": "scratch",
    #     "url": "https://pokeapi.co/api/v2/move/10/"
    #   },
    #   "version_group_details": [
    #     {
    #       "level_learned_at": 1,
    #       "move_learn_method": {
    #         "name": "level-up",
    #         "url": "https://pokeapi.co/api/v2/move-learn-method/1/"
    #       },
    #       "version_group": {
    #         "name": "red-blue",
    #         "url": "https://pokeapi.co/api/v2/version-group/1/"
    #       }
    #     },
    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["move", "version_group_details"],
                "properties": {
                    "move": {
                        "type": "object",
                        "required": ["name", "url"],
                        "properties": {
                            "name": {"type": "string", "examples": ["scratch"]},
                            "url": {
                                "type": "string",
                                "format": "uri",
                                "examples": ["https://pokeapi.co/api/v2/move/10/"],
                            },
                        },
                    },
                    "version_group_details": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": [
                                "level_learned_at",
                                "move_learn_method",
                                "version_group",
                            ],
                            "properties": {
                                "level_learned_at": {
                                    "type": "integer",
                                    "format": "int32",
                                    "examples": [1],
                                },
                                "move_learn_method": {
                                    "type": "object",
                                    "required": ["name", "url"],
                                    "properties": {
                                        "name": {
                                            "type": "string",
                                            "examples": ["level-up"],
                                        },
                                        "url": {
                                            "type": "string",
                                            "format": "uri",
                                            "examples": [
                                                "https://pokeapi.co/api/v2/move-learn-method/1/"
                                            ],
                                        },
                                    },
                                },
                                "version_group": {
                                    "type": "object",
                                    "required": ["name", "url"],
                                    "properties": {
                                        "name": {
                                            "type": "string",
                                            "examples": ["red-blue"],
                                        },
                                        "url": {
                                            "type": "string",
                                            "format": "uri",
                                            "examples": [
                                                "https://pokeapi.co/api/v2/version-group/1/"
                                            ],
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        }
    )
    def get_pokemon_moves(self, obj):
        version_objects = VersionGroup.objects.all()
        version_data = VersionGroupSummarySerializer(
            version_objects, many=True, context=self.context
        ).data
        method_objects = MoveLearnMethod.objects.all()
        method_data = MoveLearnMethodSummarySerializer(
            method_objects, many=True, context=self.context
        ).data

        # Get moves related to this pokemon and pull out unique Move IDs.
        # Note that it's important to order by the same column we're using to
        # determine if the entries are unique.  Otherwise distinct() will
        # return apparent duplicates.

        pokemon_moves = PokemonMove.objects.filter(pokemon_id=obj).order_by("move_id")
        move_ids = pokemon_moves.values("move_id").distinct()
        move_list = []

        for id in move_ids:
            pokemon_move_details = OrderedDict()

            # Get each Unique Move by ID
            move_object = Move.objects.get(pk=id["move_id"])
            move_data = MoveSummarySerializer(move_object, context=self.context).data
            pokemon_move_details["move"] = move_data

            # Get Versions and Move Methods associated with each unique move
            pokemon_move_objects = pokemon_moves.filter(move_id=id["move_id"])
            serializer = PokemonMoveSerializer(
                pokemon_move_objects, many=True, context=self.context
            )
            pokemon_move_details["version_group_details"] = []

            for move in serializer.data:
                version_detail = OrderedDict()

                version_detail["level_learned_at"] = move["level"]
                version_detail["version_group"] = version_data[
                    move["version_group"] - 1
                ]
                version_detail["move_learn_method"] = method_data[
                    move["move_learn_method"] - 1
                ]
                version_detail["order"] = move["order"]

                pokemon_move_details["version_group_details"].append(version_detail)

            move_list.append(pokemon_move_details)

        return move_list

    # {
    #   "item": {
    #     "name": "soft-sand",
    #     "url": "https://pokeapi.co/api/v2/item/214/"
    #   },
    #   "version_details": [
    #     {
    #       "rarity": 5,
    #       "version": {
    #         "name": "diamond",
    #         "url": "https://pokeapi.co/api/v2/version/12/"
    #       }
    #     },
    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["item", "version_details"],
                "properties": {
                    "item": {
                        "type": "object",
                        "required": ["name", "url"],
                        "properties": {
                            "name": {"type": "string", "examples": ["soft-sand"]},
                            "url": {
                                "type": "string",
                                "format": "uri",
                                "examples": ["https://pokeapi.co/api/v2/item/214/"],
                            },
                        },
                    },
                    "version_details": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["rarity", "version"],
                            "properties": {
                                "rarity": {
                                    "type": "integer",
                                    "format": "int32",
                                    "examples": [5],
                                },
                                "version": {
                                    "type": "object",
                                    "required": ["name", "url"],
                                    "properties": {
                                        "name": {
                                            "type": "string",
                                            "examples": ["diamond"],
                                        },
                                        "url": {
                                            "type": "string",
                                            "format": "uri",
                                            "examples": [
                                                "https://pokeapi.co/api/v2/version/12/"
                                            ],
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        }
    )
    def get_pokemon_held_items(self, obj):
        # Get items related to this pokemon and pull out unique Item IDs
        pokemon_items = PokemonItem.objects.filter(pokemon_id=obj).order_by("item_id")
        item_ids = pokemon_items.values("item_id").distinct()
        item_list = []

        for id in item_ids:
            pokemon_item_details = OrderedDict()

            # Get each Unique Item by ID
            item_object = Item.objects.get(pk=id["item_id"])
            item_data = ItemSummarySerializer(item_object, context=self.context).data
            pokemon_item_details["item"] = item_data

            # Get Versions associated with each unique item
            pokemon_item_objects = pokemon_items.filter(item_id=id["item_id"])
            serializer = PokemonItemSerializer(
                pokemon_item_objects, many=True, context=self.context
            )
            pokemon_item_details["version_details"] = []

            for item in serializer.data:
                version_detail = OrderedDict()

                version_detail["rarity"] = item["rarity"]
                version_detail["version"] = item["version"]

                pokemon_item_details["version_details"].append(version_detail)

            item_list.append(pokemon_item_details)

        return item_list

    # {
    #   "ability": {
    #     "name": "sand-veil",
    #     "url": "https://pokeapi.co/api/v2/ability/8/"
    #   },
    #   "is_hidden": false,
    #   "slot": 1
    # },
    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["ability", "is_hidden", "slot"],
                "properties": {
                    "ability": {
                        "type": "object",
                        "required": ["name", "url"],
                        "properties": {
                            "name": {"type": "string", "examples": ["sand-veil"]},
                            "url": {
                                "type": "string",
                                "format": "uri",
                                "examples": ["https://pokeapi.co/api/v2/ability/8/"],
                            },
                        },
                    },
                    "is_hidden": {"type": "boolean"},
                    "slot": {"type": "integer", "format": "int32", "examples": [1]},
                },
            },
        }
    )
    def get_pokemon_abilities(self, obj):
        pokemon_ability_objects = PokemonAbility.objects.filter(pokemon=obj)
        data = PokemonAbilitySerializer(
            pokemon_ability_objects, many=True, context=self.context
        ).data
        abilities = []

        for ability in data:
            del ability["pokemon"]
            abilities.append(ability)

        return abilities

    # {
    #   "abilities": [
    #     {
    #       "ability": {
    #         "name": "levitate",
    #         "url": "https://pokeapi.co/api/v2/ability/26/"
    #       },
    #       "is_hidden": false,
    #       "slot": 1
    #     }
    #   ],
    #   "generation": {
    #     "name": "generation-vi",
    #     "url": "https://pokeapi.co/api/v2/generation/6/"
    #   }
    # }
    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["abilities", "generation"],
                "properties": {
                    "abilities": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["ability", "is_hidden", "slot"],
                            "properties": {
                                "ability": {
                                    "type": "object",
                                    "required": ["name", "url"],
                                    "properties": {
                                        "name": {
                                            "type": "string",
                                            "examples": ["levitate"],
                                        },
                                        "url": {
                                            "type": "string",
                                            "format": "uri",
                                            "examples": [
                                                "https://pokeapi.co/api/v2/ability/26/"
                                            ],
                                        },
                                    },
                                },
                                "is_hidden": {"type": "boolean"},
                                "slot": {
                                    "type": "integer",
                                    "format": "int32",
                                    "examples": [1],
                                },
                            },
                        },
                    },
                    "generation": {
                        "type": "object",
                        "required": ["name", "url"],
                        "properties": {
                            "name": {"type": "string", "examples": ["generation-vi"]},
                            "url": {
                                "type": "string",
                                "format": "uri",
                                "examples": ["https://pokeapi.co/api/v2/generation/6/"],
                            },
                        },
                    },
                },
            },
        }
    )
    def get_past_pokemon_abilities(self, obj):
        pokemon_past_ability_objects = PokemonAbilityPast.objects.filter(pokemon=obj)
        pokemon_past_abilities = PokemonAbilityPastSerializer(
            pokemon_past_ability_objects, many=True, context=self.context
        ).data

        # post-process to the form we want
        current_generation = ""
        past_obj = {}
        final_data = []
        for pokemon_past_ability in pokemon_past_abilities:
            del pokemon_past_ability["pokemon"]

            generation = pokemon_past_ability["generation"]["name"]
            if generation != current_generation:
                current_generation = generation
                past_obj = {}

                # create past abilities object for this generation
                past_obj["generation"] = pokemon_past_ability["generation"]
                del pokemon_past_ability["generation"]

                # create abilities array
                past_obj["abilities"] = [pokemon_past_ability]

                # add to past abilities array
                final_data.append(past_obj)

            else:
                # add to existing array for this generation
                del pokemon_past_ability["generation"]
                past_obj["abilities"].append(pokemon_past_ability)

        return final_data

    # {
    #   "slot": 1,
    #   "type": {
    #     "name": "ghost",
    #     "url": "https://pokeapi.co/api/v2/type/8/"
    #   }
    # },
    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["slot", "type"],
                "properties": {
                    "slot": {"type": "integer", "format": "int32", "examples": [1]},
                    "type": {
                        "type": "object",
                        "required": ["name", "url"],
                        "properties": {
                            "name": {"type": "string", "examples": ["ghost"]},
                            "url": {
                                "type": "string",
                                "format": "uri",
                                "examples": ["https://pokeapi.co/api/v2/type/8/"],
                            },
                        },
                    },
                },
            },
        }
    )
    def get_pokemon_types(self, obj):
        poke_type_objects = PokemonType.objects.filter(pokemon=obj)
        poke_types = PokemonTypeSerializer(
            poke_type_objects, many=True, context=self.context
        ).data

        for poke_type in poke_types:
            del poke_type["pokemon"]

        return poke_types

    # "past_types": [
    #   {
    #     "generation": {
    #       "name": "generation-v",
    #       "url": "https://pokeapi.co/api/v2/generation/5/"
    #     },
    #     "types": [
    #       {
    #         "slot": 1,
    #         "type": {
    #           "name": "normal",
    #           "url": "https://pokeapi.co/api/v2/type/1/"
    #         }
    #       }
    #     ]
    #   }
    # ],
    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["generation", "types"],
                "properties": {
                    "generation": {
                        "type": "object",
                        "required": ["name", "url"],
                        "properties": {
                            "name": {"type": "string", "examples": ["generation-v"]},
                            "url": {
                                "type": "string",
                                "format": "uri",
                                "examples": ["https://pokeapi.co/api/v2/generation/5/"],
                            },
                        },
                    },
                    "types": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["slot", "type"],
                            "properties": {
                                "slot": {
                                    "type": "integer",
                                    "format": "int32",
                                    "examples": [1],
                                },
                                "type": {
                                    "type": "object",
                                    "required": ["name", "url"],
                                    "properties": {
                                        "name": {
                                            "type": "string",
                                            "examples": ["normal"],
                                        },
                                        "url": {
                                            "type": "string",
                                            "format": "uri",
                                            "examples": [
                                                "https://pokeapi.co/api/v2/type/1/"
                                            ],
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        }
    )
    def get_past_pokemon_types(self, obj):
        poke_past_type_objects = PokemonTypePast.objects.filter(pokemon=obj)
        poke_past_types = PokemonTypePastSerializer(
            poke_past_type_objects, many=True, context=self.context
        ).data

        # post-process to the form we want
        current_generation = ""
        past_obj = {}
        final_data = []
        for poke_past_type in poke_past_types:
            del poke_past_type["pokemon"]

            generation = poke_past_type["generation"]["name"]
            if generation != current_generation:
                current_generation = generation
                past_obj = {}

                # create past types object for this generation
                past_obj["generation"] = poke_past_type["generation"]
                del poke_past_type["generation"]

                # create types array
                past_obj["types"] = [poke_past_type]

                # add to past types array
                final_data.append(past_obj)

            else:
                # add to existing array for this generation
                del poke_past_type["generation"]
                past_obj["types"].append(poke_past_type)

        return final_data

    @extend_schema_field(
        field={
            "type": "string",
            "examples": ["https://pokeapi.co/api/v2/pokemon/1/encounters"],
        }
    )
    def get_encounters(self, obj):
        return reverse("pokemon_encounters", kwargs={"pokemon_id": obj.pk})


#################################
#  POKEMON SPECIES SERIALIZERS  #
#################################
class EvolutionTriggerNameSerializer(serializers.HyperlinkedModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = EvolutionTriggerName
        fields = ("name", "language")


class EvolutionTriggerDetailSerializer(serializers.HyperlinkedModelSerializer):
    names = EvolutionTriggerNameSerializer(
        many=True, read_only=True, source="evolutiontriggername"
    )
    pokemon_species = serializers.SerializerMethodField("get_species")

    class Meta:
        model = EvolutionTrigger
        fields = ("id", "name", "names", "pokemon_species")

    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name", "url"],
                "properties": {
                    "name": {"type": "string", "examples": ["ivysaur"]},
                    "url": {
                        "type": "string",
                        "format": "uri",
                        "examples": ["https://pokeapi.co/api/v2/pokemon-species/2/"],
                    },
                },
            },
        }
    )
    def get_species(self, obj):
        evo_objects = PokemonEvolution.objects.filter(evolution_trigger=obj)
        species_list = []
        species_names = set()

        for evo in evo_objects:
            species = PokemonSpeciesSummarySerializer(
                evo.evolved_species, context=self.context
            ).data
            if species["name"] not in species_names:
                species_list.append(species)
                species_names.add(species["name"])

        return species_list


class PokemonSpeciesDescriptionSerializer(serializers.ModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = PokemonSpeciesDescription
        fields = ("description", "language")


class PokemonSpeciesFlavorTextSerializer(serializers.ModelSerializer):
    flavor_text = serializers.CharField()
    language = LanguageSummarySerializer()
    version = VersionSummarySerializer()

    class Meta:
        model = PokemonSpeciesFlavorText
        fields = ("flavor_text", "language", "version")


class PokemonSpeciesNameSerializer(serializers.ModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = PokemonSpeciesName
        fields = ("name", "genus", "language")


class PokemonSpeciesEvolutionSerializer(serializers.ModelSerializer):
    """
    This is here purely to help build pokemon evolution chains
    """

    class Meta:
        model = PokemonSpecies
        fields = ("name", "id", "evolves_from_species", "is_baby")


class PokemonSpeciesDetailSerializer(serializers.ModelSerializer):
    names = serializers.SerializerMethodField("get_pokemon_names")
    form_descriptions = PokemonSpeciesDescriptionSerializer(
        many=True, read_only=True, source="pokemonspeciesdescription"
    )
    pokedex_numbers = PokemonDexEntrySerializer(
        many=True, read_only=True, source="pokemondexnumber"
    )
    egg_groups = serializers.SerializerMethodField("get_pokemon_egg_groups")
    flavor_text_entries = PokemonSpeciesFlavorTextSerializer(
        many=True, read_only=True, source="pokemonspeciesflavortext"
    )
    genera = serializers.SerializerMethodField("get_pokemon_genera")
    generation = GenerationSummarySerializer()
    growth_rate = GrowthRateSummarySerializer()
    color = PokemonColorSummarySerializer(source="pokemon_color")
    habitat = PokemonHabitatSummarySerializer(source="pokemon_habitat")
    shape = PokemonShapeSummarySerializer(source="pokemon_shape")
    evolves_from_species = PokemonSpeciesSummarySerializer()
    varieties = serializers.SerializerMethodField("get_pokemon_varieties")
    evolution_chain = EvolutionChainSummarySerializer()
    pal_park_encounters = serializers.SerializerMethodField("get_encounters")

    class Meta:
        model = PokemonSpecies
        fields = (
            "id",
            "name",
            "order",
            "gender_rate",
            "capture_rate",
            "base_happiness",
            "is_baby",
            "is_legendary",
            "is_mythical",
            "hatch_counter",
            "has_gender_differences",
            "forms_switchable",
            "growth_rate",
            "pokedex_numbers",
            "egg_groups",
            "color",
            "shape",
            "evolves_from_species",
            "evolution_chain",
            "habitat",
            "generation",
            "names",
            "pal_park_encounters",
            "form_descriptions",
            "flavor_text_entries",
            "genera",
            "varieties",
        )

    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["language", "name"],
                "properties": {
                    "language": {
                        "type": "object",
                        "required": ["name", "url"],
                        "properties": {
                            "name": {"type": "string", "examples": ["en"]},
                            "url": {
                                "type": "string",
                                "format": "uri",
                                "examples": ["https://pokeapi.co/api/v2/language/9/"],
                            },
                        },
                    },
                    "name": {"type": "string", "examples": ["bulbasaur"]},
                },
            },
        }
    )
    def get_pokemon_names(self, obj):
        species_results = PokemonSpeciesName.objects.filter(pokemon_species=obj)
        species_serializer = PokemonSpeciesNameSerializer(
            species_results, many=True, context=self.context
        )

        data = species_serializer.data

        for name in data:
            del name["genus"]

        return data

    # {
    #   "genus": "Seed Pokémon",
    #   "language": {
    #     "name": "en",
    #     "url": "https://pokeapi.co/api/v2/language/9/"
    #   }
    # },
    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["genus", "language"],
                "properties": {
                    "genus": {"type": "string", "examples": ["Seed Pokémon"]},
                    "language": {
                        "type": "object",
                        "required": ["name", "url"],
                        "properties": {
                            "name": {"type": "string", "examples": ["en"]},
                            "url": {
                                "type": "string",
                                "format": "uri",
                                "examples": ["https://pokeapi.co/api/v2/language/9/"],
                            },
                        },
                    },
                },
            },
        }
    )
    def get_pokemon_genera(self, obj):
        results = PokemonSpeciesName.objects.filter(pokemon_species=obj)
        serializer = PokemonSpeciesNameSerializer(
            results, many=True, context=self.context
        )
        data = serializer.data
        genera = []

        for entry in data:
            if entry["genus"]:
                del entry["name"]
                genera.append(entry)

        return genera

    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name", "url"],
                "properties": {
                    "name": {"type": "string", "examples": ["monster"]},
                    "url": {
                        "type": "string",
                        "format": "uri",
                        "examples": ["https://pokeapi.co/api/v2/egg-group/1/"],
                    },
                },
            },
        }
    )
    def get_pokemon_egg_groups(self, obj):
        results = PokemonEggGroup.objects.filter(pokemon_species=obj)
        data = PokemonEggGroupSerializer(results, many=True, context=self.context).data
        groups = []
        for group in data:
            groups.append(group["egg_group"])

        return groups

    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["is_default", "pokemon"],
                "properties": {
                    "is_default": {"type": "boolean"},
                    "pokemon": {
                        "type": "object",
                        "required": ["name", "url"],
                        "properties": {
                            "name": {"type": "string", "examples": ["bulbasaur"]},
                            "url": {
                                "type": "string",
                                "format": "uri",
                                "examples": ["https://pokeapi.co/api/v2/pokemon/1/"],
                            },
                        },
                    },
                },
            },
        }
    )
    def get_pokemon_varieties(self, obj):
        results = Pokemon.objects.filter(pokemon_species=obj)
        summary_data = PokemonSummarySerializer(
            results, many=True, context=self.context
        ).data
        detail_data = PokemonDetailSerializer(
            results, many=True, context=self.context
        ).data

        varieties = []

        for index, pokemon in enumerate(detail_data):
            entry = OrderedDict()
            entry["is_default"] = pokemon["is_default"]
            entry["pokemon"] = summary_data[index]
            varieties.append(entry)

        return varieties

    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["area", "base_score", "rate"],
                "properties": {
                    "area": {
                        "type": "object",
                        "required": ["name", "url"],
                        "properties": {
                            "name": {"type": "string", "examples": ["field"]},
                            "url": {
                                "type": "string",
                                "format": "uri",
                                "examples": [
                                    "https://pokeapi.co/api/v2/pal-park-area/2/"
                                ],
                            },
                        },
                    },
                    "base_score": {
                        "type": "integer",
                        "format": "int32",
                        "examples": [50],
                    },
                    "rate": {"type": "integer", "format": "int32", "examples": [30]},
                },
            },
        }
    )
    def get_encounters(self, obj):
        pal_park_objects = PalPark.objects.filter(pokemon_species=obj)
        parks = PalParkSerializer(
            pal_park_objects, many=True, context=self.context
        ).data
        encounters = []

        for encounter in parks:
            del encounter["pokemon_species"]
            encounters.append(encounter)

        return encounters


class PokemonEvolutionSerializer(serializers.ModelSerializer):
    item = ItemSummarySerializer(source="evolution_item")
    held_item = ItemSummarySerializer()
    known_move = MoveSummarySerializer()
    known_move_type = TypeSummarySerializer()
    party_species = PokemonSpeciesSummarySerializer()
    party_type = TypeSummarySerializer()
    trade_species = PokemonSpeciesSummarySerializer()
    location = LocationSummarySerializer()
    trigger = EvolutionTriggerSummarySerializer(source="evolution_trigger")
    region_id = RegionSummarySerializer(source="region")
    base_form_id = PokemonSpeciesSummarySerializer(source="base_form")

    class Meta:
        model = PokemonEvolution
        fields = (
            "item",
            "trigger",
            "gender",
            "held_item",
            "known_move",
            "known_move_type",
            "location",
            "min_level",
            "min_happiness",
            "min_beauty",
            "min_affection",
            "needs_overworld_rain",
            "party_species",
            "party_type",
            "relative_physical_stats",
            "time_of_day",
            "trade_species",
            "turn_upside_down",
            "region_id",
            "base_form_id",
        )


class EvolutionChainDetailSerializer(serializers.ModelSerializer):
    baby_trigger_item = ItemSummarySerializer()
    chain = serializers.SerializerMethodField("build_chain")

    class Meta:
        model = EvolutionChain
        fields = ("id", "baby_trigger_item", "chain")

    # TODO: Revisit Schema
    @extend_schema_field(
        field={
            "type": "object",
            "required": ["evolution_details", "evolves_to", "is_baby", "species"],
            "properties": {
                "evolution_details": {"type": "array", "items": {}, "examples": []},
                "evolves_to": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": [
                            "evolution_details",
                            "evolves_to",
                            "is_baby",
                            "species",
                        ],
                        "properties": {
                            "evolution_details": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "required": [
                                        "gender",
                                        "held_item",
                                        "item",
                                        "known_move",
                                        "known_move_type",
                                        "location",
                                        "min_affection",
                                        "min_beauty",
                                        "min_happiness",
                                        "min_level",
                                        "needs_overworld_rain",
                                        "party_species",
                                        "party_type",
                                        "relative_physical_stats",
                                        "time_of_day",
                                        "trade_species",
                                        "trigger",
                                        "turn_upside_down",
                                        "region_id",
                                        "base_form_id",
                                    ],
                                    "properties": {
                                        "gender": {
                                            "type": "",
                                            "nullable": True,
                                            "type": "object",
                                            "required": ["name", "url"],
                                            "properties": {
                                                "name": {
                                                    "type": "string",
                                                    "examples": [1],
                                                },
                                                "url": {
                                                    "type": "string",
                                                    "format": "uri",
                                                    "examples": [2],
                                                },
                                            },
                                        },
                                        "held_item": {
                                            "type": "object",
                                            "nullable": True,
                                            "required": ["name", "url"],
                                            "properties": {
                                                "name": {
                                                    "type": "string",
                                                    "examples": [1],
                                                },
                                                "url": {
                                                    "type": "string",
                                                    "format": "uri",
                                                    "examples": [2],
                                                },
                                            },
                                        },
                                        "item": {
                                            "type": "object",
                                            "nullable": True,
                                            "required": ["name", "url"],
                                            "properties": {
                                                "name": {
                                                    "type": "string",
                                                    "examples": [1],
                                                },
                                                "url": {
                                                    "type": "string",
                                                    "format": "uri",
                                                    "examples": [2],
                                                },
                                            },
                                        },
                                        "known_move": {
                                            "type": "",
                                            "nullable": True,
                                        },
                                        "known_move_type": {
                                            "type": "",
                                            "nullable": True,
                                        },
                                        "location": {
                                            "type": "object",
                                            "nullable": True,
                                            "required": ["name", "url"],
                                            "properties": {
                                                "name": {
                                                    "type": "string",
                                                },
                                                "url": {
                                                    "type": "string",
                                                    "format": "uri",
                                                },
                                            },
                                        },
                                        "min_affection": {
                                            "type": "integer",
                                            "format": "int32",
                                            "nullable": True,
                                        },
                                        "min_beauty": {
                                            "type": "integer",
                                            "format": "int32",
                                            "nullable": True,
                                        },
                                        "min_happiness": {
                                            "type": "integer",
                                            "format": "int32",
                                            "nullable": True,
                                        },
                                        "min_level": {
                                            "type": "integer",
                                            "format": "int32",
                                            "nullable": True,
                                        },
                                        "needs_overworld_rain": {
                                            "type": "boolean",
                                            "nullable": True,
                                        },
                                        "party_species": {
                                            "type": "string",
                                            "nullable": True,
                                        },
                                        "party_type": {
                                            "type": "string",
                                            "nullable": True,
                                        },
                                        "relative_physical_stats": {
                                            "type": "string",
                                            "nullable": True,
                                        },
                                        "time_of_day": {"type": "string"},
                                        "trade_species": {
                                            "type": "string",
                                            "nullable": True,
                                        },
                                        "trigger": {
                                            "type": "object",
                                            "required": ["name", "url"],
                                            "properties": {
                                                "name": {
                                                    "type": "string",
                                                },
                                                "url": {
                                                    "type": "string",
                                                    "format": "uri",
                                                },
                                            },
                                        },
                                        "turn_upside_down": {"type": "boolean"},
                                        "region_id": {
                                            "type": "object",
                                            "nullable": True,
                                            "required": ["name", "url"],
                                            "properties": {
                                                "name": {"type": "string"},
                                                "url": {
                                                    "type": "string",
                                                    "format": "uri",
                                                },
                                            },
                                        },
                                        "base_form_id": {
                                            "type": "object",
                                            "nullable": True,
                                            "required": ["name", "url"],
                                            "properties": {
                                                "name": {"type": "string"},
                                                "url": {
                                                    "type": "string",
                                                    "format": "uri",
                                                },
                                            },
                                        },
                                    },
                                },
                            },
                            "is_baby": {"type": "boolean"},
                            "species": {
                                "type": "object",
                                "required": ["name", "url"],
                                "properties": {
                                    "name": {"type": "string", "examples": ["happiny"]},
                                    "url": {
                                        "type": "string",
                                        "format": "uri",
                                        "examples": [
                                            "https://pokeapi.co/api/v2/pokemon-species/440/"
                                        ],
                                    },
                                },
                            },
                        },
                    },
                },
                "is_baby": {"type": "boolean"},
                "species": {
                    "type": "object",
                    "required": ["name", "url"],
                    "properties": {
                        "name": {"type": "string", "examples": ["happiny"]},
                        "url": {
                            "type": "string",
                            "format": "uri",
                            "examples": [
                                "https://pokeapi.co/api/v2/pokemon-species/440/"
                            ],
                        },
                    },
                },
            },
        }
    )
    def build_chain(self, obj):
        chain_id = obj.id

        pokemon_objects = PokemonSpecies.objects.filter(
            evolution_chain_id=chain_id
        ).order_by("order")
        summary_data = PokemonSpeciesSummarySerializer(
            pokemon_objects, many=True, context=self.context
        ).data
        ref_data = PokemonSpeciesEvolutionSerializer(
            pokemon_objects, many=True, context=self.context
        ).data

        # convert evolution data list to tree
        evolution_tree = self.build_evolution_tree(ref_data)

        # serialize chain recursively from tree
        chain = self.build_chain_link_entry(evolution_tree, summary_data)

        return chain

    # converts a list of Pokemon species evolution data into a tree representing the evolution chain
    def build_evolution_tree(self, species_evolution_data):
        evolution_tree = OrderedDict()
        evolution_tree["species"] = species_evolution_data[0]
        evolution_tree["children"] = []

        for species in species_evolution_data[1:]:
            chain_link = OrderedDict()
            chain_link["species"] = species
            chain_link["children"] = []

            evolves_from_species_id = chain_link["species"]["evolves_from_species"]

            # find parent link by DFS
            parent_link = evolution_tree
            search_stack = [parent_link]

            while len(search_stack) > 0:
                l = search_stack.pop()
                if l["species"]["id"] == evolves_from_species_id:
                    parent_link = l
                    break

                # "left" to "right" requires reversing the list of children
                search_stack += reversed(l["children"])

            parent_link["children"].append(chain_link)

        return evolution_tree

    # serializes an evolution chain link recursively
    # chain_link is a tree representing an evolution chain
    def build_chain_link_entry(self, chain_link, summary_data):
        entry = OrderedDict()
        evolution_data = None

        species = chain_link["species"]
        if species["evolves_from_species"]:
            evolution_object = PokemonEvolution.objects.filter(
                evolved_species=species["id"]
            )

            evolution_data = PokemonEvolutionSerializer(
                evolution_object, many=True, context=self.context
            ).data

        entry["is_baby"] = species["is_baby"]

        species_summary = next(x for x in summary_data if x["name"] == species["name"])
        entry["species"] = species_summary

        entry["evolution_details"] = evolution_data or []

        evolves_to = [
            self.build_chain_link_entry(c, summary_data) for c in chain_link["children"]
        ]
        entry["evolves_to"] = evolves_to

        return entry


class PokemonDexNumberSerializer(serializers.ModelSerializer):
    entry_number = serializers.IntegerField(source="pokedex_number")
    pokemon_species = PokemonSpeciesSummarySerializer()

    class Meta:
        model = PokemonDexNumber
        fields = ("pokedex", "entry_number", "pokemon_species")


############################
#  POKEATHLON SERIALIZERS  #
############################
class PokeathlonStatNameSerializer(serializers.HyperlinkedModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = PokeathlonStatName
        fields = ("name", "language")


class PokeathlonStatDetailSerializer(serializers.HyperlinkedModelSerializer):
    names = PokeathlonStatNameSerializer(
        many=True, read_only=True, source="pokeathlonstatname"
    )
    affecting_natures = serializers.SerializerMethodField("get_natures_that_affect")

    class Meta:
        model = PokeathlonStat
        fields = ("id", "name", "affecting_natures", "names")

    @extend_schema_field(
        field={
            "type": "object",
            "required": ["decrease", "increase"],
            "properties": {
                "decrease": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["max_change", "nature"],
                        "properties": {
                            "max_change": {
                                "type": "integer",
                                "format": "int32",
                                "maximum": -1,
                                "examples": [-1],
                            },
                            "nature": {
                                "type": "object",
                                "required": ["name", "url"],
                                "properties": {
                                    "name": {"type": "string", "examples": ["hardy"]},
                                    "url": {
                                        "type": "string",
                                        "format": "uri",
                                        "examples": [
                                            "https://pokeapi.co/api/v2/nature/1/"
                                        ],
                                    },
                                },
                            },
                        },
                    },
                },
                "increase": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["max_change", "nature"],
                        "properties": {
                            "max_change": {
                                "type": "integer",
                                "format": "int32",
                                "minimum": 1,
                                "examples": [2],
                            },
                            "nature": {
                                "type": "object",
                                "required": ["name", "url"],
                                "properties": {
                                    "name": {"type": "string", "examples": ["hardy"]},
                                    "url": {
                                        "type": "string",
                                        "format": "uri",
                                        "examples": [
                                            "https://pokeapi.co/api/v2/nature/1/"
                                        ],
                                    },
                                },
                            },
                        },
                    },
                },
            },
        }
    )
    def get_natures_that_affect(self, obj):
        stat_change_objects = NaturePokeathlonStat.objects.filter(pokeathlon_stat=obj)
        stat_changes = NaturePokeathlonStatSerializer(
            stat_change_objects, many=True, context=self.context
        ).data
        changes = OrderedDict([("increase", []), ("decrease", [])])

        for change in stat_changes:
            del change["pokeathlon_stat"]
            if change["max_change"] > 0:
                changes["increase"].append(change)
            else:
                changes["decrease"].append(change)

        return changes


#########################
#  POKEDEX SERIALIZERS  #
#########################
class PokedexNameSerializer(serializers.HyperlinkedModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = PokedexName
        fields = ("name", "language")


class PokedexDescriptionSerializer(serializers.HyperlinkedModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = PokedexDescription
        fields = ("description", "language")


class PokedexDetailSerializer(serializers.ModelSerializer):
    region = RegionSummarySerializer()
    names = PokedexNameSerializer(many=True, read_only=True, source="pokedexname")
    descriptions = PokedexDescriptionSerializer(
        many=True, read_only=True, source="pokedexdescription"
    )
    pokemon_entries = serializers.SerializerMethodField("get_pokedex_entries")
    version_groups = serializers.SerializerMethodField("get_pokedex_version_groups")

    class Meta:
        model = Pokedex
        fields = (
            "id",
            "name",
            "is_main_series",
            "descriptions",
            "names",
            "pokemon_entries",
            "region",
            "version_groups",
        )

    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["entry_number", "pokemon_species"],
                "properties": {
                    "entry_number": {
                        "type": "integer",
                        "format": "int32",
                        "examples": [1],
                    },
                    "pokemon_species": {
                        "type": "object",
                        "required": ["name", "url"],
                        "properties": {
                            "name": {"type": "string", "examples": ["bulbasaur"]},
                            "url": {
                                "type": "string",
                                "format": "uri",
                                "examples": [
                                    "https://pokeapi.co/api/v2/pokemon-species/1/"
                                ],
                            },
                        },
                    },
                },
            },
        }
    )
    def get_pokedex_entries(self, obj):
        results = PokemonDexNumber.objects.filter(pokedex=obj).order_by(
            "pokedex_number"
        )
        serializer = PokemonDexNumberSerializer(
            results, many=True, context=self.context
        )
        data = serializer.data

        for entry in data:
            del entry["pokedex"]

        return data

    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name", "url"],
                "properties": {
                    "name": {"type": "string", "examples": ["the-teal-mask"]},
                    "url": {
                        "type": "string",
                        "format": "uri",
                        "examples": ["https://pokeapi.co/api/v2/version-group/26/"],
                    },
                },
            },
        }
    )
    def get_pokedex_version_groups(self, obj):
        dex_group_objects = PokedexVersionGroup.objects.filter(pokedex=obj)
        dex_groups = PokedexVersionGroupSerializer(
            dex_group_objects, many=True, context=self.context
        ).data
        results = []

        for dex_group in dex_groups:
            results.append(dex_group["version_group"])

        return results


#########################
#  VERSION SERIALIZERS  #
#########################
class VersionNameSerializer(serializers.ModelSerializer):
    language = LanguageSummarySerializer()

    class Meta:
        model = VersionName
        fields = ("name", "language")


class VersionDetailSerializer(serializers.ModelSerializer):
    """
    Should have a link to Version Group info but the Circular
    dependency and compilation order fight eachother and I'm
    not sure how to add anything other than a hyperlink
    """

    names = VersionNameSerializer(many=True, read_only=True, source="versionname")
    version_group = VersionGroupSummarySerializer()

    class Meta:
        model = Version
        fields = ("id", "name", "names", "version_group")


class VersionGroupDetailSerializer(serializers.ModelSerializer):
    generation = GenerationSummarySerializer()
    versions = VersionSummarySerializer(many=True, read_only=True, source="version")
    regions = serializers.SerializerMethodField("get_version_group_regions")
    move_learn_methods = serializers.SerializerMethodField("get_learn_methods")
    pokedexes = serializers.SerializerMethodField("get_version_groups_pokedexes")

    class Meta:
        model = VersionGroup
        fields = (
            "id",
            "name",
            "order",
            "generation",
            "move_learn_methods",
            "pokedexes",
            "regions",
            "versions",
        )

    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name", "url"],
                "properties": {
                    "name": {"type": "string", "examples": ["kanto"]},
                    "url": {
                        "type": "string",
                        "format": "uri",
                        "examples": ["https://pokeapi.co/api/v2/region/1/"],
                    },
                },
            },
        }
    )
    def get_version_group_regions(self, obj):
        vg_regions = VersionGroupRegion.objects.filter(version_group=obj)
        data = VersionGroupRegionSerializer(
            vg_regions, many=True, context=self.context
        ).data
        regions = []

        for region in data:
            regions.append(region["region"])

        return regions

    # "name": "level-up",
    # "url": "https://pokeapi.co/api/v2/move-learn-method/1/"
    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name", "url"],
                "properties": {
                    "name": {"type": "string", "examples": ["level-up"]},
                    "url": {
                        "type": "string",
                        "format": "uri",
                        "examples": ["https://pokeapi.co/api/v2/move-learn-method/1/"],
                    },
                },
            },
        }
    )
    def get_learn_methods(self, obj):
        learn_method_objects = VersionGroupMoveLearnMethod.objects.filter(
            version_group=obj
        )
        learn_method_data = VersionGroupMoveLearnMethodSerializer(
            learn_method_objects, many=True, context=self.context
        ).data
        methods = []

        for method in learn_method_data:
            methods.append(method["move_learn_method"])

        return methods

    @extend_schema_field(
        field={
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name", "url"],
                "properties": {
                    "name": {"type": "string", "examples": ["kanto"]},
                    "url": {
                        "type": "string",
                        "format": "uri",
                        "examples": ["https://pokeapi.co/api/v2/pokedex/2/"],
                    },
                },
            },
        }
    )
    def get_version_groups_pokedexes(self, obj):
        dex_group_objects = PokedexVersionGroup.objects.filter(version_group=obj)
        dex_groups = PokedexVersionGroupSerializer(
            dex_group_objects, many=True, context=self.context
        ).data
        results = []

        for dex_group in dex_groups:
            results.append(dex_group["pokedex"])

        return results
