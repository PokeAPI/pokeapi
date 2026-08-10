# ruff: noqa: F405
# pyright: reportIncompatibleVariableOverride=false, reportUnknownMemberType=false
from __future__ import annotations

import itertools
from typing import TYPE_CHECKING, Any, ClassVar, Protocol, cast

from django.db.models import Q
from drf_spectacular.utils import extend_schema_field  # pyright: ignore[reportUnknownVariableType]
from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import *  # noqa: F403

if TYPE_CHECKING:
    from collections.abc import Sequence

    from django.db import models
    from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList

    class EncounterWithRelations(Protocol):
        encounterconditionvaluemap_set: models.Manager[EncounterConditionValueMap]
        encounterpokemondetail_set: models.Manager[EncounterPokemonDetail]

    class PokemonWithRelations(Protocol):
        pokemonsprites: models.Manager[PokemonSprites]
        pokemoncries: models.Manager[PokemonCries]


__all__: tuple[str, ...] = (
    "AbilityChangeEffectTextSerializer",
    "AbilityChangeSerializer",
    "AbilityDetailSerializer",
    "AbilityEffectTextSerializer",
    "AbilityFlavorTextSerializer",
    "AbilityNameSerializer",
    "AbilityPokemonDetailSerializer",
    "AbilitySummarySerializer",
    "BerryDetailSerializer",
    "BerryFirmnessDetailSerializer",
    "BerryFirmnessNameSerializer",
    "BerryFirmnessSummarySerializer",
    "BerryFlavorBerryMapSerializer",
    "BerryFlavorDetailSerializer",
    "BerryFlavorMapSerializer",
    "BerryFlavorNameSerializer",
    "BerryFlavorSummarySerializer",
    "BerrySummarySerializer",
    "CharacteristicDescriptionSerializer",
    "CharacteristicDetailSerializer",
    "CharacteristicSummarySerializer",
    "ContestEffectDetailSerializer",
    "ContestEffectEffectTextSerializer",
    "ContestEffectFlavorTextSerializer",
    "ContestEffectSummarySerializer",
    "ContestTypeDetailSerializer",
    "ContestTypeNameSerializer",
    "ContestTypeSummarySerializer",
    "CurrencyDetailSerializer",
    "CurrencyNameSerializer",
    "CurrencySummarySerializer",
    "EggGroupDetailSerializer",
    "EggGroupNameSerializer",
    "EggGroupSummarySerializer",
    "EncounterConditionDetailSerializer",
    "EncounterConditionNameSerializer",
    "EncounterConditionSummarySerializer",
    "EncounterConditionValueDetailSerializer",
    "EncounterConditionValueMapSerializer",
    "EncounterConditionValueNameSerializer",
    "EncounterConditionValueSummarySerializer",
    "EncounterDetailSerializer",
    "EncounterMethodDetailSerializer",
    "EncounterMethodNameSerializer",
    "EncounterMethodSummarySerializer",
    "EncounterPokemonDetailSerializer",
    "EncounterSlotSerializer",
    "EvolutionChainDetailSerializer",
    "EvolutionChainLinkSerializer",
    "EvolutionChainSummarySerializer",
    "EvolutionTriggerDetailSerializer",
    "EvolutionTriggerNameSerializer",
    "EvolutionTriggerSummarySerializer",
    "ExperienceSerializer",
    "GenderDetailSerializer",
    "GenderPokemonSpeciesSerializer",
    "GenderSummarySerializer",
    "GenerationDetailSerializer",
    "GenerationNameSerializer",
    "GenerationSummarySerializer",
    "GrowthRateDescriptionSerializer",
    "GrowthRateDetailSerializer",
    "GrowthRateSummarySerializer",
    "ItemAttributeDescriptionSerializer",
    "ItemAttributeDetailSerializer",
    "ItemAttributeNameSerializer",
    "ItemAttributeSummarySerializer",
    "ItemCategoryDetailSerializer",
    "ItemCategoryNameSerializer",
    "ItemCategorySummarySerializer",
    "ItemDetailSerializer",
    "ItemEffectTextSerializer",
    "ItemFlavorTextSerializer",
    "ItemFlingEffectDetailSerializer",
    "ItemFlingEffectEffectTextSerializer",
    "ItemFlingEffectSummarySerializer",
    "ItemGameIndexSerializer",
    "ItemMachineSerializer",
    "ItemNameSerializer",
    "ItemPocketDetailSerializer",
    "ItemPocketNameSerializer",
    "ItemPocketSummarySerializer",
    "ItemPriceSerializer",
    "ItemSpritesSerializer",
    "ItemSummarySerializer",
    "LanguageDetailSerializer",
    "LanguageNameSerializer",
    "LanguageSummarySerializer",
    "LocationAreaDetailSerializer",
    "LocationAreaEncounterDetailSerializer",
    "LocationAreaEncounterRateSerializer",
    "LocationAreaEncounterVersionDetailSerializer",
    "LocationAreaNameSerializer",
    "LocationAreaPokemonEncounterSerializer",
    "LocationAreaPokemonEncounterVersionSerializer",
    "LocationAreaSummarySerializer",
    "LocationDetailSerializer",
    "LocationGameIndexSerializer",
    "LocationNameSerializer",
    "LocationSummarySerializer",
    "MachineDetailSerializer",
    "MachineSummarySerializer",
    "MoveBattleStyleDetailSerializer",
    "MoveBattleStyleNameSerializer",
    "MoveBattleStyleSummarySerializer",
    "MoveChangeSerializer",
    "MoveComboUsageSerializer",
    "MoveCombosSerializer",
    "MoveDamageClassDescriptionSerializer",
    "MoveDamageClassDetailSerializer",
    "MoveDamageClassNameSerializer",
    "MoveDamageClassSummarySerializer",
    "MoveDetailSerializer",
    "MoveEffectChangeEffectTextSerializer",
    "MoveEffectChangeSerializer",
    "MoveEffectEffectTextSerializer",
    "MoveFlavorTextSerializer",
    "MoveLearnMethodDescriptionSerializer",
    "MoveLearnMethodDetailSerializer",
    "MoveLearnMethodNameSerializer",
    "MoveLearnMethodSummarySerializer",
    "MoveMetaAilmentDetailSerializer",
    "MoveMetaAilmentNameSerializer",
    "MoveMetaAilmentSummarySerializer",
    "MoveMetaCategoryDescriptionSerializer",
    "MoveMetaCategoryDetailSerializer",
    "MoveMetaCategorySummarySerializer",
    "MoveMetaSerializer",
    "MoveMetaStatChangeSerializer",
    "MoveNameSerializer",
    "MoveStatChangeSerializer",
    "MoveSummarySerializer",
    "MoveTargetDescriptionSerializer",
    "MoveTargetDetailSerializer",
    "MoveTargetNameSerializer",
    "MoveTargetSummarySerializer",
    "NatureBattleStylePreferenceSerializer",
    "NatureDetailSerializer",
    "NatureNameSerializer",
    "NaturePokeathlonStatSerializer",
    "NatureSummarySerializer",
    "PalParkAreaDetailSerializer",
    "PalParkAreaNameSerializer",
    "PalParkAreaSummarySerializer",
    "PalParkEncounterSerializer",
    "PokeathlonStatAffectingNatureSerializer",
    "PokeathlonStatAffectingNaturesSerializer",
    "PokeathlonStatDetailSerializer",
    "PokeathlonStatNameSerializer",
    "PokeathlonStatSummarySerializer",
    "PokedexDescriptionSerializer",
    "PokedexDetailSerializer",
    "PokedexNameSerializer",
    "PokedexSummarySerializer",
    "PokemonAbilityPastSerializer",
    "PokemonAbilitySerializer",
    "PokemonColorDetailSerializer",
    "PokemonColorNameSerializer",
    "PokemonColorSummarySerializer",
    "PokemonCriesSerializer",
    "PokemonDetailSerializer",
    "PokemonDexEntrySerializer",
    "PokemonDexNumberSerializer",
    "PokemonEvolutionSerializer",
    "PokemonFormConditionSerializer",
    "PokemonFormDetailSerializer",
    "PokemonFormNameSerializer",
    "PokemonFormSpritesSerializer",
    "PokemonFormSummarySerializer",
    "PokemonFormTriggerConditionSerializer",
    "PokemonFormTypeSerializer",
    "PokemonGameIndexSerializer",
    "PokemonHabitatDetailSerializer",
    "PokemonHabitatNameSerializer",
    "PokemonHabitatSummarySerializer",
    "PokemonHeldItemSerializer",
    "PokemonHeldItemVersionSerializer",
    "PokemonMoveSerializer",
    "PokemonMoveVersionGroupSerializer",
    "PokemonPastAbilitySerializer",
    "PokemonPastStatSerializer",
    "PokemonPastTypeSerializer",
    "PokemonShapeAwesomeNameSerializer",
    "PokemonShapeDetailSerializer",
    "PokemonShapeNameSerializer",
    "PokemonShapeSummarySerializer",
    "PokemonSpeciesDescriptionSerializer",
    "PokemonSpeciesDetailSerializer",
    "PokemonSpeciesEvolutionSerializer",
    "PokemonSpeciesFlavorTextSerializer",
    "PokemonSpeciesGenusSerializer",
    "PokemonSpeciesNameSerializer",
    "PokemonSpeciesPalParkEncounterSerializer",
    "PokemonSpeciesSummarySerializer",
    "PokemonSpeciesVarietySerializer",
    "PokemonSpritesSerializer",
    "PokemonStatPastSerializer",
    "PokemonStatSerializer",
    "PokemonSummarySerializer",
    "PokemonTypePastSerializer",
    "PokemonTypeSerializer",
    "RegionDetailSerializer",
    "RegionNameSerializer",
    "RegionSummarySerializer",
    "StatAffectingMovesSerializer",
    "StatAffectingNaturesSerializer",
    "StatDetailSerializer",
    "StatNameSerializer",
    "StatSummarySerializer",
    "SuperContestEffectDetailSerializer",
    "SuperContestEffectFlavorTextSerializer",
    "SuperContestEffectSummarySerializer",
    "TypeDetailSerializer",
    "TypeEfficacyPastSerializer",
    "TypeGameIndexSerializer",
    "TypeNameSerializer",
    "TypePastRelationshipsSerializer",
    "TypePokemonSerializer",
    "TypeRelationshipsSerializer",
    "TypeSpriteSerializer",
    "TypeSummarySerializer",
    "VersionDetailSerializer",
    "VersionGroupDetailSerializer",
    "VersionGroupSummarySerializer",
    "VersionNameSerializer",
    "VersionSummarySerializer",
)

# PokeAPI v2 serializers in order of dependency

#########################
#  SUMMARY SERIALIZERS  #
#########################

# Summary serializers are just for list and reference behavior

# Putting summary serializers up top so there are no conflicts
# with reference accross models due to script running order


class AbilitySummarySerializer(serializers.HyperlinkedModelSerializer[Ability]):
    class Meta:
        model = Ability
        fields = ("name", "url")


class BerryFirmnessSummarySerializer(serializers.HyperlinkedModelSerializer[BerryFirmness]):
    class Meta:
        model = BerryFirmness
        fields = ("name", "url")


class BerryFlavorSummarySerializer(serializers.HyperlinkedModelSerializer[BerryFlavor]):
    class Meta:
        model = BerryFlavor
        fields = ("name", "url")


class BerrySummarySerializer(serializers.HyperlinkedModelSerializer[Berry]):
    class Meta:
        model = Berry
        fields = ("name", "url")


class CharacteristicSummarySerializer(serializers.HyperlinkedModelSerializer[Characteristic]):
    class Meta:
        model = Characteristic
        fields = ("url",)


class ContestEffectSummarySerializer(serializers.HyperlinkedModelSerializer[ContestEffect]):
    class Meta:
        model = ContestEffect
        fields = ("url",)


class ContestTypeSummarySerializer(serializers.HyperlinkedModelSerializer[ContestType]):
    class Meta:
        model = ContestType
        fields = ("name", "url")


class EggGroupSummarySerializer(serializers.HyperlinkedModelSerializer[EggGroup]):
    class Meta:
        model = EggGroup
        fields = ("name", "url")


class EncounterConditionSummarySerializer(serializers.HyperlinkedModelSerializer[EncounterCondition]):
    class Meta:
        model = EncounterCondition
        fields = ("name", "url")


class EncounterConditionValueSummarySerializer(serializers.HyperlinkedModelSerializer[EncounterConditionValue]):
    class Meta:
        model = EncounterConditionValue
        fields = ("name", "url")


class EncounterMethodSummarySerializer(serializers.HyperlinkedModelSerializer[EncounterMethod]):
    class Meta:
        model = EncounterMethod
        fields = ("name", "url")


class EvolutionTriggerSummarySerializer(serializers.HyperlinkedModelSerializer[EvolutionTrigger]):
    class Meta:
        model = EvolutionTrigger
        fields = ("name", "url")


class EvolutionChainSummarySerializer(serializers.HyperlinkedModelSerializer[EvolutionChain]):
    class Meta:
        model = EvolutionChain
        fields = ("url",)


class GenerationSummarySerializer(serializers.HyperlinkedModelSerializer[Generation]):
    class Meta:
        model = Generation
        fields = ("name", "url")


class GenderSummarySerializer(serializers.HyperlinkedModelSerializer[Gender]):
    class Meta:
        model = Gender
        fields = ("name", "url")


class GrowthRateSummarySerializer(serializers.HyperlinkedModelSerializer[GrowthRate]):
    class Meta:
        model = GrowthRate
        fields = ("name", "url")


class CurrencySummarySerializer(serializers.HyperlinkedModelSerializer[Currency]):
    class Meta:
        model = Currency
        fields = ("name", "url")


class ItemPocketSummarySerializer(serializers.HyperlinkedModelSerializer[ItemPocket]):
    class Meta:
        model = ItemPocket
        fields = ("name", "url")


class ItemCategorySummarySerializer(serializers.HyperlinkedModelSerializer[ItemCategory]):
    class Meta:
        model = ItemCategory
        fields = ("name", "url")


class ItemAttributeSummarySerializer(serializers.HyperlinkedModelSerializer[ItemAttribute]):
    class Meta:
        model = ItemAttribute
        fields = ("name", "url")


class ItemFlingEffectSummarySerializer(serializers.HyperlinkedModelSerializer[ItemFlingEffect]):
    class Meta:
        model = ItemFlingEffect
        fields = ("name", "url")


class ItemSummarySerializer(serializers.HyperlinkedModelSerializer[Item]):
    class Meta:
        model = Item
        fields = ("name", "url")


class LanguageSummarySerializer(serializers.HyperlinkedModelSerializer[Language]):
    class Meta:
        model = Language
        fields = ("name", "url")


class LocationSummarySerializer(serializers.HyperlinkedModelSerializer[Location]):
    class Meta:
        model = Location
        fields = ("name", "url")


class LocationAreaSummarySerializer(serializers.HyperlinkedModelSerializer[LocationArea]):
    class Meta:
        model = LocationArea
        fields = ("name", "url")


class MachineSummarySerializer(serializers.HyperlinkedModelSerializer[Machine]):
    class Meta:
        model = Machine
        fields = ("url",)


class MoveBattleStyleSummarySerializer(serializers.HyperlinkedModelSerializer[MoveBattleStyle]):
    class Meta:
        model = MoveBattleStyle
        fields = ("name", "url")


class MoveDamageClassSummarySerializer(serializers.HyperlinkedModelSerializer[MoveDamageClass]):
    class Meta:
        model = MoveDamageClass
        fields = ("name", "url")


class MoveMetaAilmentSummarySerializer(serializers.HyperlinkedModelSerializer[MoveMetaAilment]):
    class Meta:
        model = MoveMetaAilment
        fields = ("name", "url")


class MoveMetaCategorySummarySerializer(serializers.HyperlinkedModelSerializer[MoveMetaCategory]):
    class Meta:
        model = MoveMetaCategory
        fields = ("name", "url")


class MoveTargetSummarySerializer(serializers.HyperlinkedModelSerializer[MoveTarget]):
    class Meta:
        model = MoveTarget
        fields = ("name", "url")


class MoveSummarySerializer(serializers.HyperlinkedModelSerializer[Move]):
    class Meta:
        model = Move
        fields = ("name", "url")


class MoveLearnMethodSummarySerializer(serializers.HyperlinkedModelSerializer[MoveLearnMethod]):
    class Meta:
        model = MoveLearnMethod
        fields = ("name", "url")


class NatureSummarySerializer(serializers.HyperlinkedModelSerializer[Nature]):
    class Meta:
        model = Nature
        fields = ("name", "url")


class PalParkAreaSummarySerializer(serializers.HyperlinkedModelSerializer[PalParkArea]):
    class Meta:
        model = PalParkArea
        fields = ("name", "url")


class PokeathlonStatSummarySerializer(serializers.HyperlinkedModelSerializer[PokeathlonStat]):
    class Meta:
        model = PokeathlonStat
        fields = ("name", "url")


class PokedexSummarySerializer(serializers.HyperlinkedModelSerializer[Pokedex]):
    class Meta:
        model = Pokedex
        fields = ("name", "url")


class PokemonColorSummarySerializer(serializers.HyperlinkedModelSerializer[PokemonColor]):
    class Meta:
        model = PokemonColor
        fields = ("name", "url")


class PokemonHabitatSummarySerializer(serializers.HyperlinkedModelSerializer[PokemonHabitat]):
    class Meta:
        model = PokemonHabitat
        fields = ("name", "url")


class PokemonShapeSummarySerializer(serializers.HyperlinkedModelSerializer[PokemonShape]):
    class Meta:
        model = PokemonShape
        fields = ("name", "url")


class PokemonSummarySerializer(serializers.HyperlinkedModelSerializer[Pokemon]):
    class Meta:
        model = Pokemon
        fields = ("name", "url")


class PokemonSpeciesSummarySerializer(serializers.HyperlinkedModelSerializer[PokemonSpecies]):
    class Meta:
        model = PokemonSpecies
        fields = ("name", "url")


class PokemonFormSummarySerializer(serializers.HyperlinkedModelSerializer[PokemonForm]):
    class Meta:
        model = PokemonForm
        fields = ("name", "url")


class RegionSummarySerializer(serializers.HyperlinkedModelSerializer[Region]):
    class Meta:
        model = Region
        fields = ("name", "url")


class StatSummarySerializer(serializers.HyperlinkedModelSerializer[Stat]):
    class Meta:
        model = Stat
        fields = ("name", "url")


class SuperContestEffectSummarySerializer(serializers.HyperlinkedModelSerializer[SuperContestEffect]):
    class Meta:
        model = SuperContestEffect
        fields = ("url",)


class TypeSummarySerializer(serializers.HyperlinkedModelSerializer[Type]):
    class Meta:
        model = Type
        fields = ("name", "url")


class VersionSummarySerializer(serializers.HyperlinkedModelSerializer[Version]):
    class Meta:
        model = Version
        fields = ("name", "url")


class VersionGroupSummarySerializer(serializers.HyperlinkedModelSerializer[VersionGroup]):
    class Meta:
        model = VersionGroup
        fields = ("name", "url")


#####################
#  MAP SERIALIZERS  #
#####################


class PokemonDexEntrySerializer(serializers.ModelSerializer[PokemonDexNumber]):
    entry_number = serializers.IntegerField(source="pokedex_number")
    pokedex = PokedexSummarySerializer()

    class Meta:
        model = PokemonDexNumber
        fields = ("entry_number", "pokedex")


class EncounterConditionValueMapSerializer(serializers.ModelSerializer[EncounterConditionValueMap]):
    condition_value = EncounterConditionValueSummarySerializer(source="encounter_condition_value")

    class Meta:
        model = EncounterConditionValueMap
        fields = ("condition_value",)


################################
#  CHARACTERISTIC SERIALIZERS  #
################################


class CharacteristicDescriptionSerializer(serializers.ModelSerializer[CharacteristicDescription]):
    language = LanguageSummarySerializer()

    class Meta:
        model = CharacteristicDescription
        fields = ("description", "language")


class CharacteristicDetailSerializer(serializers.ModelSerializer[Characteristic]):
    descriptions = CharacteristicDescriptionSerializer(many=True, read_only=True, source="characteristicdescription")
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

    @extend_schema_field(serializers.ListField(child=serializers.IntegerField()))
    def get_values(self, obj: Characteristic) -> list[int]:
        return list(range(obj.gene_mod_5, 32, 5))


#########################
#  CONTEST SERIALIZERS  #
#########################


class SuperContestEffectFlavorTextSerializer(serializers.ModelSerializer[SuperContestEffectFlavorText]):
    language = LanguageSummarySerializer()

    class Meta:
        model = SuperContestEffectFlavorText
        fields = ("flavor_text", "language")


class SuperContestEffectDetailSerializer(serializers.ModelSerializer[SuperContestEffect]):
    flavor_text_entries = SuperContestEffectFlavorTextSerializer(
        many=True, read_only=True, source="supercontesteffectflavortext"
    )
    moves = MoveSummarySerializer(many=True, read_only=True, source="move")

    class Meta:
        model = SuperContestEffect
        fields = ("id", "appeal", "flavor_text_entries", "moves")


class ContestEffectEffectTextSerializer(serializers.ModelSerializer[ContestEffectEffectText]):
    language = LanguageSummarySerializer()

    class Meta:
        model = ContestEffectEffectText
        fields = ("effect", "language")


class ContestEffectFlavorTextSerializer(serializers.ModelSerializer[ContestEffectFlavorText]):
    language = LanguageSummarySerializer()

    class Meta:
        model = ContestEffectFlavorText
        fields = ("flavor_text", "language")


class ContestEffectDetailSerializer(serializers.ModelSerializer[ContestEffect]):
    effect_entries = ContestEffectEffectTextSerializer(many=True, read_only=True, source="contesteffecteffecttext")
    flavor_text_entries = ContestEffectFlavorTextSerializer(many=True, read_only=True, source="contesteffectflavortext")

    class Meta:
        model = ContestEffect
        fields = ("id", "appeal", "jam", "effect_entries", "flavor_text_entries")


class ContestTypeNameSerializer(serializers.ModelSerializer[ContestTypeName]):
    language = LanguageSummarySerializer()

    class Meta:
        model = ContestTypeName
        fields = ("name", "color", "language")


class ContestTypeDetailSerializer(serializers.ModelSerializer[ContestType]):
    names = ContestTypeNameSerializer(many=True, read_only=True, source="contesttypename")
    berry_flavor = BerryFlavorSummarySerializer(read_only=True, source="berryflavor")

    class Meta:
        model = ContestType
        fields = ("id", "name", "berry_flavor", "names")


########################
#  REGION SERIALIZERS  #
########################


class RegionNameSerializer(serializers.ModelSerializer[RegionName]):
    language = LanguageSummarySerializer()

    class Meta:
        model = RegionName
        fields = ("name", "language")


class RegionDetailSerializer(serializers.ModelSerializer[Region]):
    names = RegionNameSerializer(many=True, read_only=True, source="regionname")
    locations = LocationSummarySerializer(many=True, read_only=True, source="location")
    version_groups = serializers.SerializerMethodField("get_region_version_groups")
    pokedexes = PokedexSummarySerializer(many=True, read_only=True, source="pokedex")
    main_generation = GenerationSummarySerializer(read_only=True, source="generation", allow_null=True)

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

    @extend_schema_field(VersionGroupSummarySerializer(many=True))
    def get_region_version_groups(self, obj: Region) -> ReturnList[ReturnDict[str, Any]]:
        version_groups = VersionGroup.objects.filter(versiongroupregion__region=obj).distinct()
        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            VersionGroupSummarySerializer(version_groups, many=True, context=self.context).data,
        )


############################
#  GENERATION SERIALIZERS  #
############################


class GenerationNameSerializer(serializers.ModelSerializer[GenerationName]):
    language = LanguageSummarySerializer()

    class Meta:
        model = GenerationName
        fields = ("name", "language")


class GenerationDetailSerializer(serializers.ModelSerializer[Generation]):
    main_region = RegionSummarySerializer(source="region")
    names = GenerationNameSerializer(many=True, read_only=True, source="generationname")
    abilities = AbilitySummarySerializer(many=True, read_only=True, source="ability")
    moves = MoveSummarySerializer(many=True, read_only=True, source="move")
    pokemon_species = PokemonSpeciesSummarySerializer(many=True, read_only=True, source="pokemonspecies")
    types = TypeSummarySerializer(many=True, read_only=True, source="type")
    version_groups = VersionGroupSummarySerializer(many=True, read_only=True, source="versiongroup")

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


class GenderPokemonSpeciesSerializer(serializers.ModelSerializer[PokemonSpecies]):
    rate = serializers.IntegerField(source="gender_rate")
    pokemon_species = PokemonSpeciesSummarySerializer(source="*")

    class Meta:
        model = PokemonSpecies
        fields = ("rate", "pokemon_species")


class GenderDetailSerializer(serializers.ModelSerializer[Gender]):
    pokemon_species_details = serializers.SerializerMethodField("get_species")
    required_for_evolution = serializers.SerializerMethodField("get_required")

    class Meta:
        model = Gender
        fields = ("id", "name", "pokemon_species_details", "required_for_evolution")

    @extend_schema_field(GenderPokemonSpeciesSerializer(many=True))
    def get_species(self, obj: Gender) -> ReturnList[ReturnDict[str, Any]]:
        gender_filters = {
            "female": Q(gender_rate__gt=0),
            "male": Q(gender_rate__range=[0, 7]),
            "genderless": Q(gender_rate=-1),
        }
        species_objects = PokemonSpecies.objects.filter(gender_filters.get(obj.name, Q(pk__in=[])))
        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            GenderPokemonSpeciesSerializer(species_objects, many=True, context=self.context).data,
        )

    @extend_schema_field(PokemonSpeciesSummarySerializer(many=True))
    def get_required(self, obj: Gender) -> ReturnList[ReturnDict[str, Any]]:
        species = PokemonSpecies.objects.filter(evolved_species__gender=obj).distinct().order_by("id")
        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            PokemonSpeciesSummarySerializer(species, many=True, context=self.context).data,
        )


#############################
#  GROWTH RATE SERIALIZERS  #
#############################


class ExperienceSerializer(serializers.ModelSerializer[Experience]):
    class Meta:
        model = Experience
        fields = ("level", "experience")


class GrowthRateDescriptionSerializer(serializers.ModelSerializer[GrowthRateDescription]):
    language = LanguageSummarySerializer()

    class Meta:
        model = GrowthRateDescription
        fields = ("description", "language")


class GrowthRateDetailSerializer(serializers.ModelSerializer[GrowthRate]):
    descriptions = GrowthRateDescriptionSerializer(many=True, read_only=True, source="growthratedescription")
    levels = ExperienceSerializer(many=True, read_only=True, source="experience")
    pokemon_species = PokemonSpeciesSummarySerializer(many=True, read_only=True, source="pokemonspecies")

    class Meta:
        model = GrowthRate
        fields = ("id", "name", "formula", "descriptions", "levels", "pokemon_species")


##########################
#  LANGUAGE SERIALIZERS  #
##########################


class LanguageNameSerializer(serializers.ModelSerializer[LanguageName]):
    language = LanguageSummarySerializer(source="local_language")

    class Meta:
        model = LanguageName
        fields = ("name", "language")


class LanguageDetailSerializer(serializers.ModelSerializer[Language]):
    names = LanguageNameSerializer(many=True, read_only=True, source="languagename_language")

    class Meta:
        model = Language
        fields = ("id", "name", "official", "iso639", "iso3166", "names")


########################################
#  LOCATION AND ENCOUNTER SERIALIZERS  #
########################################


class EncounterConditionNameSerializer(serializers.ModelSerializer[EncounterConditionName]):
    language = LanguageSummarySerializer()

    class Meta:
        model = EncounterConditionName
        fields = ("name", "language")


class EncounterConditionDetailSerializer(serializers.ModelSerializer[EncounterCondition]):
    names = EncounterConditionNameSerializer(many=True, read_only=True, source="encounterconditionname")
    values = EncounterConditionValueSummarySerializer(many=True, read_only=True, source="encounterconditionvalue")

    class Meta:
        model = EncounterCondition
        fields = ("id", "name", "values", "names")


class EncounterConditionValueNameSerializer(serializers.ModelSerializer[EncounterConditionValueName]):
    language = LanguageSummarySerializer()

    class Meta:
        model = EncounterConditionValueName
        fields = ("name", "language")


class EncounterConditionValueDetailSerializer(serializers.ModelSerializer[EncounterConditionValue]):
    condition = EncounterConditionSummarySerializer(source="encounter_condition")
    names = EncounterConditionValueNameSerializer(many=True, read_only=True, source="encounterconditionvaluename")

    class Meta:
        model = EncounterConditionValue
        fields = ("id", "name", "condition", "names")


class EncounterMethodNameSerializer(serializers.ModelSerializer[EncounterMethodName]):
    language = LanguageSummarySerializer()

    class Meta:
        model = EncounterMethodName
        fields = ("name", "language")


class EncounterMethodDetailSerializer(serializers.ModelSerializer[EncounterMethod]):
    names = EncounterMethodNameSerializer(many=True, read_only=True, source="encountermethodname")

    class Meta:
        model = EncounterMethod
        fields = ("id", "name", "order", "names")


class EncounterSlotSerializer(serializers.ModelSerializer[EncounterSlot]):
    encounter_method = EncounterMethodSummarySerializer()
    chance = serializers.IntegerField(source="rarity")

    class Meta:
        model = EncounterSlot
        fields = ("id", "slot", "chance", "encounter_method", "version_group")


class EncounterPokemonDetailSerializer(serializers.ModelSerializer[EncounterPokemonDetail]):
    class Meta:
        model = EncounterPokemonDetail
        fields = (
            "min_perfect_ivs",
            "always_shiny",
            "never_shiny",
            "is_alpha",
        )


class EncounterDetailSerializer(serializers.ModelSerializer[Encounter]):
    version = VersionSummarySerializer()
    location_area = LocationAreaSummarySerializer()
    pokemon = PokemonSummarySerializer()
    condition_values = serializers.SerializerMethodField("get_encounter_conditions")
    pokemon_details = serializers.SerializerMethodField("get_encounter_pokemon_details")

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
            "pokemon_details",
        )

    @extend_schema_field(EncounterConditionValueSummarySerializer(many=True))
    def get_encounter_conditions(self, obj: Encounter) -> list[dict[str, Any]]:
        condition_values = EncounterConditionValueMap.objects.filter(encounter=obj)
        data = cast(
            "ReturnList[ReturnDict[str, Any]]",
            EncounterConditionValueMapSerializer(condition_values, many=True, context=self.context).data,
        )
        return [item["condition_value"] for item in data]

    @extend_schema_field(EncounterPokemonDetailSerializer(allow_null=True))
    def get_encounter_pokemon_details(self, obj: Encounter) -> ReturnDict[str, Any] | None:
        encounter_pokemon_details = EncounterPokemonDetail.objects.filter(encounter=obj).first()
        return cast(
            "ReturnDict[str, Any] | None",
            EncounterPokemonDetailSerializer(encounter_pokemon_details, context=self.context).data
            if encounter_pokemon_details
            else None,
        )


class LocationAreaNameSerializer(serializers.ModelSerializer[LocationAreaName]):
    language = LanguageSummarySerializer()

    class Meta:
        model = LocationAreaName
        fields = ("name", "language")


class LocationAreaEncounterVersionDetailSerializer(serializers.Serializer[Any]):
    rate = serializers.IntegerField()
    version = VersionSummarySerializer()


class LocationAreaEncounterRateSerializer(serializers.Serializer[Any]):
    encounter_method = EncounterMethodSummarySerializer()
    version_details = LocationAreaEncounterVersionDetailSerializer(many=True)


class LocationAreaEncounterDetailSerializer(serializers.Serializer[Any]):
    min_level = serializers.IntegerField()
    max_level = serializers.IntegerField()
    chance = serializers.IntegerField(source="encounter_slot.rarity", default=0)
    method = EncounterMethodSummarySerializer(source="encounter_slot.encounter_method", default=None)
    condition_values = serializers.SerializerMethodField("get_encounter_conditions")
    pokemon_details = serializers.SerializerMethodField("get_encounter_pokemon_details")

    @extend_schema_field(EncounterConditionValueSummarySerializer(many=True))
    def get_encounter_conditions(self, obj: Encounter) -> list[ReturnDict[str, Any]]:
        condition_maps = cast("EncounterWithRelations", obj).encounterconditionvaluemap_set.all()
        return [
            cast(
                "ReturnDict[str, Any]",
                EncounterConditionValueSummarySerializer(cv.encounter_condition_value, context=self.context).data,
            )
            for cv in condition_maps
        ]

    @extend_schema_field(EncounterPokemonDetailSerializer(allow_null=True))
    def get_encounter_pokemon_details(self, obj: Encounter) -> ReturnDict[str, Any] | None:
        details_list = list(cast("EncounterWithRelations", obj).encounterpokemondetail_set.all())
        details = details_list[0] if details_list else None
        return cast(
            "ReturnDict[str, Any] | None",
            EncounterPokemonDetailSerializer(details, context=self.context).data if details else None,
        )


class LocationAreaPokemonEncounterVersionSerializer(serializers.Serializer[Any]):
    version = VersionSummarySerializer()
    max_chance = serializers.IntegerField()
    encounter_details = LocationAreaEncounterDetailSerializer(many=True)


class LocationAreaPokemonEncounterSerializer(serializers.Serializer[Any]):
    pokemon = PokemonSummarySerializer()
    version_details = LocationAreaPokemonEncounterVersionSerializer(many=True)


class LocationAreaDetailSerializer(serializers.ModelSerializer[LocationArea]):
    location = LocationSummarySerializer()
    encounter_method_rates = serializers.SerializerMethodField("get_method_rates")
    pokemon_encounters = serializers.SerializerMethodField("get_encounters")
    names = LocationAreaNameSerializer(many=True, read_only=True, source="locationareaname")

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

    @extend_schema_field(LocationAreaEncounterRateSerializer(many=True))
    def get_method_rates(self, obj: LocationAreaEncounterRate) -> ReturnList[ReturnDict[str, Any]]:
        # Get encounters related to this area and pull out unique encounter methods
        rates = (
            LocationAreaEncounterRate.objects.filter(location_area=obj, encounter_method__isnull=False)
            .select_related("encounter_method", "version")
            .order_by("encounter_method_id")
        )
        grouped_rates: list[dict[str, Any]] = [
            {
                "encounter_method": method,
                "version_details": list(group_rates),
            }
            for method, group_rates in itertools.groupby(rates, key=lambda r: r.encounter_method)
        ]
        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            LocationAreaEncounterRateSerializer(grouped_rates, many=True, context=self.context).data,
        )

    @extend_schema_field(LocationAreaPokemonEncounterSerializer(many=True))
    def get_encounters(self, obj: LocationArea) -> ReturnList[ReturnDict[str, Any]]:
        encounters = (
            Encounter.objects.filter(location_area=obj)
            .select_related(
                "pokemon",
                "version",
                "encounter_slot",
                "encounter_slot__encounter_method",
            )
            .prefetch_related(
                "encounterconditionvaluemap_set",
                "encounterpokemondetail_set",
            )
            .order_by("pokemon_id", "version_id")
        )

        grouped_data: list[dict[str, Any]] = []
        for pokemon, poke_group in itertools.groupby(encounters, key=lambda e: e.pokemon):
            version_details = []

            for version, ver_group in itertools.groupby(poke_group, key=lambda e: e.version):
                encounter_list = list(ver_group)
                max_chance = sum(e.encounter_slot.rarity for e in encounter_list if e.encounter_slot)
                version_details.append(
                    {
                        "version": version,
                        "max_chance": max_chance,
                        "encounter_details": encounter_list,
                    }
                )

            grouped_data.append(
                {
                    "pokemon": pokemon,
                    "version_details": version_details,
                }
            )

        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            LocationAreaPokemonEncounterSerializer(grouped_data, many=True, context=self.context).data,
        )


class LocationGameIndexSerializer(serializers.ModelSerializer[LocationGameIndex]):
    generation = GenerationSummarySerializer()

    class Meta:
        model = LocationGameIndex
        fields = ("game_index", "generation")


class LocationNameSerializer(serializers.ModelSerializer[LocationName]):
    language = LanguageSummarySerializer()

    class Meta:
        model = LocationName
        fields = ("name", "language")


class LocationDetailSerializer(serializers.ModelSerializer[Location]):
    region = RegionSummarySerializer()
    names = LocationNameSerializer(many=True, read_only=True, source="locationname")
    game_indices = LocationGameIndexSerializer(many=True, read_only=True, source="locationgameindex")
    areas = LocationAreaSummarySerializer(many=True, read_only=True, source="locationarea")

    class Meta:
        model = Location
        fields = ("id", "name", "region", "names", "game_indices", "areas")


#########################
#  ABILITY SERIALIZERS  #
#########################


class AbilityEffectTextSerializer(serializers.ModelSerializer[AbilityEffectText]):
    language = LanguageSummarySerializer()

    class Meta:
        model = AbilityEffectText
        fields = ("effect", "short_effect", "language")


class AbilityFlavorTextSerializer(serializers.ModelSerializer[AbilityFlavorText]):
    flavor_text = serializers.CharField()
    language = LanguageSummarySerializer()
    version_group = VersionGroupSummarySerializer()

    class Meta:
        model = AbilityFlavorText
        fields = ("flavor_text", "language", "version_group")


class AbilityChangeEffectTextSerializer(serializers.ModelSerializer[AbilityChangeEffectText]):
    language = LanguageSummarySerializer()

    class Meta:
        model = AbilityChangeEffectText
        fields = (
            "effect",
            "language",
        )


class AbilityChangeSerializer(serializers.ModelSerializer[AbilityChange]):
    version_group = VersionGroupSummarySerializer()
    effect_entries = AbilityChangeEffectTextSerializer(many=True, read_only=True, source="abilitychangeeffecttext")

    class Meta:
        model = AbilityChange
        fields = ("version_group", "effect_entries")


class AbilityNameSerializer(serializers.ModelSerializer[AbilityName]):
    language = LanguageSummarySerializer()

    class Meta:
        model = AbilityName
        fields = ("name", "language")


class AbilityPokemonDetailSerializer(serializers.ModelSerializer[PokemonAbility]):
    pokemon = PokemonSummarySerializer()

    class Meta:
        model = PokemonAbility
        fields = ("is_hidden", "slot", "pokemon")


class AbilityDetailSerializer(serializers.ModelSerializer[Ability]):
    effect_entries = AbilityEffectTextSerializer(many=True, read_only=True, source="abilityeffecttext")
    flavor_text_entries = AbilityFlavorTextSerializer(many=True, read_only=True, source="abilityflavortext")
    names = AbilityNameSerializer(many=True, read_only=True, source="abilityname")
    generation = GenerationSummarySerializer()
    effect_changes = AbilityChangeSerializer(many=True, read_only=True, source="abilitychange")
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

    @extend_schema_field(AbilityPokemonDetailSerializer(many=True))
    def get_ability_pokemon(self, obj: Ability) -> ReturnList[ReturnDict[str, Any]]:
        pokemon_ability_objects = PokemonAbility.objects.filter(ability=obj).select_related("pokemon")
        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            AbilityPokemonDetailSerializer(pokemon_ability_objects, many=True, context=self.context).data,
        )


######################
#  STAT SERIALIZERS  #
######################


class StatNameSerializer(serializers.ModelSerializer[StatName]):
    language = LanguageSummarySerializer()

    class Meta:
        model = StatName
        fields = ("name", "language")


class MoveStatChangeSerializer(serializers.ModelSerializer[MoveMetaStatChange]):
    move = MoveSummarySerializer()

    class Meta:
        model = MoveMetaStatChange
        fields = ("change", "move")


class StatAffectingMovesSerializer(serializers.Serializer[Any]):
    increase = MoveStatChangeSerializer(many=True)
    decrease = MoveStatChangeSerializer(many=True)


class StatAffectingNaturesSerializer(serializers.Serializer[Any]):
    increase = NatureSummarySerializer(many=True)
    decrease = NatureSummarySerializer(many=True)


class StatDetailSerializer(serializers.ModelSerializer[Stat]):
    names = StatNameSerializer(many=True, read_only=True, source="statname")
    move_damage_class = MoveDamageClassSummarySerializer()
    characteristics = CharacteristicSummarySerializer(many=True, read_only=True, source="characteristic")
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

    @extend_schema_field(StatAffectingMovesSerializer)
    def get_moves_that_affect(self, obj: Stat) -> ReturnDict[str, Any]:
        stat_change_objects = MoveMetaStatChange.objects.filter(stat=obj).select_related("move")
        increases = stat_change_objects.filter(change__gt=0)
        decreases = stat_change_objects.filter(change__lte=0)

        return cast(
            "ReturnDict[str, Any]",
            StatAffectingMovesSerializer({"increase": increases, "decrease": decreases}, context=self.context).data,
        )

    @extend_schema_field(StatAffectingNaturesSerializer)
    def get_natures_that_affect(self, obj: Stat) -> ReturnDict[str, Any]:
        increases = Nature.objects.filter(increased_stat=obj)
        decreases = Nature.objects.filter(decreased_stat=obj)

        return cast(
            "ReturnDict[str, Any]",
            StatAffectingNaturesSerializer({"increase": increases, "decrease": decreases}, context=self.context).data,
        )

    @extend_schema_field(ItemSummarySerializer(many=True))
    def get_items_that_affect(self, obj: Stat) -> ReturnList[ReturnDict[str, Any]]:
        """
        Get items that affect this stat (like vitamins, X-items, etc.)
        """
        # Map stat names to their corresponding vitamin and X-item names
        stat_item_mapping = {
            "hp": ["hp-up"],
            "attack": ["protein", "x-attack"],
            "defense": ["iron", "x-defense"],
            "special-attack": ["calcium", "x-sp-atk"],
            "special-defense": ["zinc", "x-sp-def"],
            "speed": ["carbos", "x-speed"],
            "accuracy": ["x-accuracy"],
            "evasion": ["x-evasion"],
        }

        # Get the stat name (lowercase)
        stat_name = obj.name.lower()
        # Get the corresponding item names for this stat
        item_names = stat_item_mapping.get(stat_name, [])

        if not item_names:
            return cast("ReturnList[ReturnDict[str, Any]]", [])

        items = Item.objects.filter(name__in=item_names)
        return cast(
            "ReturnList[ReturnDict[str, Any]]", ItemSummarySerializer(items, many=True, context=self.context).data
        )


#############################
#  ITEM POCKET SERIALIZERS  #
#############################


class ItemPocketNameSerializer(serializers.ModelSerializer[ItemPocketName]):
    language = LanguageSummarySerializer()

    class Meta:
        model = ItemPocketName
        fields = ("name", "language")


class ItemPocketDetailSerializer(serializers.ModelSerializer[ItemPocket]):
    names = ItemPocketNameSerializer(many=True, read_only=True, source="itempocketname")
    categories = ItemCategorySummarySerializer(many=True, read_only=True, source="itemcategory")

    class Meta:
        model = ItemPocket
        fields = ("id", "name", "categories", "categories", "names")


###############################
#  ITEM CATEGORY SERIALIZERS  #
###############################


class ItemCategoryNameSerializer(serializers.ModelSerializer[ItemCategoryName]):
    language = LanguageSummarySerializer()

    class Meta:
        model = ItemCategoryName
        fields = ("name", "language")


class ItemCategoryDetailSerializer(serializers.ModelSerializer[ItemCategory]):
    names = ItemCategoryNameSerializer(many=True, read_only=True, source="itemcategoryname")
    pocket = ItemPocketSummarySerializer(source="item_pocket")
    items = ItemSummarySerializer(many=True, read_only=True, source="item")

    class Meta:
        model = ItemCategory
        fields = ("id", "name", "items", "names", "pocket")


################################
#  ITEM ATTRIBUTE SERIALIZERS  #
################################


class ItemAttributeNameSerializer(serializers.ModelSerializer[ItemAttributeName]):
    language = LanguageSummarySerializer()

    class Meta:
        model = ItemAttributeName
        fields = ("name", "language")


class ItemAttributeDescriptionSerializer(serializers.ModelSerializer[ItemAttributeDescription]):
    language = LanguageSummarySerializer()

    class Meta:
        model = ItemAttributeDescription
        fields = ("description", "language")


class ItemAttributeDetailSerializer(serializers.ModelSerializer[ItemAttribute]):
    names = ItemAttributeNameSerializer(many=True, read_only=True, source="itemattributename")
    descriptions = ItemAttributeDescriptionSerializer(many=True, read_only=True, source="itemattributedescription")
    items = serializers.SerializerMethodField("get_attribute_items")

    class Meta:
        model = ItemAttribute
        fields = ("id", "name", "descriptions", "items", "names")

    @extend_schema_field(ItemSummarySerializer(many=True))
    def get_attribute_items(self, obj: ItemAttribute) -> ReturnList[ReturnDict[str, Any]]:
        items = Item.objects.filter(itemattributemap__item_attribute=obj, itemattributemap__item__isnull=False)
        return cast(
            "ReturnList[ReturnDict[str, Any]]", ItemSummarySerializer(items, many=True, context=self.context).data
        )


###########################
#  CURRENCY SERIALIZERS  #
###########################


class CurrencyNameSerializer(serializers.ModelSerializer[CurrencyName]):
    language = LanguageSummarySerializer()

    class Meta:
        model = CurrencyName
        fields = ("name", "language")


class CurrencyDetailSerializer(serializers.ModelSerializer[Currency]):
    names = CurrencyNameSerializer(many=True, read_only=True, source="currencyname")

    class Meta:
        model = Currency
        fields = ("id", "name", "names")


###################################
#  ITEM FLING EFFECT SERIALIZERS  #
###################################


class ItemFlingEffectEffectTextSerializer(serializers.ModelSerializer[ItemFlingEffectEffectText]):
    language = LanguageSummarySerializer()

    class Meta:
        model = ItemFlingEffectEffectText
        fields = ("effect", "language")


class ItemFlingEffectDetailSerializer(serializers.ModelSerializer[ItemFlingEffect]):
    effect_entries = ItemFlingEffectEffectTextSerializer(many=True, read_only=True, source="itemflingeffecteffecttext")
    items = ItemSummarySerializer(many=True, read_only=True, source="item")

    class Meta:
        model = ItemFlingEffect
        fields = ("id", "name", "effect_entries", "items")


#######################
#  ITEM  SERIALIZERS  #
#######################


class ItemFlavorTextSerializer(serializers.ModelSerializer[ItemFlavorText]):
    text = serializers.CharField(source="flavor_text")
    language = LanguageSummarySerializer()
    version_group = VersionGroupSummarySerializer()

    class Meta:
        model = ItemFlavorText
        fields = ("text", "version_group", "language")


class ItemEffectTextSerializer(serializers.ModelSerializer[ItemEffectText]):
    language = LanguageSummarySerializer()

    class Meta:
        model = ItemEffectText
        fields = ("effect", "short_effect", "language")


class ItemGameIndexSerializer(serializers.ModelSerializer[ItemGameIndex]):
    generation = GenerationSummarySerializer()

    class Meta:
        model = ItemGameIndex
        fields = ("game_index", "generation")


class ItemPriceSerializer(serializers.ModelSerializer[ItemPrice]):
    currency = CurrencySummarySerializer()
    version_group = VersionGroupSummarySerializer()

    class Meta:
        model = ItemPrice
        fields = (
            "purchase_price",
            "sell_price",
            "currency",
            "version_group",
        )


class ItemNameSerializer(serializers.ModelSerializer[ItemName]):
    language = LanguageSummarySerializer()

    class Meta:
        model = ItemName
        fields = ("name", "language")


class ItemSpritesSerializer(serializers.Serializer[Any]):
    default = serializers.CharField(allow_null=True)


class PokemonHeldItemVersionSerializer(serializers.Serializer[Any]):
    rarity = serializers.IntegerField()
    version = VersionSummarySerializer()


class PokemonHeldItemSerializer(serializers.Serializer[Any]):
    pokemon = PokemonSummarySerializer()
    version_details = PokemonHeldItemVersionSerializer(many=True)


class ItemMachineSerializer(serializers.ModelSerializer[Machine]):
    machine = MachineSummarySerializer(source="*")
    version_group = VersionGroupSummarySerializer()

    class Meta:
        model = Machine
        fields = ("machine", "version_group")


class ItemDetailSerializer(serializers.ModelSerializer[Item]):
    names = ItemNameSerializer(many=True, read_only=True, source="itemname")
    game_indices = ItemGameIndexSerializer(many=True, read_only=True, source="itemgameindex")
    prices = ItemPriceSerializer(many=True, read_only=True, source="itemprice")
    effect_entries = ItemEffectTextSerializer(many=True, read_only=True, source="itemeffecttext")
    flavor_text_entries = ItemFlavorTextSerializer(many=True, read_only=True, source="itemflavortext")
    category = ItemCategorySummarySerializer(source="item_category")
    attributes = serializers.SerializerMethodField("get_item_attributes")
    fling_effect = ItemFlingEffectSummarySerializer(source="item_fling_effect")
    held_by_pokemon = serializers.SerializerMethodField("get_held_by_pokemon")
    baby_trigger_for = serializers.SerializerMethodField("get_baby_trigger_for")
    sprites = serializers.SerializerMethodField("get_item_sprites")
    machines = serializers.SerializerMethodField("get_item_machines")

    class Meta:
        model = Item
        fields = (
            "id",
            "name",
            "fling_power",
            "fling_effect",
            "attributes",
            "category",
            "effect_entries",
            "flavor_text_entries",
            "game_indices",
            "prices",
            "names",
            "held_by_pokemon",
            "sprites",
            "baby_trigger_for",
            "machines",
        )

    @extend_schema_field(ItemMachineSerializer(many=True))
    def get_item_machines(self, obj: Item) -> list[ReturnDict[str, Any]]:
        machine_objects = Machine.objects.filter(item=obj).select_related("version_group")
        return cast(
            "list[ReturnDict[str, Any]]",
            ItemMachineSerializer(machine_objects, many=True, context=self.context).data,
        )

    @extend_schema_field(ItemSpritesSerializer)
    def get_item_sprites(self, obj: Item) -> dict[str, str | None]:
        sprites_object = ItemSprites.objects.filter(item=obj).first()
        return sprites_object.sprites if sprites_object else {}

    @extend_schema_field(ItemAttributeSummarySerializer(many=True))
    def get_item_attributes(self, obj: Item) -> ReturnList[ReturnDict[str, Any]]:
        attributes = ItemAttribute.objects.filter(itemattributemap__item=obj)
        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            ItemAttributeSummarySerializer(attributes, many=True, context=self.context).data,
        )

    @extend_schema_field(PokemonHeldItemSerializer(many=True))
    def get_held_by_pokemon(self, obj: Item) -> ReturnList[ReturnDict[str, Any]]:
        pokemon_items = (
            PokemonItem.objects.filter(item=obj)
            .select_related("pokemon", "version")
            .order_by("pokemon_id", "version_id")
        )
        grouped_data: list[dict[str, Any]] = [
            {
                "pokemon": pokemon,
                "version_details": list(items),
            }
            for pokemon, items in itertools.groupby(pokemon_items, key=lambda pi: pi.pokemon)
        ]
        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            PokemonHeldItemSerializer(grouped_data, many=True, context=self.context).data,
        )

    @extend_schema_field(EvolutionChainSummarySerializer(allow_null=True))
    def get_baby_trigger_for(self, obj: Item) -> ReturnDict[str, Any] | None:
        chain_object = EvolutionChain.objects.filter(baby_trigger_item=obj).first()
        return cast(
            "ReturnDict[str, Any] | None",
            EvolutionChainSummarySerializer(chain_object, context=self.context).data if chain_object else None,
        )


########################
#  NATURE SERIALIZERS  #
########################


class NatureBattleStylePreferenceSerializer(serializers.ModelSerializer[NatureBattleStylePreference]):
    move_battle_style = MoveBattleStyleSummarySerializer()

    class Meta:
        model = NatureBattleStylePreference
        fields = (
            "low_hp_preference",
            "high_hp_preference",
            "move_battle_style",
        )


class NatureNameSerializer(serializers.ModelSerializer[NatureName]):
    language = LanguageSummarySerializer()

    class Meta:
        model = NatureName
        fields = ("name", "language")


class NaturePokeathlonStatSerializer(serializers.ModelSerializer[NaturePokeathlonStat]):
    pokeathlon_stat = PokeathlonStatSummarySerializer()

    class Meta:
        model = NaturePokeathlonStat
        fields = ("max_change", "pokeathlon_stat")


class NatureDetailSerializer(serializers.ModelSerializer[Nature]):
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

    @extend_schema_field(NaturePokeathlonStatSerializer(many=True))
    def get_pokeathlon_stats(self, obj: Nature) -> ReturnList[ReturnDict[str, Any]]:
        pokeathlon_stat_objects = NaturePokeathlonStat.objects.filter(nature=obj).select_related("pokeathlon_stat")
        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            NaturePokeathlonStatSerializer(pokeathlon_stat_objects, many=True, context=self.context).data,
        )


#######################
#  BERRY SERIALIZERS  #
#######################


class BerryFirmnessNameSerializer(serializers.ModelSerializer[BerryFirmnessName]):
    language = LanguageSummarySerializer()

    class Meta:
        model = BerryFirmnessName
        fields = ("name", "language")


class BerryFirmnessDetailSerializer(serializers.ModelSerializer[BerryFirmness]):
    names = BerryFirmnessNameSerializer(many=True, read_only=True, source="berryfirmnessname")
    berries = BerrySummarySerializer(many=True, read_only=True, source="berry")

    class Meta:
        model = BerryFirmness
        fields = ("id", "name", "berries", "names")


class BerryFlavorNameSerializer(serializers.ModelSerializer[BerryFlavorName]):
    language = LanguageSummarySerializer()

    class Meta:
        model = BerryFlavorName
        fields = ("name", "language")


class BerryFlavorBerryMapSerializer(serializers.ModelSerializer[BerryFlavorMap]):
    berry = BerrySummarySerializer()

    class Meta:
        model = BerryFlavorMap
        fields = ("potency", "berry")


class BerryFlavorDetailSerializer(serializers.ModelSerializer[BerryFlavor]):
    names = BerryFlavorNameSerializer(many=True, read_only=True, source="berryflavorname")
    contest_type = ContestTypeSummarySerializer()
    berries = serializers.SerializerMethodField("get_berries_with_flavor")

    class Meta:
        model = BerryFlavor
        fields = ("id", "name", "berries", "contest_type", "names")

    @extend_schema_field(BerryFlavorBerryMapSerializer(many=True))
    def get_berries_with_flavor(self, obj: BerryFlavor) -> ReturnList[ReturnDict[str, Any]]:
        flavor_map_objects = (
            BerryFlavorMap.objects.filter(berry_flavor=obj, potency__gt=0).select_related("berry").order_by("potency")
        )
        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            BerryFlavorBerryMapSerializer(flavor_map_objects, many=True, context=self.context).data,
        )


class BerryFlavorMapSerializer(serializers.ModelSerializer[BerryFlavorMap]):
    flavor = BerryFlavorSummarySerializer(source="berry_flavor")

    class Meta:
        model = BerryFlavorMap
        fields = ("potency", "flavor")


class BerryDetailSerializer(serializers.ModelSerializer[Berry]):
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

    @extend_schema_field(BerryFlavorMapSerializer(many=True))
    def get_berry_flavors(self, obj: Berry) -> ReturnList[ReturnDict[str, Any]]:
        flavor_map_objects = BerryFlavorMap.objects.filter(berry=obj).select_related("berry_flavor")
        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            BerryFlavorMapSerializer(flavor_map_objects, many=True, context=self.context).data,
        )


###########################
#  EGG GROUP SERIALIZERS  #
###########################


class EggGroupNameSerializer(serializers.ModelSerializer[EggGroupName]):
    language = LanguageSummarySerializer()

    class Meta:
        model = EggGroupName
        fields = ("name", "language")


class EggGroupDetailSerializer(serializers.ModelSerializer[EggGroup]):
    names = EggGroupNameSerializer(many=True, read_only=True, source="egggroupname")
    pokemon_species = serializers.SerializerMethodField("get_species")

    class Meta:
        model = EggGroup
        fields = ("id", "name", "names", "pokemon_species")

    @extend_schema_field(PokemonSpeciesSummarySerializer(many=True))
    def get_species(self, obj: EggGroup) -> ReturnList[ReturnDict[str, Any]]:
        species = PokemonSpecies.objects.filter(pokemonegggroup__egg_group=obj)
        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            PokemonSpeciesSummarySerializer(species, many=True, context=self.context).data,
        )


######################
#  TYPE SERIALIZERS  #
######################


class TypeEfficacyPastSerializer(serializers.ModelSerializer[TypeEfficacyPast]):
    generation = GenerationSummarySerializer()

    class Meta:
        model = TypeEfficacyPast
        fields = ("target_type", "damage_type", "damage_factor", "generation")


class TypeGameIndexSerializer(serializers.ModelSerializer[TypeGameIndex]):
    generation = GenerationSummarySerializer()

    class Meta:
        model = TypeGameIndex
        fields = ("game_index", "generation")


class TypeNameSerializer(serializers.ModelSerializer[TypeName]):
    language = LanguageSummarySerializer()

    class Meta:
        model = TypeName
        fields = ("name", "language")


class TypeSpriteSerializer(serializers.ModelSerializer[TypeSprites]):
    class Meta:
        model = TypeSprites
        fields = ("sprites",)


class TypeRelationshipsSerializer(serializers.Serializer[Any]):
    no_damage_to = TypeSummarySerializer(many=True)
    half_damage_to = TypeSummarySerializer(many=True)
    double_damage_to = TypeSummarySerializer(many=True)
    no_damage_from = TypeSummarySerializer(many=True)
    half_damage_from = TypeSummarySerializer(many=True)
    double_damage_from = TypeSummarySerializer(many=True)


class TypePastRelationshipsSerializer(serializers.Serializer[Any]):
    generation = GenerationSummarySerializer()
    damage_relations = TypeRelationshipsSerializer()


class TypePokemonSerializer(serializers.ModelSerializer[PokemonType]):
    pokemon = PokemonSummarySerializer()

    class Meta:
        model = PokemonType
        fields = ("slot", "pokemon")


class TypeDetailSerializer(serializers.ModelSerializer[Type]):
    """
    Serializer for the Type resource
    """

    generation = GenerationSummarySerializer()
    names = TypeNameSerializer(many=True, read_only=True, source="typename")
    game_indices = TypeGameIndexSerializer(many=True, read_only=True, source="typegameindex")
    move_damage_class = MoveDamageClassSummarySerializer()
    damage_relations = serializers.SerializerMethodField("get_type_relationships")
    past_damage_relations = serializers.SerializerMethodField("get_type_past_relationships")
    pokemon = serializers.SerializerMethodField("get_type_pokemon")
    moves = MoveSummarySerializer(many=True, read_only=True, source="move")
    sprites = serializers.SerializerMethodField("get_type_sprites")

    FACTOR_PREFIX_MAP: ClassVar[dict[int, str]] = {200: "double", 50: "half", 0: "no"}
    RELATION_KEYS = (
        "no_damage_to",
        "half_damage_to",
        "double_damage_to",
        "no_damage_from",
        "half_damage_from",
        "double_damage_from",
    )

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

    @extend_schema_field(TypeSpriteSerializer)
    def get_type_sprites(self, obj: Type) -> dict[str, str | None]:
        sprites_object = TypeSprites.objects.filter(type=obj).first()
        return sprites_object.sprites if sprites_object else {}

    def add_type_entry(
        self, relations: dict[str, list[Any]], type_obj: Type, damage_factor: int, direction: str = "_damage_to"
    ) -> None:
        """
        Add an entry for the given type with the given damage factor in the given direction to the set of relations.
        """
        if prefix := self.FACTOR_PREFIX_MAP.get(damage_factor):
            type_data = cast("ReturnDict[str, Any]", TypeSummarySerializer(type_obj, context=self.context).data)
            relations[f"{prefix}{direction}"].append(type_data)

    @extend_schema_field(TypeRelationshipsSerializer)
    def get_type_relationships(self, obj: Type) -> dict[str, list[dict[str, Any]]]:
        relations: dict[str, list[dict[str, Any]]] = {key: [] for key in self.RELATION_KEYS}

        # Damage To
        damage_to_efficacy = TypeEfficacy.objects.filter(damage_type=obj).select_related("target_type")
        for efficacy in damage_to_efficacy:
            if efficacy.target_type:
                self.add_type_entry(relations, efficacy.target_type, efficacy.damage_factor, direction="_damage_to")

        # Damage From
        damage_from_efficacy = TypeEfficacy.objects.filter(target_type=obj).select_related("damage_type")
        for efficacy in damage_from_efficacy:
            if efficacy.damage_type:
                self.add_type_entry(relations, efficacy.damage_type, efficacy.damage_factor, direction="_damage_from")

        return relations

    def remove_type_entry(self, relations: dict[str, list[Any]], type_obj: Type, direction: str = "_damage_to") -> None:
        """
        Remove the entry for the given type in the given direction from the set of relations.
        """
        for prefix in ("double", "half", "no"):
            rel_list = relations[f"{prefix}{direction}"]
            for i, item in enumerate(rel_list):
                if item["name"] == type_obj.name:
                    del rel_list[i]
                    return

    @extend_schema_field(TypePastRelationshipsSerializer(many=True))
    def get_type_past_relationships(self, obj: Type) -> list[dict[str, Any]]:
        """Returns a list of past type relationships for the given type object, grouped by generation."""
        # collect data from DB
        all_past_efficacy = list(
            TypeEfficacyPast.objects.filter(Q(damage_type=obj) | Q(target_type=obj)).select_related(
                "generation", "target_type", "damage_type"
            )
        )
        if not all_past_efficacy:
            return []

        serializer_data = cast(
            "ReturnList[ReturnDict[str, Any]]",
            TypeEfficacyPastSerializer(all_past_efficacy, many=True, context=self.context).data,
        )

        # group data by generation
        data_by_gen = [
            list(group) for _, group in itertools.groupby(serializer_data, key=lambda r: r["generation"]["name"])
        ]
        all_types = Type.objects.select_related("generation").all()
        type_cache = {t.pk: t for t in all_types}
        name_to_gen_pk = {t.name: t.generation.pk if t.generation else 0 for t in all_types}

        # process each generation's data in turn
        final_data: list[dict[str, Any]] = []
        for gen_data in data_by_gen:
            current_gen_name = gen_data[0]["generation"]["name"]
            current_gen = Generation.objects.filter(name=current_gen_name).first()
            # create past relations object for this generation
            past_relations: dict[str, Any] = {
                "generation": gen_data[0]["generation"],
                "damage_relations": self.get_type_relationships(obj),
            }
            relations = past_relations["damage_relations"]

            # remove types not yet introduced
            # e.g. Poison has no effect on Steel, but Steel was not present in generation I
            # so it should be absent from the list
            if current_gen:
                for key in self.RELATION_KEYS:
                    relations[key] = [
                        item for item in relations[key] if name_to_gen_pk.get(item["name"], 0) <= current_gen.pk
                    ]

            # populate offensive relations
            for relation in (r for r in gen_data if r["damage_type"] == obj.pk):
                if target_type_obj := type_cache.get(relation["target_type"]):
                    self.remove_type_entry(relations, target_type_obj, direction="_damage_to")
                    self.add_type_entry(relations, target_type_obj, relation["damage_factor"], direction="_damage_to")
            # populate defensive relations
            for relation in (r for r in gen_data if r["target_type"] == obj.pk):
                if damage_type_obj := type_cache.get(relation["damage_type"]):
                    self.remove_type_entry(relations, damage_type_obj, direction="_damage_from")
                    self.add_type_entry(relations, damage_type_obj, relation["damage_factor"], direction="_damage_from")

            final_data.append(past_relations)

        return final_data

    @extend_schema_field(TypePokemonSerializer(many=True))
    def get_type_pokemon(self, obj: Type) -> ReturnList[ReturnDict[str, Any]]:
        poke_type_objects = PokemonType.objects.filter(type=obj).select_related("pokemon")
        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            TypePokemonSerializer(poke_type_objects, many=True, context=self.context).data,
        )


#########################
#  MACHINE SERIALIZERS  #
#########################


class MachineDetailSerializer(serializers.ModelSerializer[Machine]):
    item = ItemSummarySerializer()
    version_group = VersionGroupSummarySerializer()
    move = MoveSummarySerializer()

    class Meta:
        model = Machine
        fields = ("id", "item", "version_group", "move")


###################################
#  MOVE BATTLE STYLE SERIALIZERS  #
###################################


class MoveBattleStyleNameSerializer(serializers.ModelSerializer[MoveBattleStyleName]):
    language = LanguageSummarySerializer()

    class Meta:
        model = MoveBattleStyleName
        fields = ("name", "language")


class MoveBattleStyleDetailSerializer(serializers.ModelSerializer[MoveBattleStyle]):
    names = MoveBattleStyleNameSerializer(many=True, read_only=True, source="movebattlestylename")

    class Meta:
        model = MoveBattleStyle
        fields = ("id", "name", "names")


###################################
#  MOVE DAMAGE CLASS SERIALIZERS  #
###################################


class MoveDamageClassNameSerializer(serializers.ModelSerializer[MoveDamageClassName]):
    language = LanguageSummarySerializer()

    class Meta:
        model = MoveDamageClassName
        fields = ("name", "language")


class MoveDamageClassDescriptionSerializer(serializers.ModelSerializer[MoveDamageClassDescription]):
    language = LanguageSummarySerializer()

    class Meta:
        model = MoveDamageClassDescription
        fields = ("description", "language")


class MoveDamageClassDetailSerializer(serializers.ModelSerializer[MoveDamageClass]):
    names = MoveDamageClassNameSerializer(many=True, read_only=True, source="movedamageclassname")
    descriptions = MoveDamageClassDescriptionSerializer(many=True, read_only=True, source="movedamageclassdescription")
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


class MoveMetaAilmentNameSerializer(serializers.ModelSerializer[MoveMetaAilmentName]):
    language = LanguageSummarySerializer()

    class Meta:
        model = MoveMetaAilmentName
        fields = ("name", "language")


class MoveMetaAilmentDetailSerializer(serializers.ModelSerializer[MoveMetaAilment]):
    names = MoveMetaAilmentNameSerializer(many=True, read_only=True, source="movemetaailmentname")
    moves = serializers.SerializerMethodField("get_ailment_moves")

    class Meta:
        model = MoveMetaAilment
        fields = ("id", "name", "moves", "names")

    @extend_schema_field(MoveSummarySerializer(many=True))
    def get_ailment_moves(self, obj: MoveMetaAilment) -> ReturnList[ReturnDict[str, Any]]:
        moves = Move.objects.filter(movemeta__move_meta_ailment=obj)
        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            MoveSummarySerializer(moves, many=True, context=self.context).data,
        )


class MoveMetaCategoryDescriptionSerializer(serializers.ModelSerializer[MoveMetaCategoryDescription]):
    language = LanguageSummarySerializer()

    class Meta:
        model = MoveMetaCategoryDescription
        fields = ("description", "language")


class MoveMetaCategoryDetailSerializer(serializers.ModelSerializer[MoveMetaCategory]):
    descriptions = MoveMetaCategoryDescriptionSerializer(
        many=True, read_only=True, source="movemetacategorydescription"
    )
    moves = serializers.SerializerMethodField("get_category_moves")

    class Meta:
        model = MoveMetaCategory
        fields = ("id", "name", "descriptions", "moves")

    @extend_schema_field(MoveSummarySerializer(many=True))
    def get_category_moves(self, obj: MoveMetaCategory) -> ReturnList[ReturnDict[str, Any]]:
        moves = Move.objects.filter(movemeta__move_meta_category=obj)
        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            MoveSummarySerializer(moves, many=True, context=self.context).data,
        )


class MoveMetaSerializer(serializers.ModelSerializer[MoveMeta]):
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


class MoveTargetNameSerializer(serializers.ModelSerializer[MoveTargetName]):
    language = LanguageSummarySerializer()

    class Meta:
        model = MoveTargetName
        fields = ("name", "language")


class MoveTargetDescriptionSerializer(serializers.ModelSerializer[MoveTargetDescription]):
    language = LanguageSummarySerializer()

    class Meta:
        model = MoveTargetDescription
        fields = ("description", "language")


class MoveTargetDetailSerializer(serializers.ModelSerializer[MoveTarget]):
    names = MoveTargetNameSerializer(many=True, read_only=True, source="movetargetname")
    descriptions = MoveTargetDescriptionSerializer(many=True, read_only=True, source="movetargetdescription")
    moves = MoveSummarySerializer(many=True, read_only=True, source="move")

    class Meta:
        model = MoveTarget
        fields = ("id", "name", "descriptions", "moves", "names")


######################
#  MOVE SERIALIZERS  #
######################


class MoveNameSerializer(serializers.ModelSerializer[MoveName]):
    language = LanguageSummarySerializer()

    class Meta:
        model = MoveName
        fields = ("name", "language")


class MoveEffectEffectTextSerializer(serializers.ModelSerializer[MoveEffectEffectText]):
    language = LanguageSummarySerializer()

    class Meta:
        model = MoveEffectEffectText
        fields = ("effect", "short_effect", "language")


class MoveChangeSerializer(serializers.ModelSerializer[MoveChange]):
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

    @extend_schema_field(MoveEffectEffectTextSerializer(many=True))
    def get_effects(self, obj: MoveChange) -> ReturnList[ReturnDict[str, Any]]:
        effect_texts = MoveEffectEffectText.objects.filter(move_effect=obj.move_effect).select_related("language")
        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            MoveEffectEffectTextSerializer(effect_texts, many=True, context=self.context).data,
        )


class MoveEffectChangeEffectTextSerializer(serializers.ModelSerializer[MoveEffectChangeEffectText]):
    language = LanguageSummarySerializer()

    class Meta:
        model = MoveEffectChangeEffectText
        fields = ("effect", "language")


class MoveEffectChangeSerializer(serializers.ModelSerializer[MoveEffectChange]):
    version_group = VersionGroupSummarySerializer()
    effect_entries = MoveEffectChangeEffectTextSerializer(
        many=True, read_only=True, source="moveeffectchangeeffecttext"
    )

    class Meta:
        model = MoveEffectChange
        fields = ("version_group", "effect_entries")


class MoveFlavorTextSerializer(serializers.ModelSerializer[MoveFlavorText]):
    flavor_text = serializers.CharField()
    language = LanguageSummarySerializer()
    version_group = VersionGroupSummarySerializer()

    class Meta:
        model = MoveFlavorText
        fields = ("flavor_text", "language", "version_group")


class MoveComboUsageSerializer(serializers.Serializer[Any]):
    use_before = MoveSummarySerializer(many=True, allow_null=True)
    use_after = MoveSummarySerializer(many=True, allow_null=True)


class MoveCombosSerializer(serializers.Serializer[Any]):
    normal = MoveComboUsageSerializer()
    super = MoveComboUsageSerializer()


class MoveMetaStatChangeSerializer(serializers.ModelSerializer[MoveMetaStatChange]):
    stat = StatSummarySerializer()

    class Meta:
        model = MoveMetaStatChange
        fields = ("change", "stat")


class MoveDetailSerializer(serializers.ModelSerializer[Move]):
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
    flavor_text_entries = MoveFlavorTextSerializer(many=True, read_only=True, source="moveflavortext")
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

    @extend_schema_field(PokemonSummarySerializer(many=True))
    def get_learned_by_pokemon(self, obj: Move) -> ReturnList[ReturnDict[str, Any]]:
        pokemon = Pokemon.objects.filter(pokemonmove__move=obj).distinct().order_by("id")
        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            PokemonSummarySerializer(pokemon, many=True, context=self.context).data,
        )

    @extend_schema_field(ItemMachineSerializer(many=True))
    def get_move_machines(self, obj: Move) -> ReturnList[ReturnDict[str, Any]]:
        machine_objects = Machine.objects.filter(move=obj).select_related("version_group")
        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            ItemMachineSerializer(machine_objects, many=True, context=self.context).data,
        )

    @extend_schema_field(MoveCombosSerializer(allow_null=True))
    def get_combos(self, obj: Move) -> dict[str, Any] | None:
        normal_before = [
            c.second_move
            for c in ContestCombo.objects.filter(first_move=obj).select_related("second_move")
            if c.second_move
        ]
        normal_after = [
            c.first_move
            for c in ContestCombo.objects.filter(second_move=obj).select_related("first_move")
            if c.first_move
        ]
        super_before = [
            c.second_move
            for c in SuperContestCombo.objects.filter(first_move=obj).select_related("second_move")
            if c.second_move
        ]
        super_after = [
            c.first_move
            for c in SuperContestCombo.objects.filter(second_move=obj).select_related("first_move")
            if c.first_move
        ]

        if not (normal_before or normal_after or super_before or super_after):
            return None

        def serialize_list(moves: list[Any]) -> list[dict[str, Any]] | None:
            if not moves:
                return None
            return cast(
                "list[dict[str, Any]]",
                MoveSummarySerializer(moves, many=True, context=self.context).data,
            )

        return {
            "normal": {
                "use_before": serialize_list(normal_before),
                "use_after": serialize_list(normal_after),
            },
            "super": {
                "use_before": serialize_list(super_before),
                "use_after": serialize_list(super_after),
            },
        }

    @extend_schema_field(MoveEffectEffectTextSerializer(many=True))
    def get_effect_text(self, obj: Move) -> ReturnList[ReturnDict[str, Any]]:
        effect_texts = MoveEffectEffectText.objects.filter(move_effect=obj.move_effect).select_related("language")
        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            MoveEffectEffectTextSerializer(effect_texts, many=True, context=self.context).data,
        )

    @extend_schema_field(MoveEffectChangeSerializer(many=True))
    def get_effect_change_text(self, obj: Move) -> ReturnList[ReturnDict[str, Any]]:
        effect_changes = MoveEffectChange.objects.filter(move_effect=obj.move_effect).select_related("version_group")
        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            MoveEffectChangeSerializer(effect_changes, many=True, context=self.context).data,
        )

    @extend_schema_field(MoveMetaStatChangeSerializer(many=True))
    def get_move_stat_change(self, obj: Move) -> ReturnList[ReturnDict[str, Any]]:
        stat_changes = MoveMetaStatChange.objects.filter(move=obj).select_related("stat")
        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            MoveMetaStatChangeSerializer(stat_changes, many=True, context=self.context).data,
        )


##########################
#  PAL PARK SERIALIZERS  #
##########################


class PalParkAreaNameSerializer(serializers.HyperlinkedModelSerializer[PalParkAreaName]):
    language = LanguageSummarySerializer()

    class Meta:
        model = PalParkAreaName
        fields = ("name", "language")


class PalParkEncounterSerializer(serializers.ModelSerializer[PalPark]):
    pokemon_species = PokemonSpeciesSummarySerializer()

    class Meta:
        model = PalPark
        fields = ("base_score", "rate", "pokemon_species")


class PalParkAreaDetailSerializer(serializers.ModelSerializer[PalParkArea]):
    names = PalParkAreaNameSerializer(many=True, read_only=True, source="palparkareaname")
    pokemon_encounters = serializers.SerializerMethodField("get_encounters")

    class Meta:
        model = PalParkArea
        fields = ("id", "name", "names", "pokemon_encounters")

    @extend_schema_field(PalParkEncounterSerializer(many=True))
    def get_encounters(self, obj: PalParkArea) -> ReturnList[ReturnDict[str, Any]]:
        pal_park_objects = PalPark.objects.filter(pal_park_area=obj).select_related("pokemon_species")

        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            PalParkEncounterSerializer(pal_park_objects, many=True, context=self.context).data,
        )


###############################
#  POKEMON COLOR SERIALIZERS  #
###############################


class PokemonColorNameSerializer(serializers.HyperlinkedModelSerializer[PokemonColorName]):
    language = LanguageSummarySerializer()

    class Meta:
        model = PokemonColorName
        fields = ("name", "language")


class PokemonColorDetailSerializer(serializers.ModelSerializer[PokemonColor]):
    names = PokemonColorNameSerializer(many=True, read_only=True, source="pokemoncolorname")
    pokemon_species = PokemonSpeciesSummarySerializer(many=True, read_only=True, source="pokemonspecies")

    class Meta:
        model = PokemonColor
        fields = ("id", "name", "names", "pokemon_species")


##############################
#  POKEMON FORM SERIALIZERS  #
##############################


class PokemonFormSpritesSerializer(serializers.ModelSerializer[PokemonFormSprites]):
    class Meta:
        model = PokemonFormSprites
        fields = ("sprites",)


class PokemonFormConditionSerializer(serializers.ModelSerializer[PokemonFormCondition]):
    trigger = serializers.CharField(source="form_trigger.name", read_only=True)
    item = ItemSummarySerializer()
    ability = AbilitySummarySerializer()
    move = MoveSummarySerializer()
    base_form = PokemonFormSummarySerializer()

    class Meta:
        model = PokemonFormCondition
        fields = ("trigger", "item", "ability", "move", "base_form")


class PokemonFormNameSerializer(serializers.ModelSerializer[PokemonFormName]):
    language = LanguageSummarySerializer()

    class Meta:
        model = PokemonFormName
        fields = ("name", "language")


class PokemonFormTypeSerializer(serializers.ModelSerializer[PokemonFormType]):
    type = TypeSummarySerializer()

    class Meta:
        model = PokemonFormType
        fields = ("slot", "type")


class PokemonTypeSerializer(serializers.ModelSerializer[PokemonType]):
    type = TypeSummarySerializer()

    class Meta:
        model = PokemonType
        fields = ("slot", "type")


class PokemonFormTriggerConditionSerializer(serializers.Serializer[Any]):
    trigger = serializers.CharField()
    base_form = PokemonFormSummarySerializer()


class PokemonShapeNameSerializer(serializers.ModelSerializer[PokemonShapeName]):
    language = LanguageSummarySerializer()

    class Meta:
        model = PokemonShapeName
        fields = ("name", "language")


class PokemonShapeAwesomeNameSerializer(serializers.ModelSerializer[PokemonShapeName]):
    language = LanguageSummarySerializer()

    class Meta:
        model = PokemonShapeName
        fields = ("awesome_name", "language")


class PokemonFormDetailSerializer(serializers.ModelSerializer[PokemonForm]):
    pokemon = PokemonSummarySerializer()
    version_group = VersionGroupSummarySerializer()
    sprites = serializers.SerializerMethodField("get_pokemon_form_sprites")
    form_names = serializers.SerializerMethodField("get_pokemon_form_names")
    names = serializers.SerializerMethodField("get_pokemon_form_pokemon_names")
    types = serializers.SerializerMethodField("get_pokemon_form_types")
    trigger_conditions = serializers.SerializerMethodField("get_pokemon_form_triggers_conditions")

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
            "trigger_conditions",
        )

    @extend_schema_field(PokemonFormNameSerializer(many=True))
    def get_pokemon_form_names(self, obj: PokemonForm) -> ReturnList[ReturnDict[str, Any]]:
        form_results = PokemonFormName.objects.filter(pokemon_form=obj, name__regex=".+").select_related("language")
        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            PokemonFormNameSerializer(form_results, many=True, context=self.context).data,
        )

    @extend_schema_field(PokemonFormNameSerializer(many=True))
    def get_pokemon_form_pokemon_names(self, obj: PokemonForm) -> ReturnList[ReturnDict[str, Any]]:
        form_results = PokemonFormName.objects.filter(pokemon_form=obj, pokemon_name__regex=".+").select_related(
            "language"
        )
        data = cast(
            "ReturnList[ReturnDict[str, Any]]",
            PokemonFormNameSerializer(form_results, many=True, context=self.context).data,
        )
        for item, fn in zip(data, form_results, strict=True):
            item["name"] = fn.pokemon_name

        return data

    @extend_schema_field(PokemonFormSpritesSerializer)
    def get_pokemon_form_sprites(self, obj: PokemonForm) -> dict[str, Any]:
        sprites_object = PokemonFormSprites.objects.filter(pokemon_form=obj).first()
        return sprites_object.sprites if sprites_object else {}

    @extend_schema_field(PokemonFormTypeSerializer(many=True))
    def get_pokemon_form_types(self, obj: PokemonForm) -> ReturnList[ReturnDict[str, Any]]:
        form_types = PokemonFormType.objects.filter(pokemon_form=obj).select_related("type").order_by("slot")

        if form_types:
            return cast(
                "ReturnList[ReturnDict[str, Any]]",
                PokemonFormTypeSerializer(form_types, many=True, context=self.context).data,
            )

        # Fall back to parent Pokemon's types if no form-specific types exist
        pokemon_types = PokemonType.objects.filter(pokemon=obj.pokemon).select_related("type").order_by("slot")
        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            PokemonTypeSerializer(pokemon_types, many=True, context=self.context).data,
        )

    @extend_schema_field(PokemonFormTriggerConditionSerializer(many=True))
    def get_pokemon_form_triggers_conditions(self, obj: PokemonForm) -> list[dict[str, Any]]:
        conditions = PokemonFormCondition.objects.filter(pokemon_form=obj).select_related(
            "form_trigger", "item", "ability", "move", "base_form"
        )
        conditions_data = cast(
            "ReturnList[ReturnDict[str, Any]]",
            PokemonFormConditionSerializer(conditions, many=True, context=self.context).data,
        )

        triggers: list[dict[str, Any]] = []
        for condition in conditions_data:
            if trigger_value := condition.get("trigger"):
                trigger = {"trigger": trigger_value}
                for key, value in condition.items():
                    if key not in ("trigger", "base_form") and value:
                        trigger.update(value)
                        break
                if base_form := condition.get("base_form"):
                    trigger["base_form"] = base_form
                triggers.append(trigger)

        return triggers


#################################
#  POKEMON HABITAT SERIALIZERS  #
#################################


class PokemonHabitatNameSerializer(serializers.HyperlinkedModelSerializer[PokemonHabitatName]):
    language = LanguageSummarySerializer()

    class Meta:
        model = PokemonHabitatName
        fields = ("name", "language")


class PokemonHabitatDetailSerializer(serializers.ModelSerializer[PokemonHabitat]):
    names = PokemonHabitatNameSerializer(many=True, read_only=True, source="pokemonhabitatname")
    pokemon_species = PokemonSpeciesSummarySerializer(many=True, read_only=True, source="pokemonspecies")

    class Meta:
        model = PokemonHabitat
        fields = ("id", "name", "names", "pokemon_species")


##############################
#  POKEMON MOVE SERIALIZERS  #
##############################


class MoveLearnMethodNameSerializer(serializers.HyperlinkedModelSerializer[MoveLearnMethodName]):
    language = LanguageSummarySerializer()

    class Meta:
        model = MoveLearnMethodName
        fields = ("name", "language")


class MoveLearnMethodDescriptionSerializer(serializers.HyperlinkedModelSerializer[MoveLearnMethodDescription]):
    language = LanguageSummarySerializer()

    class Meta:
        model = MoveLearnMethodDescription
        fields = ("description", "language")


class MoveLearnMethodDetailSerializer(serializers.ModelSerializer[MoveLearnMethod]):
    names = MoveLearnMethodNameSerializer(many=True, read_only=True, source="movelearnmethodname")
    descriptions = MoveLearnMethodDescriptionSerializer(many=True, read_only=True, source="movelearnmethoddescription")
    version_groups = serializers.SerializerMethodField("get_method_version_groups")

    class Meta:
        model = MoveLearnMethod
        fields = ("id", "name", "names", "descriptions", "version_groups")

    @extend_schema_field(VersionGroupSummarySerializer(many=True))
    def get_method_version_groups(self, obj: MoveLearnMethod) -> ReturnList[ReturnDict[str, Any]]:
        version_groups = VersionGroup.objects.filter(versiongroupmovelearnmethod__move_learn_method=obj).distinct()
        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            VersionGroupSummarySerializer(version_groups, many=True, context=self.context).data,
        )


###############################
#  POKEMON SHAPE SERIALIZERS  #
###############################


class PokemonShapeDetailSerializer(serializers.ModelSerializer[PokemonShape]):
    names = serializers.SerializerMethodField("get_shape_names")
    awesome_names = serializers.SerializerMethodField("get_shape_awesome_names")
    pokemon_species = PokemonSpeciesSummarySerializer(many=True, read_only=True, source="pokemonspecies")

    class Meta:
        model = PokemonShape
        fields = ("id", "name", "awesome_names", "names", "pokemon_species")

    @extend_schema_field(PokemonShapeNameSerializer(many=True))
    def get_shape_names(self, obj: PokemonShape) -> ReturnList[ReturnDict[str, Any]]:
        results = PokemonShapeName.objects.filter(pokemon_shape_id=obj).select_related("language")
        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            PokemonShapeNameSerializer(results, many=True, context=self.context).data,
        )

    @extend_schema_field(PokemonShapeAwesomeNameSerializer(many=True))
    def get_shape_awesome_names(self, obj: PokemonShape) -> ReturnList[ReturnDict[str, Any]]:
        results = PokemonShapeName.objects.filter(pokemon_shape_id=obj).select_related("language")
        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            PokemonShapeAwesomeNameSerializer(results, many=True, context=self.context).data,
        )


##############################
#  POKEMON ITEM SERIALIZERS  #
##############################


##############################
#  POKEMON STAT SERIALIZERS  #
##############################


#########################
#  POKEMON SERIALIZERS  #
#########################


class PokemonGameIndexSerializer(serializers.ModelSerializer[PokemonGameIndex]):
    version = VersionSummarySerializer()

    class Meta:
        model = PokemonGameIndex
        fields = ("game_index", "version")


class PokemonAbilitySerializer(serializers.ModelSerializer[PokemonAbility]):
    ability = AbilitySummarySerializer()

    class Meta:
        model = PokemonAbility
        fields = ("is_hidden", "slot", "ability")


class PokemonSpritesSerializer(serializers.Serializer[Any]):
    front_default = serializers.CharField(allow_null=True)


class PokemonCriesSerializer(serializers.Serializer[Any]):
    latest = serializers.CharField(allow_null=True)
    legacy = serializers.CharField(allow_null=True)


class PokemonMoveVersionGroupSerializer(serializers.Serializer[Any]):
    level_learned_at = serializers.IntegerField()
    move_learn_method = MoveLearnMethodSummarySerializer()
    version_group = VersionGroupSummarySerializer()
    order = serializers.IntegerField(required=False)


class PokemonMoveSerializer(serializers.Serializer[Any]):
    move = MoveSummarySerializer()
    version_group_details = PokemonMoveVersionGroupSerializer(many=True)


class PokemonAbilityPastSerializer(serializers.ModelSerializer[PokemonAbilityPast]):
    ability = AbilitySummarySerializer()

    class Meta:
        model = PokemonAbilityPast
        fields = ("is_hidden", "slot", "ability")


class PokemonPastAbilitySerializer(serializers.Serializer[Any]):
    abilities = PokemonAbilityPastSerializer(many=True)
    generation = GenerationSummarySerializer()


class PokemonStatSerializer(serializers.ModelSerializer[PokemonStat]):
    stat = StatSummarySerializer()

    class Meta:
        model = PokemonStat
        fields = ("base_stat", "effort", "stat")


class PokemonPastStatSerializer(serializers.Serializer[Any]):
    generation = GenerationSummarySerializer()
    stats = PokemonStatSerializer(many=True)


class PokemonPastTypeSerializer(serializers.Serializer[Any]):
    generation = GenerationSummarySerializer()
    types = TypePokemonSerializer(many=True)


class PokemonSpeciesNameSerializer(serializers.ModelSerializer[PokemonSpeciesName]):
    language = LanguageSummarySerializer()

    class Meta:
        model = PokemonSpeciesName
        fields = ("name", "language")


class PokemonSpeciesGenusSerializer(serializers.ModelSerializer[PokemonSpeciesName]):
    language = LanguageSummarySerializer()

    class Meta:
        model = PokemonSpeciesName
        fields = ("genus", "language")


class PokemonSpeciesVarietySerializer(serializers.Serializer[Any]):
    is_default = serializers.BooleanField()
    pokemon = PokemonSummarySerializer()


class PokemonSpeciesPalParkEncounterSerializer(serializers.ModelSerializer[PalPark]):
    area = PalParkAreaSummarySerializer(source="pal_park_area")

    class Meta:
        model = PalPark
        fields = ("base_score", "rate", "area")


class PokemonStatPastSerializer(serializers.ModelSerializer[PokemonStatPast]):
    stat = StatSummarySerializer()

    class Meta:
        model = PokemonStatPast
        fields = ("base_stat", "effort", "stat")


class PokemonTypePastSerializer(serializers.ModelSerializer[PokemonTypePast]):
    type = TypeSummarySerializer()

    class Meta:
        model = PokemonTypePast
        fields = ("slot", "type")


class PokemonDetailSerializer(serializers.ModelSerializer[Pokemon]):
    abilities = serializers.SerializerMethodField("get_pokemon_abilities")
    past_abilities = serializers.SerializerMethodField("get_past_pokemon_abilities")
    game_indices = PokemonGameIndexSerializer(many=True, read_only=True, source="pokemongameindex")
    moves = serializers.SerializerMethodField("get_pokemon_moves")
    species = PokemonSpeciesSummarySerializer(source="pokemon_species")
    stats = PokemonStatSerializer(many=True, read_only=True, source="pokemonstat")
    past_stats = serializers.SerializerMethodField("get_past_pokemon_stats")
    types = serializers.SerializerMethodField("get_pokemon_types")
    past_types = serializers.SerializerMethodField("get_past_pokemon_types")
    forms = PokemonFormSummarySerializer(many=True, read_only=True, source="pokemonform")
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
            "past_stats",
            "types",
            "past_types",
        )

    @extend_schema_field(PokemonSpritesSerializer)
    def get_pokemon_sprites(self, obj: Pokemon) -> dict[str, str | None]:
        sprites_list = list(cast("PokemonWithRelations", obj).pokemonsprites.all())
        return sprites_list[0].sprites if sprites_list else {}

    @extend_schema_field(PokemonCriesSerializer)
    def get_pokemon_cries(self, obj: Pokemon) -> dict[str, str | None]:
        cries_list = list(cast("PokemonWithRelations", obj).pokemoncries.all())
        return cries_list[0].cries if cries_list else {}

    @extend_schema_field(PokemonMoveSerializer(many=True))
    def get_pokemon_moves(self, obj: Pokemon) -> list[dict[str, Any]]:
        pokemon_moves = (
            PokemonMove.objects.filter(pokemon=obj, move__isnull=False)
            .select_related("move", "version_group", "move_learn_method")
            .order_by("move__id", "version_group_id")
        )

        vg_cache: dict[int, Any] = {}
        mlm_cache: dict[int, Any] = {}

        moves_grouped: dict[int, dict[str, Any]] = {}
        for pm in pokemon_moves:
            if pm.move is None or pm.version_group is None or pm.move_learn_method is None:
                continue

            move_pk = pm.move.pk
            if move_pk not in moves_grouped:
                moves_grouped[move_pk] = {
                    "move": MoveSummarySerializer(pm.move, context=self.context).data,
                    "version_group_details": [],
                }

            vg_pk = pm.version_group.pk
            if vg_pk not in vg_cache:
                vg_cache[vg_pk] = VersionGroupSummarySerializer(pm.version_group, context=self.context).data
            version_group_data = vg_cache[vg_pk]

            mlm_pk = pm.move_learn_method.pk
            if mlm_pk not in mlm_cache:
                mlm_cache[mlm_pk] = MoveLearnMethodSummarySerializer(pm.move_learn_method, context=self.context).data
            move_learn_method_data = mlm_cache[mlm_pk]

            moves_grouped[move_pk]["version_group_details"].append(
                {
                    "level_learned_at": pm.level,
                    "version_group": version_group_data,
                    "move_learn_method": move_learn_method_data,
                    "order": pm.order,
                }
            )

        return list(moves_grouped.values())

    @extend_schema_field(PokemonHeldItemSerializer(many=True))
    def get_pokemon_held_items(self, obj: Pokemon) -> list[dict[str, Any]]:
        pokemon_items = (
            PokemonItem.objects.filter(pokemon=obj, item__isnull=False)
            .select_related("item", "version")
            .order_by("item__id", "version_id")
        )

        version_cache: dict[int, Any] = {}

        items_grouped: dict[int, dict[str, Any]] = {}
        for pi in pokemon_items:
            if pi.item is None or pi.version is None:
                continue

            item_pk = pi.item.pk
            if item_pk not in items_grouped:
                items_grouped[item_pk] = {
                    "item": ItemSummarySerializer(pi.item, context=self.context).data,
                    "version_details": [],
                }

            v_pk = pi.version.pk
            if v_pk not in version_cache:
                version_cache[v_pk] = VersionSummarySerializer(pi.version, context=self.context).data

            items_grouped[item_pk]["version_details"].append(
                {
                    "rarity": pi.rarity,
                    "version": version_cache[v_pk],
                }
            )

        return list(items_grouped.values())

    @extend_schema_field(PokemonAbilitySerializer(many=True))
    def get_pokemon_abilities(self, obj: Pokemon) -> ReturnList[ReturnDict[str, Any]]:
        abilities = PokemonAbility.objects.filter(pokemon=obj).select_related("ability")
        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            PokemonAbilitySerializer(abilities, many=True, context=self.context).data,
        )

    @extend_schema_field(PokemonPastAbilitySerializer(many=True))
    def get_past_pokemon_abilities(self, obj: Pokemon) -> list[dict[str, Any]]:
        past_abilities = (
            PokemonAbilityPast.objects.filter(pokemon=obj, generation__isnull=False)
            .select_related("generation", "ability")
            .order_by("generation_id")
        )

        final_data: list[dict[str, Any]] = []
        for _, group in itertools.groupby(past_abilities, key=lambda x: cast("Generation", x.generation).name):
            group_list: Sequence[PokemonAbilityPast] = list(group)
            gen_data = cast(
                "ReturnDict[str, Any]",
                GenerationSummarySerializer(group_list[0].generation, context=self.context).data,
            )
            abilities_data = cast(
                "ReturnList[ReturnDict[str, Any]]",
                PokemonAbilityPastSerializer(group_list, many=True, context=self.context).data,
            )
            final_data.append(
                {
                    "generation": gen_data,
                    "abilities": abilities_data,
                }
            )

        return final_data

    @extend_schema_field(PokemonPastStatSerializer(many=True))
    def get_past_pokemon_stats(self, obj: Pokemon) -> list[dict[str, Any]]:
        past_stats = (
            PokemonStatPast.objects.filter(pokemon=obj, generation__isnull=False)
            .select_related("generation", "stat")
            .order_by("generation_id")
        )

        final_data: list[dict[str, Any]] = []
        for _, group in itertools.groupby(past_stats, key=lambda x: cast("Generation", x.generation).name):
            group_list: Sequence[PokemonStatPast] = list(group)
            gen_data = cast(
                "ReturnDict[str, Any]",
                GenerationSummarySerializer(group_list[0].generation, context=self.context).data,
            )
            stats_data = cast(
                "ReturnList[ReturnDict[str, Any]]",
                PokemonStatPastSerializer(group_list, many=True, context=self.context).data,
            )
            final_data.append(
                {
                    "generation": gen_data,
                    "stats": stats_data,
                }
            )

        return final_data

    @extend_schema_field(PokemonTypeSerializer(many=True))
    def get_pokemon_types(self, obj: Pokemon) -> ReturnList[ReturnDict[str, Any]]:
        types = PokemonType.objects.filter(pokemon=obj).select_related("type").order_by("slot")
        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            PokemonTypeSerializer(types, many=True, context=self.context).data,
        )

    @extend_schema_field(PokemonPastTypeSerializer(many=True))
    def get_past_pokemon_types(self, obj: Pokemon) -> list[dict[str, Any]]:
        past_types = (
            PokemonTypePast.objects.filter(pokemon=obj, generation__isnull=False)
            .select_related("generation", "type")
            .order_by("generation_id", "slot")
        )

        final_data: list[dict[str, Any]] = []
        for _, group in itertools.groupby(past_types, key=lambda x: cast("Generation", x.generation).name):
            group_list: Sequence[PokemonTypePast] = list(group)
            gen_data = cast(
                "ReturnDict[str, Any]", GenerationSummarySerializer(group_list[0].generation, context=self.context).data
            )
            types_data = cast(
                "ReturnList[ReturnDict[str, Any]]",
                PokemonTypePastSerializer(group_list, many=True, context=self.context).data,
            )
            final_data.append(
                {
                    "generation": gen_data,
                    "types": types_data,
                }
            )

        return final_data

    @extend_schema_field(serializers.CharField)
    def get_encounters(self, obj: Pokemon) -> str:
        return reverse("pokemon_encounters", kwargs={"pokemon_id": obj.pk}, request=self.context.get("request"))


#################################
#  POKEMON SPECIES SERIALIZERS  #
#################################


class EvolutionTriggerNameSerializer(serializers.HyperlinkedModelSerializer[EvolutionTriggerName]):
    language = LanguageSummarySerializer()

    class Meta:
        model = EvolutionTriggerName
        fields = ("name", "language")


class EvolutionTriggerDetailSerializer(serializers.HyperlinkedModelSerializer[EvolutionTrigger]):
    names = EvolutionTriggerNameSerializer(many=True, read_only=True, source="evolutiontriggername")
    pokemon_species = serializers.SerializerMethodField("get_species")

    class Meta:
        model = EvolutionTrigger
        fields = ("id", "name", "names", "pokemon_species")

    @extend_schema_field(PokemonSpeciesSummarySerializer(many=True))
    def get_species(self, obj: EvolutionTrigger) -> ReturnList[ReturnDict[str, Any]]:
        species = PokemonSpecies.objects.filter(evolved_species__evolution_trigger=obj).distinct().order_by("id")
        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            PokemonSpeciesSummarySerializer(species, many=True, context=self.context).data,
        )


class PokemonSpeciesDescriptionSerializer(serializers.ModelSerializer[PokemonSpeciesDescription]):
    language = LanguageSummarySerializer()

    class Meta:
        model = PokemonSpeciesDescription
        fields = ("description", "language")


class PokemonSpeciesFlavorTextSerializer(serializers.ModelSerializer[PokemonSpeciesFlavorText]):
    flavor_text = serializers.CharField()
    language = LanguageSummarySerializer()
    version = VersionSummarySerializer()

    class Meta:
        model = PokemonSpeciesFlavorText
        fields = ("flavor_text", "language", "version")


class PokemonSpeciesEvolutionSerializer(serializers.ModelSerializer[PokemonSpecies]):
    """
    This is here purely to help build pokemon evolution chains
    """

    class Meta:
        model = PokemonSpecies
        fields = ("name", "id", "evolves_from_species", "is_baby")


class PokemonSpeciesDetailSerializer(serializers.ModelSerializer[PokemonSpecies]):
    names = serializers.SerializerMethodField("get_pokemon_names")
    form_descriptions = PokemonSpeciesDescriptionSerializer(
        many=True, read_only=True, source="pokemonspeciesdescription"
    )
    pokedex_numbers = PokemonDexEntrySerializer(many=True, read_only=True, source="pokemondexnumber")
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

    @extend_schema_field(PokemonSpeciesNameSerializer(many=True))
    def get_pokemon_names(self, obj: PokemonSpecies) -> ReturnList[ReturnDict[str, Any]]:
        species_results = PokemonSpeciesName.objects.filter(pokemon_species=obj).select_related("language")
        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            PokemonSpeciesNameSerializer(species_results, many=True, context=self.context).data,
        )

    @extend_schema_field(PokemonSpeciesGenusSerializer(many=True))
    def get_pokemon_genera(self, obj: PokemonSpecies) -> ReturnList[ReturnDict[str, Any]]:
        results = (
            PokemonSpeciesName.objects.filter(pokemon_species=obj, genus__isnull=False)
            .exclude(genus="")
            .select_related("language")
        )
        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            PokemonSpeciesGenusSerializer(results, many=True, context=self.context).data,
        )

    @extend_schema_field(EggGroupSummarySerializer(many=True))
    def get_pokemon_egg_groups(self, obj: PokemonSpecies) -> ReturnList[ReturnDict[str, Any]]:
        egg_groups = EggGroup.objects.filter(pokemonegggroup__pokemon_species=obj).distinct()
        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            EggGroupSummarySerializer(egg_groups, many=True, context=self.context).data,
        )

    @extend_schema_field(PokemonSpeciesVarietySerializer(many=True))
    def get_pokemon_varieties(self, obj: PokemonSpecies) -> list[dict[str, Any]]:
        pokemon_list = Pokemon.objects.filter(pokemon_species=obj)
        summaries = cast(
            "ReturnList[ReturnDict[str, Any]]",
            PokemonSummarySerializer(pokemon_list, many=True, context=self.context).data,
        )
        return [
            {
                "is_default": pk.is_default,
                "pokemon": summary,
            }
            for pk, summary in zip(pokemon_list, summaries, strict=True)
        ]

    @extend_schema_field(PokemonSpeciesPalParkEncounterSerializer(many=True))
    def get_encounters(self, obj: PokemonSpecies) -> ReturnList[ReturnDict[str, Any]]:
        pal_park_objects = PalPark.objects.filter(pokemon_species=obj).select_related("pal_park_area")
        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            PokemonSpeciesPalParkEncounterSerializer(pal_park_objects, many=True, context=self.context).data,
        )


class PokemonEvolutionSerializer(serializers.ModelSerializer[PokemonEvolution]):
    version_group = VersionGroupSummarySerializer()
    item = ItemSummarySerializer(source="evolution_item")
    held_item = ItemSummarySerializer()
    known_move = MoveSummarySerializer()
    known_move_type = TypeSummarySerializer()
    party_species = PokemonSpeciesSummarySerializer()
    party_type = TypeSummarySerializer()
    trade_species = PokemonSpeciesSummarySerializer()
    location = LocationSummarySerializer()
    trigger = EvolutionTriggerSummarySerializer(source="evolution_trigger")
    region = RegionSummarySerializer()
    base_form = PokemonSummarySerializer()
    evolved_form = PokemonSummarySerializer()
    used_move = MoveSummarySerializer()

    class Meta:
        model = PokemonEvolution
        fields = (
            "version_group",
            "is_default",
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
            "near_special_rock",
            "needs_multiplayer",
            "needs_overworld_rain",
            "party_species",
            "party_type",
            "relative_physical_stats",
            "time_of_day",
            "trade_species",
            "turn_upside_down",
            "region",
            "base_form",
            "evolved_form",
            "used_move",
            "min_move_count",
            "min_steps",
            "min_damage_taken",
        )


class EvolutionChainLinkSerializer(serializers.Serializer[Any]):
    is_baby = serializers.BooleanField()
    species = PokemonSpeciesSummarySerializer()
    evolution_details = PokemonEvolutionSerializer(many=True)
    evolves_to = serializers.ListField(child=serializers.DictField())


class EvolutionChainDetailSerializer(serializers.ModelSerializer[EvolutionChain]):
    baby_trigger_item = ItemSummarySerializer()
    chain = serializers.SerializerMethodField("build_chain")

    POKEMON_EVOLUTION_FK_FIELDS: ClassVar[list[str]] = [
        field.name
        for field in PokemonEvolution._meta.get_fields()
        if field.is_relation and (field.many_to_one or field.one_to_one)
    ]

    class Meta:
        model = EvolutionChain
        fields = ("id", "baby_trigger_item", "chain")

    @extend_schema_field(EvolutionChainLinkSerializer)
    def build_chain(self, obj: EvolutionChain) -> dict[str, Any]:
        pokemon_objects = PokemonSpecies.objects.filter(evolution_chain=obj).order_by("order")
        summary_data = cast(
            "ReturnList[ReturnDict[str, Any]]",
            PokemonSpeciesSummarySerializer(pokemon_objects, many=True, context=self.context).data,
        )
        ref_data = cast(
            "ReturnList[ReturnDict[str, Any]]",
            PokemonSpeciesEvolutionSerializer(pokemon_objects, many=True, context=self.context).data,
        )

        evolution_tree = self.build_evolution_tree(ref_data)
        return self.build_chain_link_entry(evolution_tree, summary_data)

    # converts a list of Pokemon species evolution data into a tree representing the evolution chain
    def build_evolution_tree(self, species_evolution_data: ReturnList[ReturnDict[str, Any]]) -> dict[str, Any]:
        if not species_evolution_data:
            return {}

        first_species: dict[str, Any] = species_evolution_data[0]
        evolution_tree: dict[str, Any] = {"species": first_species, "children": []}

        for species in species_evolution_data[1:]:
            species_item: dict[str, Any] = species
            chain_link: dict[str, Any] = {
                "species": species_item,
                "children": [],
            }

            species_dict: dict[str, Any] = chain_link["species"]
            evolves_from_species_id = species_dict["evolves_from_species"]

            parent_link = evolution_tree
            search_stack = [parent_link]

            while search_stack:
                link = search_stack.pop()
                if link["species"]["id"] == evolves_from_species_id:
                    parent_link = link
                    break
                search_stack.extend(reversed(link["children"]))

            parent_link["children"].append(chain_link)

        return evolution_tree

    # serializes an evolution chain link recursively
    # chain_link is a tree representing an evolution chain
    def build_chain_link_entry(
        self, chain_link: dict[str, Any], summary_data: ReturnList[ReturnDict[str, Any]]
    ) -> dict[str, Any]:
        species = chain_link["species"]
        evolution_data = None

        if species["evolves_from_species"]:
            evolution_objects = PokemonEvolution.objects.filter(evolved_species=species["id"]).select_related(
                *self.POKEMON_EVOLUTION_FK_FIELDS
            )
            evolution_data = cast(
                "ReturnList[ReturnDict[str, Any]]",
                PokemonEvolutionSerializer(evolution_objects, many=True, context=self.context).data,
            )

        return {
            "is_baby": species["is_baby"],
            "species": next(x for x in summary_data if x["name"] == species["name"]),
            "evolution_details": evolution_data or [],
            "evolves_to": [self.build_chain_link_entry(c, summary_data) for c in chain_link["children"]],
        }


############################
#  POKEATHLON SERIALIZERS  #
############################


class PokeathlonStatNameSerializer(serializers.HyperlinkedModelSerializer[PokeathlonStatName]):
    language = LanguageSummarySerializer()

    class Meta:
        model = PokeathlonStatName
        fields = ("name", "language")


class PokeathlonStatAffectingNatureSerializer(serializers.ModelSerializer[NaturePokeathlonStat]):
    nature = NatureSummarySerializer()

    class Meta:
        model = NaturePokeathlonStat
        fields = ("max_change", "nature")


class PokeathlonStatAffectingNaturesSerializer(serializers.Serializer[Any]):
    increase = PokeathlonStatAffectingNatureSerializer(many=True)
    decrease = PokeathlonStatAffectingNatureSerializer(many=True)


class PokeathlonStatDetailSerializer(serializers.HyperlinkedModelSerializer[PokeathlonStat]):
    names = PokeathlonStatNameSerializer(many=True, read_only=True, source="pokeathlonstatname")
    affecting_natures = serializers.SerializerMethodField("get_natures_that_affect")

    class Meta:
        model = PokeathlonStat
        fields = ("id", "name", "affecting_natures", "names")

    @extend_schema_field(PokeathlonStatAffectingNaturesSerializer)
    def get_natures_that_affect(self, obj: PokeathlonStat) -> dict[str, ReturnList[ReturnDict[str, Any]]]:
        base_qs = NaturePokeathlonStat.objects.filter(pokeathlon_stat=obj).select_related("nature")
        increases = base_qs.filter(max_change__gt=0)
        decreases = base_qs.filter(max_change__lte=0)
        return {
            "increase": cast(
                "ReturnList[ReturnDict[str, Any]]",
                PokeathlonStatAffectingNatureSerializer(increases, many=True, context=self.context).data,
            ),
            "decrease": cast(
                "ReturnList[ReturnDict[str, Any]]",
                PokeathlonStatAffectingNatureSerializer(decreases, many=True, context=self.context).data,
            ),
        }


#########################
#  POKEDEX SERIALIZERS  #
#########################


class PokedexNameSerializer(serializers.HyperlinkedModelSerializer[PokedexName]):
    language = LanguageSummarySerializer()

    class Meta:
        model = PokedexName
        fields = ("name", "language")


class PokedexDescriptionSerializer(serializers.HyperlinkedModelSerializer[PokedexDescription]):
    language = LanguageSummarySerializer()

    class Meta:
        model = PokedexDescription
        fields = ("description", "language")


class PokemonDexNumberSerializer(serializers.ModelSerializer[PokemonDexNumber]):
    entry_number = serializers.IntegerField(source="pokedex_number")
    pokemon_species = PokemonSpeciesSummarySerializer()

    class Meta:
        model = PokemonDexNumber
        fields = ("entry_number", "pokemon_species")


class PokedexDetailSerializer(serializers.ModelSerializer[Pokedex]):
    region = RegionSummarySerializer()
    names = PokedexNameSerializer(many=True, read_only=True, source="pokedexname")
    descriptions = PokedexDescriptionSerializer(many=True, read_only=True, source="pokedexdescription")
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

    @extend_schema_field(PokemonDexNumberSerializer(many=True))
    def get_pokedex_entries(self, obj: Pokedex) -> ReturnList[ReturnDict[str, Any]]:
        entries = (
            PokemonDexNumber.objects.filter(pokedex=obj).select_related("pokemon_species").order_by("pokedex_number")
        )
        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            PokemonDexNumberSerializer(entries, many=True, context=self.context).data,
        )

    @extend_schema_field(VersionGroupSummarySerializer(many=True))
    def get_pokedex_version_groups(self, obj: Pokedex) -> ReturnList[ReturnDict[str, Any]]:
        version_groups = VersionGroup.objects.filter(pokedexversiongroup__pokedex=obj).distinct()
        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            VersionGroupSummarySerializer(version_groups, many=True, context=self.context).data,
        )


#########################
#  VERSION SERIALIZERS  #
#########################


class VersionNameSerializer(serializers.ModelSerializer[VersionName]):
    language = LanguageSummarySerializer()

    class Meta:
        model = VersionName
        fields = ("name", "language")


class VersionDetailSerializer(serializers.ModelSerializer[Version]):
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


class VersionGroupDetailSerializer(serializers.ModelSerializer[VersionGroup]):
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

    @extend_schema_field(RegionSummarySerializer(many=True))
    def get_version_group_regions(self, obj: VersionGroup) -> ReturnList[ReturnDict[str, Any]]:
        regions = Region.objects.filter(versiongroupregion__version_group=obj).distinct()
        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            RegionSummarySerializer(regions, many=True, context=self.context).data,
        )

    @extend_schema_field(MoveLearnMethodSummarySerializer(many=True))
    def get_learn_methods(self, obj: VersionGroup) -> ReturnList[ReturnDict[str, Any]]:
        methods = MoveLearnMethod.objects.filter(versiongroupmovelearnmethod__version_group=obj).distinct()
        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            MoveLearnMethodSummarySerializer(methods, many=True, context=self.context).data,
        )

    @extend_schema_field(PokedexSummarySerializer(many=True))
    def get_version_groups_pokedexes(self, obj: VersionGroup) -> ReturnList[ReturnDict[str, Any]]:
        pokedexes = Pokedex.objects.filter(pokedexversiongroup__version_group=obj).distinct()
        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            PokedexSummarySerializer(pokedexes, many=True, context=self.context).data,
        )
