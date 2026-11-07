# ruff: noqa: F405, E501
# pyright: reportIncompatibleVariableOverride=false, reportUnknownMemberType=false
from __future__ import annotations

import itertools
from collections import defaultdict
from functools import cached_property
from typing import TYPE_CHECKING, Any, ClassVar, Protocol, cast

from django.db.models import Q
from drf_spectacular.helpers import lazy_serializer
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
    "EvolutionConditionExpressionSerializer",
    "EvolutionTriggerDetailSerializer",
    "EvolutionTriggerNameSerializer",
    "EvolutionTriggerSummarySerializer",
    "EvolutionVariableDescriptionSerializer",
    "EvolutionVariableDetailSerializer",
    "EvolutionVariableNameSerializer",
    "EvolutionVariableSummarySerializer",
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
    "PokemonHeldItemSummarySerializer",
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
    "PokemonSpritesOtherDreamWorldSerializer",
    "PokemonSpritesOtherHomeSerializer",
    "PokemonSpritesOtherOfficialArtworkSerializer",
    "PokemonSpritesOtherSerializer",
    "PokemonSpritesOtherShowdownSerializer",
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
    "TypeGameSpriteSerializer",
    "TypeNameSerializer",
    "TypePastRelationshipsSerializer",
    "TypePokemonSerializer",
    "TypeRelationshipsSerializer",
    "TypeSummarySerializer",
    "VersionDetailSerializer",
    "VersionGroupDetailSerializer",
    "VersionGroupSummarySerializer",
    "VersionNameSerializer",
    "VersionSummarySerializer",
)

NAME_LANGUAGE_HELP: str = "The language this name is in."
LOCALIZED_NAMES_HELP: str = "The name of this resource listed in different languages."
EFFECT_LANGUAGE_HELP: str = "The language this effect is in."
LOCALIZED_DESCRIPTIONS_HELP: str = "The description of this resource listed in different languages."
GAME_INDEX_GENERATION_HELP: str = "The generation relevent to this game index."
RESOURCE_URL_HELP: str = "The URL of the referenced resource."
RESOURCE_ID_HELP: str = "The identifier for this resource."
REFERENCE_NAME_HELP: str = "The name of the referenced resource."
RESOURCE_NAME_HELP: str = "The name for this resource."
LOCALIZED_NAME_HELP: str = "The localized name for an API resource in a specific language."
LOCALIZED_DESCRIPTION_HELP: str = "The localized description for an API resource in a specific language."
LOCALIZED_EFFECT_HELP: str = "The localized effect text for an API resource in a specific language."
GAME_INDEX_HELP: str = "The internal id of an API resource within game data."
POKEMON_TYPE_SLOT_HELP: str = "The order the Pokémon's types are listed in."
LOCALIZED_SHORT_EFFECT_HELP: str = "The localized effect text in brief."
LOCALIZED_FLAVOR_TEXT_HELP: str = "The localized flavor text for an API resource in a specific language."
BERRY_FLAVOR_POTENCY_HELP: str = "How powerful the referenced flavor is for this berry."
MOVE_ACCURACY_HELP: str = "The percent value of how likely this move is to be successful."
MOVE_PP_HELP: str = "Power points. The number of times this move can be used."
POKEMON_ABILITY_HIDDEN_HELP: str = "Whether or not this is a hidden ability."
POKEMON_ABILITY_SLOT_HELP: str = "The slot this ability occupies in this Pokémon species."
POKEMON_BASE_STAT_HELP: str = "The base value of the stat."
POKEMON_EFFORT_HELP: str = "The effort points (EV) the Pokémon has in the stat."


def format_help_text(**fields: str) -> dict[str, dict[str, str]]:
    return {name: {"help_text": text} for name, text in fields.items()}


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
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


class BerryFirmnessSummarySerializer(serializers.HyperlinkedModelSerializer[BerryFirmness]):
    class Meta:
        model = BerryFirmness
        fields = ("name", "url")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


class BerryFlavorSummarySerializer(serializers.HyperlinkedModelSerializer[BerryFlavor]):
    class Meta:
        model = BerryFlavor
        fields = ("name", "url")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


class BerrySummarySerializer(serializers.HyperlinkedModelSerializer[Berry]):
    class Meta:
        model = Berry
        fields = ("name", "url")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


class CharacteristicSummarySerializer(serializers.HyperlinkedModelSerializer[Characteristic]):
    class Meta:
        model = Characteristic
        fields = ("url",)
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            url=RESOURCE_URL_HELP,
        )


class ContestEffectSummarySerializer(serializers.HyperlinkedModelSerializer[ContestEffect]):
    class Meta:
        model = ContestEffect
        fields = ("url",)
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            url=RESOURCE_URL_HELP,
        )


class ContestTypeSummarySerializer(serializers.HyperlinkedModelSerializer[ContestType]):
    class Meta:
        model = ContestType
        fields = ("name", "url")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


class EggGroupSummarySerializer(serializers.HyperlinkedModelSerializer[EggGroup]):
    class Meta:
        model = EggGroup
        fields = ("name", "url")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


class EncounterConditionSummarySerializer(serializers.HyperlinkedModelSerializer[EncounterCondition]):
    class Meta:
        model = EncounterCondition
        fields = ("name", "url")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


class EncounterConditionValueSummarySerializer(serializers.HyperlinkedModelSerializer[EncounterConditionValue]):
    class Meta:
        model = EncounterConditionValue
        fields = ("name", "url")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


class EncounterMethodSummarySerializer(serializers.HyperlinkedModelSerializer[EncounterMethod]):
    class Meta:
        model = EncounterMethod
        fields = ("name", "url")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


class EvolutionTriggerSummarySerializer(serializers.HyperlinkedModelSerializer[EvolutionTrigger]):
    class Meta:
        model = EvolutionTrigger
        fields = ("name", "url")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


class EvolutionVariableSummarySerializer(serializers.HyperlinkedModelSerializer[EvolutionVariable]):
    class Meta:
        model = EvolutionVariable
        fields = ("name", "url")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


class EvolutionConditionExpressionSerializer(serializers.Serializer[Any]):
    expression = serializers.CharField(
        help_text="Evaluatable RPN condition expression using evolution variables (e.g. 'EC 100 % 0 ==')"
    )
    percentage_chance = serializers.FloatField(
        allow_null=True,
        help_text="Percentage chance of evolution under this condition (0-100)",
    )
    variables = EvolutionVariableSummarySerializer(
        many=True,
        help_text="Evolution variables referenced in the expression",
    )


class EvolutionChainSummarySerializer(serializers.HyperlinkedModelSerializer[EvolutionChain]):
    class Meta:
        model = EvolutionChain
        fields = ("url",)
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            url=RESOURCE_URL_HELP,
        )


class GenerationSummarySerializer(serializers.HyperlinkedModelSerializer[Generation]):
    class Meta:
        model = Generation
        fields = ("name", "url")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


class GenderSummarySerializer(serializers.HyperlinkedModelSerializer[Gender]):
    class Meta:
        model = Gender
        fields = ("name", "url")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


class GrowthRateSummarySerializer(serializers.HyperlinkedModelSerializer[GrowthRate]):
    class Meta:
        model = GrowthRate
        fields = ("name", "url")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


class CurrencySummarySerializer(serializers.HyperlinkedModelSerializer[Currency]):
    class Meta:
        model = Currency
        fields = ("name", "url")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


class ItemPocketSummarySerializer(serializers.HyperlinkedModelSerializer[ItemPocket]):
    class Meta:
        model = ItemPocket
        fields = ("name", "url")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


class ItemCategorySummarySerializer(serializers.HyperlinkedModelSerializer[ItemCategory]):
    class Meta:
        model = ItemCategory
        fields = ("name", "url")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


class ItemAttributeSummarySerializer(serializers.HyperlinkedModelSerializer[ItemAttribute]):
    class Meta:
        model = ItemAttribute
        fields = ("name", "url")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


class ItemFlingEffectSummarySerializer(serializers.HyperlinkedModelSerializer[ItemFlingEffect]):
    class Meta:
        model = ItemFlingEffect
        fields = ("name", "url")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


class ItemSummarySerializer(serializers.HyperlinkedModelSerializer[Item]):
    class Meta:
        model = Item
        fields = ("name", "url")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


class LanguageSummarySerializer(serializers.HyperlinkedModelSerializer[Language]):
    class Meta:
        model = Language
        fields = ("name", "url")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


class LocationSummarySerializer(serializers.HyperlinkedModelSerializer[Location]):
    class Meta:
        model = Location
        fields = ("name", "url")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


class LocationAreaSummarySerializer(serializers.HyperlinkedModelSerializer[LocationArea]):
    class Meta:
        model = LocationArea
        fields = ("name", "url")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


class MachineSummarySerializer(serializers.HyperlinkedModelSerializer[Machine]):
    class Meta:
        model = Machine
        fields = ("url",)
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            url=RESOURCE_URL_HELP,
        )


class MoveBattleStyleSummarySerializer(serializers.HyperlinkedModelSerializer[MoveBattleStyle]):
    class Meta:
        model = MoveBattleStyle
        fields = ("name", "url")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


class MoveDamageClassSummarySerializer(serializers.HyperlinkedModelSerializer[MoveDamageClass]):
    class Meta:
        model = MoveDamageClass
        fields = ("name", "url")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


class MoveMetaAilmentSummarySerializer(serializers.HyperlinkedModelSerializer[MoveMetaAilment]):
    class Meta:
        model = MoveMetaAilment
        fields = ("name", "url")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


class MoveMetaCategorySummarySerializer(serializers.HyperlinkedModelSerializer[MoveMetaCategory]):
    class Meta:
        model = MoveMetaCategory
        fields = ("name", "url")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


class MoveTargetSummarySerializer(serializers.HyperlinkedModelSerializer[MoveTarget]):
    class Meta:
        model = MoveTarget
        fields = ("name", "url")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


class MoveSummarySerializer(serializers.HyperlinkedModelSerializer[Move]):
    class Meta:
        model = Move
        fields = ("name", "url")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


class MoveLearnMethodSummarySerializer(serializers.HyperlinkedModelSerializer[MoveLearnMethod]):
    class Meta:
        model = MoveLearnMethod
        fields = ("name", "url")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


class NatureSummarySerializer(serializers.HyperlinkedModelSerializer[Nature]):
    class Meta:
        model = Nature
        fields = ("name", "url")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


class PalParkAreaSummarySerializer(serializers.HyperlinkedModelSerializer[PalParkArea]):
    class Meta:
        model = PalParkArea
        fields = ("name", "url")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


class PokeathlonStatSummarySerializer(serializers.HyperlinkedModelSerializer[PokeathlonStat]):
    class Meta:
        model = PokeathlonStat
        fields = ("name", "url")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


class PokedexSummarySerializer(serializers.HyperlinkedModelSerializer[Pokedex]):
    class Meta:
        model = Pokedex
        fields = ("name", "url")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


class PokemonColorSummarySerializer(serializers.HyperlinkedModelSerializer[PokemonColor]):
    class Meta:
        model = PokemonColor
        fields = ("name", "url")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


class PokemonHabitatSummarySerializer(serializers.HyperlinkedModelSerializer[PokemonHabitat]):
    class Meta:
        model = PokemonHabitat
        fields = ("name", "url")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


class PokemonShapeSummarySerializer(serializers.HyperlinkedModelSerializer[PokemonShape]):
    class Meta:
        model = PokemonShape
        fields = ("name", "url")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


class PokemonSummarySerializer(serializers.HyperlinkedModelSerializer[Pokemon]):
    class Meta:
        model = Pokemon
        fields = ("name", "url")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


class PokemonSpeciesSummarySerializer(serializers.HyperlinkedModelSerializer[PokemonSpecies]):
    class Meta:
        model = PokemonSpecies
        fields = ("name", "url")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


class PokemonFormSummarySerializer(serializers.HyperlinkedModelSerializer[PokemonForm]):
    class Meta:
        model = PokemonForm
        fields = ("name", "url")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


class RegionSummarySerializer(serializers.HyperlinkedModelSerializer[Region]):
    class Meta:
        model = Region
        fields = ("name", "url")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


class StatSummarySerializer(serializers.HyperlinkedModelSerializer[Stat]):
    class Meta:
        model = Stat
        fields = ("name", "url")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


class SuperContestEffectSummarySerializer(serializers.HyperlinkedModelSerializer[SuperContestEffect]):
    class Meta:
        model = SuperContestEffect
        fields = ("url",)
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            url=RESOURCE_URL_HELP,
        )


class TypeSummarySerializer(serializers.HyperlinkedModelSerializer[Type]):
    class Meta:
        model = Type
        fields = ("name", "url")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


class VersionSummarySerializer(serializers.HyperlinkedModelSerializer[Version]):
    class Meta:
        model = Version
        fields = ("name", "url")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


class VersionGroupSummarySerializer(serializers.HyperlinkedModelSerializer[VersionGroup]):
    class Meta:
        model = VersionGroup
        fields = ("name", "url")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=REFERENCE_NAME_HELP,
            url=RESOURCE_URL_HELP,
        )


#####################
#  MAP SERIALIZERS  #
#####################


class PokemonDexEntrySerializer(serializers.ModelSerializer[PokemonDexNumber]):
    entry_number = serializers.IntegerField(source="pokedex_number", help_text="The index number within the Pokédex.")
    pokedex = PokedexSummarySerializer(help_text="The Pokédex the referenced Pokémon species can be found in.")

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
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = CharacteristicDescription
        fields = ("description", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            description=LOCALIZED_DESCRIPTION_HELP,
        )


class CharacteristicDetailSerializer(serializers.ModelSerializer[Characteristic]):
    descriptions = CharacteristicDescriptionSerializer(
        many=True,
        read_only=True,
        source="characteristicdescription",
        help_text="The descriptions of this characteristic listed in different languages.",
    )
    highest_stat = StatSummarySerializer(source="stat", help_text="The stat which results in this characteristic.")
    gene_modulo = serializers.IntegerField(
        source="gene_mod_5", help_text="The remainder of the highest stat/IV divided by 5."
    )
    possible_values = serializers.SerializerMethodField(
        "get_values",
        help_text="The possible values of the highest stat that would result in a Pokémon recieving this characteristic when divided by 5.",
    )

    class Meta:
        model = Characteristic
        fields = (
            "id",
            "gene_modulo",
            "possible_values",
            "highest_stat",
            "descriptions",
        )
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
        )

    @extend_schema_field(serializers.ListField(child=serializers.IntegerField()))
    def get_values(self, obj: Characteristic) -> list[int]:
        return list(range(obj.gene_mod_5, 32, 5))


#########################
#  CONTEST SERIALIZERS  #
#########################


class SuperContestEffectFlavorTextSerializer(serializers.ModelSerializer[SuperContestEffectFlavorText]):
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = SuperContestEffectFlavorText
        fields = ("flavor_text", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            flavor_text=LOCALIZED_FLAVOR_TEXT_HELP,
        )


class SuperContestEffectDetailSerializer(serializers.ModelSerializer[SuperContestEffect]):
    flavor_text_entries = SuperContestEffectFlavorTextSerializer(
        many=True,
        read_only=True,
        source="supercontesteffectflavortext",
        help_text="The flavor text of this super contest effect listed in different languages.",
    )
    moves = MoveSummarySerializer(
        many=True,
        read_only=True,
        source="move",
        help_text="A list of moves that have the effect when used in super contests.",
    )

    class Meta:
        model = SuperContestEffect
        fields = ("id", "appeal", "flavor_text_entries", "moves")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            appeal="The level of appeal this super contest effect has.",
        )


class ContestEffectEffectTextSerializer(serializers.ModelSerializer[ContestEffectEffectText]):
    language = LanguageSummarySerializer(help_text=EFFECT_LANGUAGE_HELP)

    class Meta:
        model = ContestEffectEffectText
        fields = ("effect", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            effect=LOCALIZED_EFFECT_HELP,
        )


class ContestEffectFlavorTextSerializer(serializers.ModelSerializer[ContestEffectFlavorText]):
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = ContestEffectFlavorText
        fields = ("flavor_text", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            flavor_text=LOCALIZED_FLAVOR_TEXT_HELP,
        )


class ContestEffectDetailSerializer(serializers.ModelSerializer[ContestEffect]):
    effect_entries = ContestEffectEffectTextSerializer(
        many=True,
        read_only=True,
        source="contesteffecteffecttext",
        help_text="The result of this contest effect listed in different languages.",
    )
    flavor_text_entries = ContestEffectFlavorTextSerializer(
        many=True,
        read_only=True,
        source="contesteffectflavortext",
        help_text="The flavor text of this contest effect listed in different languages.",
    )

    class Meta:
        model = ContestEffect
        fields = ("id", "appeal", "jam", "effect_entries", "flavor_text_entries")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            appeal="The base number of hearts the user of this move gets.",
            jam="The base number of hearts the user's opponent loses.",
        )


class ContestTypeNameSerializer(serializers.ModelSerializer[ContestTypeName]):
    language = LanguageSummarySerializer(help_text="The language that this name is in.")

    class Meta:
        model = ContestTypeName
        fields = ("name", "color", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name="The name for this contest.",
            color="The color associated with this contest's name.",
        )


class ContestTypeDetailSerializer(serializers.ModelSerializer[ContestType]):
    names = ContestTypeNameSerializer(
        many=True,
        read_only=True,
        source="contesttypename",
        help_text="The name of this contest type listed in different languages.",
    )
    berry_flavor = BerryFlavorSummarySerializer(
        read_only=True, source="berryflavor", help_text="The berry flavor that correlates with this contest type."
    )

    class Meta:
        model = ContestType
        fields = ("id", "name", "berry_flavor", "names")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
        )


########################
#  REGION SERIALIZERS  #
########################


class RegionNameSerializer(serializers.ModelSerializer[RegionName]):
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = RegionName
        fields = ("name", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=LOCALIZED_NAME_HELP,
        )


class RegionDetailSerializer(serializers.ModelSerializer[Region]):
    names = RegionNameSerializer(
        many=True,
        read_only=True,
        source="regionname",
        help_text=LOCALIZED_NAMES_HELP,
    )
    locations = LocationSummarySerializer(
        many=True, read_only=True, source="location", help_text="A list of locations that can be found in this region."
    )
    version_groups = serializers.SerializerMethodField(
        "get_region_version_groups", help_text="A list of version groups where this region can be visited."
    )
    pokedexes = PokedexSummarySerializer(
        many=True,
        read_only=True,
        source="pokedex",
        help_text="A list of pokédexes that catalogue Pokémon in this region.",
    )
    main_generation = GenerationSummarySerializer(
        read_only=True, source="generation", allow_null=True, help_text="The generation this region was introduced in."
    )

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
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
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
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = GenerationName
        fields = ("name", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=LOCALIZED_NAME_HELP,
        )


class GenerationDetailSerializer(serializers.ModelSerializer[Generation]):
    main_region = RegionSummarySerializer(source="region", help_text="The main region travelled in this generation.")
    names = GenerationNameSerializer(
        many=True,
        read_only=True,
        source="generationname",
        help_text=LOCALIZED_NAMES_HELP,
    )
    abilities = AbilitySummarySerializer(
        many=True,
        read_only=True,
        source="ability",
        help_text="A list of abilities that were introduced in this generation.",
    )
    moves = MoveSummarySerializer(
        many=True, read_only=True, source="move", help_text="A list of moves that were introduced in this generation."
    )
    pokemon_species = PokemonSpeciesSummarySerializer(
        many=True,
        read_only=True,
        source="pokemonspecies",
        help_text="A list of Pokémon species that were introduced in this generation.",
    )
    types = TypeSummarySerializer(
        many=True, read_only=True, source="type", help_text="A list of types that were introduced in this generation."
    )
    version_groups = VersionGroupSummarySerializer(
        many=True,
        read_only=True,
        source="versiongroup",
        help_text="A list of version groups that were introduced in this generation.",
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
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
        )


########################
#  GENDER SERIALIZERS  #
########################


class GenderPokemonSpeciesSerializer(serializers.ModelSerializer[PokemonSpecies]):
    rate = serializers.IntegerField(
        source="gender_rate", help_text="The chance of this Pokémon being female, in eighths; or -1 for genderless."
    )
    pokemon_species = PokemonSpeciesSummarySerializer(
        source="*", help_text="A Pokémon species that can be the referenced gender."
    )

    class Meta:
        model = PokemonSpecies
        fields = ("rate", "pokemon_species")


class GenderDetailSerializer(serializers.ModelSerializer[Gender]):
    pokemon_species_details = serializers.SerializerMethodField(
        "get_species",
        help_text="A list of Pokémon species that can be this gender and how likely it is that they will be.",
    )
    required_for_evolution = serializers.SerializerMethodField(
        "get_required",
        help_text="A list of Pokémon species that required this gender in order for a Pokémon to evolve into them.",
    )

    class Meta:
        model = Gender
        fields = ("id", "name", "pokemon_species_details", "required_for_evolution")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
        )

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
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            level="The level gained.",
            experience="The amount of experience required to reach the referenced level.",
        )


class GrowthRateDescriptionSerializer(serializers.ModelSerializer[GrowthRateDescription]):
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = GrowthRateDescription
        fields = ("description", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            description=LOCALIZED_DESCRIPTION_HELP,
        )


class GrowthRateDetailSerializer(serializers.ModelSerializer[GrowthRate]):
    descriptions = GrowthRateDescriptionSerializer(
        many=True,
        read_only=True,
        source="growthratedescription",
        help_text="The descriptions of this characteristic listed in different languages.",
    )
    levels = ExperienceSerializer(
        many=True,
        read_only=True,
        source="experience",
        help_text="A list of levels and the amount of experienced needed to atain them based on this growth rate.",
    )
    pokemon_species = PokemonSpeciesSummarySerializer(
        many=True,
        read_only=True,
        source="pokemonspecies",
        help_text="A list of Pokémon species that gain levels at this growth rate.",
    )

    class Meta:
        model = GrowthRate
        fields = ("id", "name", "formula", "descriptions", "levels", "pokemon_species")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
            formula="The formula used to calculate the rate at which the Pokémon species gains level.",
        )


##########################
#  LANGUAGE SERIALIZERS  #
##########################


class LanguageNameSerializer(serializers.ModelSerializer[LanguageName]):
    language = LanguageSummarySerializer(source="local_language", help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = LanguageName
        fields = ("name", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=LOCALIZED_NAME_HELP,
        )


class LanguageDetailSerializer(serializers.ModelSerializer[Language]):
    names = LanguageNameSerializer(
        many=True,
        read_only=True,
        source="languagename_language",
        help_text=LOCALIZED_NAMES_HELP,
    )

    class Meta:
        model = Language
        fields = ("id", "name", "official", "iso639", "iso3166", "names")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
            official="Whether or not the games are published in this language.",
            iso639="The two-letter ISO 639-1 language code. Multiple PokéAPI language records may share this code.",
            iso3166="The two-letter ISO 3166-1 alpha-2 code of the country or region associated with this language record. Multiple PokéAPI language records may share this code.",
        )


########################################
#  LOCATION AND ENCOUNTER SERIALIZERS  #
########################################


class EncounterConditionNameSerializer(serializers.ModelSerializer[EncounterConditionName]):
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = EncounterConditionName
        fields = ("name", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=LOCALIZED_NAME_HELP,
        )


class EncounterConditionDetailSerializer(serializers.ModelSerializer[EncounterCondition]):
    names = EncounterConditionNameSerializer(
        many=True,
        read_only=True,
        source="encounterconditionname",
        help_text=LOCALIZED_NAMES_HELP,
    )
    values = EncounterConditionValueSummarySerializer(
        many=True,
        read_only=True,
        source="encounterconditionvalue",
        help_text="A list of possible values for this encounter condition.",
    )

    class Meta:
        model = EncounterCondition
        fields = ("id", "name", "values", "names")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
        )


class EncounterConditionValueNameSerializer(serializers.ModelSerializer[EncounterConditionValueName]):
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = EncounterConditionValueName
        fields = ("name", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=LOCALIZED_NAME_HELP,
        )


class EncounterConditionValueDetailSerializer(serializers.ModelSerializer[EncounterConditionValue]):
    condition = EncounterConditionSummarySerializer(
        source="encounter_condition", help_text="The condition this encounter condition value pertains to."
    )
    names = EncounterConditionValueNameSerializer(
        many=True,
        read_only=True,
        source="encounterconditionvaluename",
        help_text=LOCALIZED_NAMES_HELP,
    )

    class Meta:
        model = EncounterConditionValue
        fields = ("id", "name", "condition", "names")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
        )


class EncounterMethodNameSerializer(serializers.ModelSerializer[EncounterMethodName]):
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = EncounterMethodName
        fields = ("name", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=LOCALIZED_NAME_HELP,
        )


class EncounterMethodDetailSerializer(serializers.ModelSerializer[EncounterMethod]):
    names = EncounterMethodNameSerializer(
        many=True,
        read_only=True,
        source="encountermethodname",
        help_text=LOCALIZED_NAMES_HELP,
    )

    class Meta:
        model = EncounterMethod
        fields = ("id", "name", "order", "names")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
            order="A good value for sorting.",
        )


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
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            min_perfect_ivs="The minimum number of perfect IVs, or null if unspecified.",
            always_shiny="Whether the encountered Pokémon is always shiny.",
            never_shiny="Whether the encountered Pokémon can never be shiny.",
            is_alpha="Whether the encountered Pokémon is an alpha Pokémon.",
        )


class EncounterDetailSerializer(serializers.ModelSerializer[Encounter]):
    version = VersionSummarySerializer()
    location_area = LocationAreaSummarySerializer()
    pokemon = PokemonSummarySerializer()
    condition_values = serializers.SerializerMethodField(
        "get_encounter_conditions",
        help_text="A list of condition values that must be in effect for this encounter to occur.",
    )
    pokemon_details = serializers.SerializerMethodField(
        "get_encounter_pokemon_details",
        help_text="Additional properties of the encountered Pokémon, or null if unspecified.",
    )

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
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            min_level="The lowest level the Pokémon could be encountered at.",
            max_level="The highest level the Pokémon could be encountered at.",
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
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = LocationAreaName
        fields = ("name", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=LOCALIZED_NAME_HELP,
        )


class LocationAreaEncounterVersionDetailSerializer(serializers.Serializer[Any]):
    rate = serializers.IntegerField(help_text="The chance of an encounter to occur.")
    version = VersionSummarySerializer(
        help_text="The version of the game in which the encounter can occur with the given chance."
    )


class LocationAreaEncounterRateSerializer(serializers.Serializer[Any]):
    encounter_method = EncounterMethodSummarySerializer(
        help_text="The method in which Pokémon may be encountered in an area.."
    )
    version_details = LocationAreaEncounterVersionDetailSerializer(
        many=True, help_text="The chance of the encounter to occur on a version of the game."
    )


class LocationAreaEncounterDetailSerializer(serializers.Serializer[Any]):
    min_level = serializers.IntegerField(help_text="The lowest level the Pokémon could be encountered at.")
    max_level = serializers.IntegerField(help_text="The highest level the Pokémon could be encountered at.")
    chance = serializers.IntegerField(
        source="encounter_slot.rarity", default=0, help_text="Percent chance that this encounter will occur."
    )
    method = EncounterMethodSummarySerializer(
        source="encounter_slot.encounter_method", default=None, help_text="The method by which this encounter happens."
    )
    condition_values = serializers.SerializerMethodField(
        "get_encounter_conditions",
        help_text="A list of condition values that must be in effect for this encounter to occur.",
    )
    pokemon_details = serializers.SerializerMethodField(
        "get_encounter_pokemon_details",
        help_text="Additional properties of the encountered Pokémon, or null if unspecified.",
    )

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
    version = VersionSummarySerializer(help_text="The game version this encounter happens in.")
    max_chance = serializers.IntegerField(help_text="The total percentage of all encounter potential.")
    encounter_details = LocationAreaEncounterDetailSerializer(
        many=True, help_text="A list of encounters and their specifics."
    )


class LocationAreaPokemonEncounterSerializer(serializers.Serializer[Any]):
    pokemon = PokemonSummarySerializer(help_text="The Pokémon being encountered.")
    version_details = LocationAreaPokemonEncounterVersionSerializer(
        many=True,
        help_text="A list of versions and encounters with Pokémon that might happen in the referenced location area.",
    )


class LocationAreaDetailSerializer(serializers.ModelSerializer[LocationArea]):
    location = LocationSummarySerializer(help_text="The region this location area can be found in.")
    encounter_method_rates = serializers.SerializerMethodField(
        "get_method_rates",
        help_text="A list of methods in which Pokémon may be encountered in this area and how likely the method will occur depending on the version of the game.",
    )
    pokemon_encounters = serializers.SerializerMethodField(
        "get_encounters",
        help_text="A list of Pokémon that can be encountered in this area along with version specific details about the encounter.",
    )
    names = LocationAreaNameSerializer(
        many=True,
        read_only=True,
        source="locationareaname",
        help_text=LOCALIZED_NAMES_HELP,
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
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
            game_index=GAME_INDEX_HELP,
        )

    @extend_schema_field(LocationAreaEncounterRateSerializer(many=True))
    def get_method_rates(self, obj: LocationAreaEncounterRate) -> ReturnList[ReturnDict[str, Any]]:
        # Get encounters related to this area and pull out unique encounter methods
        rates = (
            LocationAreaEncounterRate.objects.filter(location_area=obj, encounter_method__isnull=False)
            .select_related("encounter_method", "version")
            .order_by("encounter_method_id", "version_id", "pk")
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
            .order_by("pokemon_id", "version_id", "encounter_slot_id", "pk")
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
    generation = GenerationSummarySerializer(help_text=GAME_INDEX_GENERATION_HELP)

    class Meta:
        model = LocationGameIndex
        fields = ("game_index", "generation")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            game_index=GAME_INDEX_HELP,
        )


class LocationNameSerializer(serializers.ModelSerializer[LocationName]):
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = LocationName
        fields = ("name", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=LOCALIZED_NAME_HELP,
        )


class LocationDetailSerializer(serializers.ModelSerializer[Location]):
    region = RegionSummarySerializer(allow_null=True, help_text="The region this location can be found in.")
    names = LocationNameSerializer(
        many=True,
        read_only=True,
        source="locationname",
        help_text=LOCALIZED_NAMES_HELP,
    )
    game_indices = LocationGameIndexSerializer(
        many=True,
        read_only=True,
        source="locationgameindex",
        help_text="A list of game indices relevent to this location by generation.",
    )
    areas = LocationAreaSummarySerializer(
        many=True, read_only=True, source="locationarea", help_text="Areas that can be found within this location."
    )

    class Meta:
        model = Location
        fields = ("id", "name", "region", "names", "game_indices", "areas")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
        )


#########################
#  ABILITY SERIALIZERS  #
#########################


class AbilityEffectTextSerializer(serializers.ModelSerializer[AbilityEffectText]):
    language = LanguageSummarySerializer(help_text=EFFECT_LANGUAGE_HELP)

    class Meta:
        model = AbilityEffectText
        fields = ("effect", "short_effect", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            effect=LOCALIZED_EFFECT_HELP,
            short_effect=LOCALIZED_SHORT_EFFECT_HELP,
        )


class AbilityFlavorTextSerializer(serializers.ModelSerializer[AbilityFlavorText]):
    flavor_text = serializers.CharField(help_text="The localized name for an API resource in a specific language.")
    language = LanguageSummarySerializer(help_text="The language this text resource is in.")
    version_group = VersionGroupSummarySerializer(help_text="The version group that uses this flavor text.")

    class Meta:
        model = AbilityFlavorText
        fields = ("flavor_text", "language", "version_group")


class AbilityChangeEffectTextSerializer(serializers.ModelSerializer[AbilityChangeEffectText]):
    language = LanguageSummarySerializer(help_text=EFFECT_LANGUAGE_HELP)

    class Meta:
        model = AbilityChangeEffectText
        fields = (
            "effect",
            "language",
        )
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            effect=LOCALIZED_EFFECT_HELP,
        )


class AbilityChangeSerializer(serializers.ModelSerializer[AbilityChange]):
    version_group = VersionGroupSummarySerializer(
        help_text="The version group in which the previous effect of this ability originated."
    )
    effect_entries = AbilityChangeEffectTextSerializer(
        many=True,
        read_only=True,
        source="abilitychangeeffecttext",
        help_text="The previous effect of this ability listed in different languages.",
    )

    class Meta:
        model = AbilityChange
        fields = ("version_group", "effect_entries")


class AbilityNameSerializer(serializers.ModelSerializer[AbilityName]):
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = AbilityName
        fields = ("name", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=LOCALIZED_NAME_HELP,
        )


class AbilityPokemonDetailSerializer(serializers.ModelSerializer[PokemonAbility]):
    pokemon = PokemonSummarySerializer(help_text="The Pokémon this ability could belong to.")

    class Meta:
        model = PokemonAbility
        fields = ("is_hidden", "slot", "pokemon")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            is_hidden="Whether or not this a hidden ability for the referenced Pokémon.",
            slot="Pokémon have 3 ability 'slots' which hold references to possible abilities they could have. This is the slot of this ability for the referenced pokemon.",
        )


class AbilityDetailSerializer(serializers.ModelSerializer[Ability]):
    effect_entries = AbilityEffectTextSerializer(
        many=True,
        read_only=True,
        source="abilityeffecttext",
        help_text="The effect of this ability listed in different languages.",
    )
    flavor_text_entries = AbilityFlavorTextSerializer(
        many=True,
        read_only=True,
        source="abilityflavortext",
        help_text="The flavor text of this ability listed in different languages.",
    )
    names = AbilityNameSerializer(
        many=True,
        read_only=True,
        source="abilityname",
        help_text=LOCALIZED_NAMES_HELP,
    )
    generation = GenerationSummarySerializer(help_text="The generation this ability originated in.")
    effect_changes = AbilityChangeSerializer(
        many=True,
        read_only=True,
        source="abilitychange",
        help_text="The list of previous effects this ability has had across version groups.",
    )
    pokemon = serializers.SerializerMethodField(
        "get_ability_pokemon", help_text="A list of Pokémon that could potentially have this ability."
    )

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
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
            is_main_series="Whether or not this ability originated in the main series of the video games.",
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
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = StatName
        fields = ("name", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=LOCALIZED_NAME_HELP,
        )


class MoveStatChangeSerializer(serializers.ModelSerializer[MoveMetaStatChange]):
    move = MoveSummarySerializer(help_text="The move causing the change.")

    class Meta:
        model = MoveMetaStatChange
        fields = ("change", "move")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            change="The maximum amount of change to the referenced stat.",
        )


class StatAffectingMovesSerializer(serializers.Serializer[Any]):
    increase = MoveStatChangeSerializer(many=True, help_text="A list of moves and how they change the referenced stat.")
    decrease = MoveStatChangeSerializer(many=True, help_text="A list of moves and how they change the referenced stat.")


class StatAffectingNaturesSerializer(serializers.Serializer[Any]):
    increase = NatureSummarySerializer(
        many=True, help_text="A list of natures and how they change the referenced stat."
    )
    decrease = NatureSummarySerializer(
        many=True, help_text="A list of nature sand how they change the referenced stat."
    )


class StatDetailSerializer(serializers.ModelSerializer[Stat]):
    names = StatNameSerializer(
        many=True,
        read_only=True,
        source="statname",
        help_text=LOCALIZED_NAMES_HELP,
    )
    move_damage_class = MoveDamageClassSummarySerializer(
        allow_null=True, help_text="The class of damage this stat is directly related to."
    )
    characteristics = CharacteristicSummarySerializer(
        many=True,
        read_only=True,
        source="characteristic",
        help_text="A list of characteristics that are set on a Pokémon when its highest base stat is this stat.",
    )
    affecting_moves = serializers.SerializerMethodField(
        "get_moves_that_affect", help_text="A detail of moves which affect this stat positively or negatively."
    )
    affecting_natures = serializers.SerializerMethodField(
        "get_natures_that_affect", help_text="A detail of natures which affect this stat positively or negatively."
    )
    affecting_items = serializers.SerializerMethodField(
        "get_items_that_affect", help_text="Items that affect this stat, such as vitamins and battle items."
    )

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
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
            game_index="ID the games use for this stat.",
            is_battle_only="Whether this stat only exists within a battle.",
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
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = ItemPocketName
        fields = ("name", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=LOCALIZED_NAME_HELP,
        )


class ItemPocketDetailSerializer(serializers.ModelSerializer[ItemPocket]):
    names = ItemPocketNameSerializer(
        many=True,
        read_only=True,
        source="itempocketname",
        help_text=LOCALIZED_NAMES_HELP,
    )
    categories = ItemCategorySummarySerializer(
        many=True,
        read_only=True,
        source="itemcategory",
        help_text="A list of item categories that are relevant to this item pocket.",
    )

    class Meta:
        model = ItemPocket
        fields = ("id", "name", "categories", "categories", "names")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
        )


###############################
#  ITEM CATEGORY SERIALIZERS  #
###############################


class ItemCategoryNameSerializer(serializers.ModelSerializer[ItemCategoryName]):
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = ItemCategoryName
        fields = ("name", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=LOCALIZED_NAME_HELP,
        )


class ItemCategoryDetailSerializer(serializers.ModelSerializer[ItemCategory]):
    names = ItemCategoryNameSerializer(
        many=True,
        read_only=True,
        source="itemcategoryname",
        help_text="The name of this item category listed in different languages.",
    )
    pocket = ItemPocketSummarySerializer(
        source="item_pocket", help_text="The pocket items in this category would be put in."
    )
    items = ItemSummarySerializer(
        many=True, read_only=True, source="item", help_text="A list of items that are a part of this category."
    )

    class Meta:
        model = ItemCategory
        fields = ("id", "name", "items", "names", "pocket")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
        )


################################
#  ITEM ATTRIBUTE SERIALIZERS  #
################################


class ItemAttributeNameSerializer(serializers.ModelSerializer[ItemAttributeName]):
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = ItemAttributeName
        fields = ("name", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=LOCALIZED_NAME_HELP,
        )


class ItemAttributeDescriptionSerializer(serializers.ModelSerializer[ItemAttributeDescription]):
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = ItemAttributeDescription
        fields = ("description", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            description=LOCALIZED_DESCRIPTION_HELP,
        )


class ItemAttributeDetailSerializer(serializers.ModelSerializer[ItemAttribute]):
    names = ItemAttributeNameSerializer(
        many=True,
        read_only=True,
        source="itemattributename",
        help_text="The name of this item attribute listed in different languages.",
    )
    descriptions = ItemAttributeDescriptionSerializer(
        many=True,
        read_only=True,
        source="itemattributedescription",
        help_text="The description of this item attribute listed in different languages.",
    )
    items = serializers.SerializerMethodField(
        "get_attribute_items", help_text="A list of items that have this attribute."
    )

    class Meta:
        model = ItemAttribute
        fields = ("id", "name", "descriptions", "items", "names")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
        )

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
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = CurrencyName
        fields = ("name", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=LOCALIZED_NAME_HELP,
        )


class CurrencyDetailSerializer(serializers.ModelSerializer[Currency]):
    names = CurrencyNameSerializer(
        many=True,
        read_only=True,
        source="currencyname",
        help_text=LOCALIZED_NAMES_HELP,
    )

    class Meta:
        model = Currency
        fields = ("id", "name", "names")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
        )


###################################
#  ITEM FLING EFFECT SERIALIZERS  #
###################################


class ItemFlingEffectEffectTextSerializer(serializers.ModelSerializer[ItemFlingEffectEffectText]):
    language = LanguageSummarySerializer(help_text=EFFECT_LANGUAGE_HELP)

    class Meta:
        model = ItemFlingEffectEffectText
        fields = ("effect", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            effect=LOCALIZED_EFFECT_HELP,
        )


class ItemFlingEffectDetailSerializer(serializers.ModelSerializer[ItemFlingEffect]):
    effect_entries = ItemFlingEffectEffectTextSerializer(
        many=True,
        read_only=True,
        source="itemflingeffecteffecttext",
        help_text="The result of this fling effect listed in different languages.",
    )
    items = ItemSummarySerializer(
        many=True, read_only=True, source="item", help_text="A list of items that have this fling effect."
    )

    class Meta:
        model = ItemFlingEffect
        fields = ("id", "name", "effect_entries", "items")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
        )


#######################
#  ITEM  SERIALIZERS  #
#######################


class ItemFlavorTextSerializer(serializers.ModelSerializer[ItemFlavorText]):
    text = serializers.CharField(source="flavor_text", help_text=LOCALIZED_FLAVOR_TEXT_HELP)
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)
    version_group = VersionGroupSummarySerializer(help_text="The version group which uses this flavor text.")

    class Meta:
        model = ItemFlavorText
        fields = ("text", "version_group", "language")


class ItemEffectTextSerializer(serializers.ModelSerializer[ItemEffectText]):
    language = LanguageSummarySerializer(help_text=EFFECT_LANGUAGE_HELP)

    class Meta:
        model = ItemEffectText
        fields = ("effect", "short_effect", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            effect=LOCALIZED_EFFECT_HELP,
            short_effect=LOCALIZED_SHORT_EFFECT_HELP,
        )


class ItemGameIndexSerializer(serializers.ModelSerializer[ItemGameIndex]):
    generation = GenerationSummarySerializer(help_text=GAME_INDEX_GENERATION_HELP)

    class Meta:
        model = ItemGameIndex
        fields = ("game_index", "generation")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            game_index=GAME_INDEX_HELP,
        )


class ItemPriceSerializer(serializers.ModelSerializer[ItemPrice]):
    currency = CurrencySummarySerializer(help_text="The currency used for this price.")
    version_group = VersionGroupSummarySerializer(help_text="The version group to which this price applies.")

    class Meta:
        model = ItemPrice
        fields = (
            "purchase_price",
            "sell_price",
            "currency",
            "version_group",
        )
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            purchase_price="The purchase price in this currency and version group, or null if unavailable.",
            sell_price="The sell price in this currency and version group, or null if unavailable.",
        )


class ItemNameSerializer(serializers.ModelSerializer[ItemName]):
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = ItemName
        fields = ("name", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=LOCALIZED_NAME_HELP,
        )


class ItemSpritesSerializer(serializers.Serializer[Any]):
    default = serializers.CharField(allow_null=True, help_text="The default depiction of this item.")


class PokemonHeldItemVersionSerializer(serializers.Serializer[Any]):
    rarity = serializers.IntegerField(help_text="How often the item is held.")
    version = VersionSummarySerializer(help_text="The version in which the item is held.")


class PokemonHeldItemSerializer(serializers.Serializer[Any]):
    pokemon = PokemonSummarySerializer(help_text="The Pokémon that holds this item.")
    version_details = PokemonHeldItemVersionSerializer(
        many=True, help_text="The details for the version that this item is held in by the Pokémon."
    )


class PokemonHeldItemSummarySerializer(serializers.Serializer[Any]):
    item = ItemSummarySerializer(help_text="The item the referenced Pokémon holds.")
    version_details = PokemonHeldItemVersionSerializer(
        many=True, help_text="The details of the different versions in which the item is held."
    )


class ItemMachineSerializer(serializers.ModelSerializer[Machine]):
    machine = MachineSummarySerializer(source="*", help_text="The machine that teaches a move from an item.")
    version_group = VersionGroupSummarySerializer(help_text="The version group of this specific machine.")

    class Meta:
        model = Machine
        fields = ("machine", "version_group")


class ItemDetailSerializer(serializers.ModelSerializer[Item]):
    names = ItemNameSerializer(
        many=True, read_only=True, source="itemname", help_text="The name of this item listed in different languages."
    )
    game_indices = ItemGameIndexSerializer(
        many=True,
        read_only=True,
        source="itemgameindex",
        help_text="A list of game indices relevent to this item by generation.",
    )
    prices = ItemPriceSerializer(
        many=True,
        read_only=True,
        source="itemprice",
        help_text="Purchase and sell prices by currency and version group. Prices may be null when the item cannot be bought or sold.",
    )
    effect_entries = ItemEffectTextSerializer(
        many=True,
        read_only=True,
        source="itemeffecttext",
        help_text="The effect of this ability listed in different languages.",
    )
    flavor_text_entries = ItemFlavorTextSerializer(
        many=True,
        read_only=True,
        source="itemflavortext",
        help_text="The flavor text of this ability listed in different languages.",
    )
    category = ItemCategorySummarySerializer(
        source="item_category", help_text="The category of items this item falls into."
    )
    attributes = serializers.SerializerMethodField(
        "get_item_attributes", help_text="A list of attributes this item has."
    )
    fling_effect = ItemFlingEffectSummarySerializer(
        source="item_fling_effect", allow_null=True, help_text="The effect of the move Fling when used with this item."
    )
    held_by_pokemon = serializers.SerializerMethodField(
        "get_held_by_pokemon", help_text="A list of Pokémon that might be found in the wild holding this item."
    )
    baby_trigger_for = serializers.SerializerMethodField(
        "get_baby_trigger_for", help_text="An evolution chain this item requires to produce a bay during mating."
    )
    sprites = serializers.SerializerMethodField(
        "get_item_sprites", help_text="A set of sprites used to depict this item in the game."
    )
    machines = serializers.SerializerMethodField(
        "get_item_machines", help_text="A list of the machines related to this item."
    )

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
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
            fling_power="The power of the move Fling when used with this item.",
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
            .order_by("pokemon_id", "version_id", "pk")
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
    move_battle_style = MoveBattleStyleSummarySerializer(help_text="The move battle style.")

    class Meta:
        model = NatureBattleStylePreference
        fields = (
            "low_hp_preference",
            "high_hp_preference",
            "move_battle_style",
        )
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            low_hp_preference="Chance of using the move, in percent, if HP is under one half.",
            high_hp_preference="Chance of using the move, in percent, if HP is over one half.",
        )


class NatureNameSerializer(serializers.ModelSerializer[NatureName]):
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = NatureName
        fields = ("name", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=LOCALIZED_NAME_HELP,
        )


class NaturePokeathlonStatSerializer(serializers.ModelSerializer[NaturePokeathlonStat]):
    pokeathlon_stat = PokeathlonStatSummarySerializer(help_text="The stat being affected.")

    class Meta:
        model = NaturePokeathlonStat
        fields = ("max_change", "pokeathlon_stat")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            max_change="The amount of change.",
        )


class NatureDetailSerializer(serializers.ModelSerializer[Nature]):
    names = NatureNameSerializer(
        many=True,
        read_only=True,
        source="naturename",
        help_text=LOCALIZED_NAMES_HELP,
    )
    decreased_stat = StatSummarySerializer(
        allow_null=True, help_text="The stat decreased by 10% in Pokémon with this nature."
    )
    increased_stat = StatSummarySerializer(
        allow_null=True, help_text="The stat increased by 10% in Pokémon with this nature."
    )
    likes_flavor = BerryFlavorSummarySerializer(
        allow_null=True, help_text="The flavor liked by Pokémon with this nature."
    )
    hates_flavor = BerryFlavorSummarySerializer(
        allow_null=True, help_text="The flavor hated by Pokémon with this nature."
    )
    pokeathlon_stat_changes = serializers.SerializerMethodField(
        "get_pokeathlon_stats", help_text="A list of Pokéathlon stats this nature effects and how much it effects them."
    )
    move_battle_style_preferences = NatureBattleStylePreferenceSerializer(
        many=True,
        read_only=True,
        source="naturebattlestylepreference",
        help_text="A list of battle styles and how likely a Pokémon with this nature is to use them in the Battle Palace or Battle Tent.",
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
            "pokeathlon_stat_changes",
            "move_battle_style_preferences",
            "names",
        )
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
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
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = BerryFirmnessName
        fields = ("name", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=LOCALIZED_NAME_HELP,
        )


class BerryFirmnessDetailSerializer(serializers.ModelSerializer[BerryFirmness]):
    names = BerryFirmnessNameSerializer(
        many=True,
        read_only=True,
        source="berryfirmnessname",
        help_text=LOCALIZED_NAMES_HELP,
    )
    berries = BerrySummarySerializer(
        many=True, read_only=True, source="berry", help_text="A list of the berries with this firmness."
    )

    class Meta:
        model = BerryFirmness
        fields = ("id", "name", "berries", "names")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
        )


class BerryFlavorNameSerializer(serializers.ModelSerializer[BerryFlavorName]):
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = BerryFlavorName
        fields = ("name", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=LOCALIZED_NAME_HELP,
        )


class BerryFlavorBerryMapSerializer(serializers.ModelSerializer[BerryFlavorMap]):
    berry = BerrySummarySerializer(help_text="The berry with the referenced flavor.")

    class Meta:
        model = BerryFlavorMap
        fields = ("potency", "berry")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            potency=BERRY_FLAVOR_POTENCY_HELP,
        )


class BerryFlavorDetailSerializer(serializers.ModelSerializer[BerryFlavor]):
    names = BerryFlavorNameSerializer(
        many=True,
        read_only=True,
        source="berryflavorname",
        help_text=LOCALIZED_NAMES_HELP,
    )
    contest_type = ContestTypeSummarySerializer(help_text="The contest type that correlates with this berry flavor.")
    berries = serializers.SerializerMethodField(
        "get_berries_with_flavor", help_text="A list of the berries with this flavor."
    )

    class Meta:
        model = BerryFlavor
        fields = ("id", "name", "berries", "contest_type", "names")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
        )

    @extend_schema_field(BerryFlavorBerryMapSerializer(many=True))
    def get_berries_with_flavor(self, obj: BerryFlavor) -> ReturnList[ReturnDict[str, Any]]:
        flavor_map_objects = (
            BerryFlavorMap.objects.filter(berry_flavor=obj, potency__gt=0)
            .select_related("berry")
            .order_by("potency", "berry_id", "pk")
        )
        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            BerryFlavorBerryMapSerializer(flavor_map_objects, many=True, context=self.context).data,
        )


class BerryFlavorMapSerializer(serializers.ModelSerializer[BerryFlavorMap]):
    flavor = BerryFlavorSummarySerializer(source="berry_flavor", help_text="The referenced berry flavor.")

    class Meta:
        model = BerryFlavorMap
        fields = ("potency", "flavor")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            potency=BERRY_FLAVOR_POTENCY_HELP,
        )


class BerryDetailSerializer(serializers.ModelSerializer[Berry]):
    item = ItemSummarySerializer(
        help_text="Berries are actually items. This is a reference to the item specific data for this berry."
    )
    natural_gift_type = TypeSummarySerializer(
        allow_null=True, help_text='The type inherited by "Natural Gift" when used with this Berry.'
    )
    firmness = BerryFirmnessSummarySerializer(
        source="berry_firmness",
        allow_null=True,
        help_text="The firmness of this berry, used in making Pokéblocks or Poffins.",
    )
    flavors = serializers.SerializerMethodField(
        "get_berry_flavors",
        help_text="A list of references to each flavor a berry can have and the potency of each of those flavors in regard to this berry.",
    )

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
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
            growth_time="Time it takes the tree to grow one stage, in hours. Berry trees go through four of these growth stages before they can be picked.",
            max_harvest="The maximum number of these berries that can grow on one tree in Generation IV.",
            natural_gift_power='The power of the move "Natural Gift" when used with this Berry.',
            size="The size of this Berry, in millimeters.",
            smoothness="The smoothness of this Berry, used in making Pokéblocks or Poffins.",
            soil_dryness="The speed at which this Berry dries out the soil as it grows. A higher rate means the soil dries more quickly.",
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
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = EggGroupName
        fields = ("name", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=LOCALIZED_NAME_HELP,
        )


class EggGroupDetailSerializer(serializers.ModelSerializer[EggGroup]):
    names = EggGroupNameSerializer(
        many=True,
        read_only=True,
        source="egggroupname",
        help_text=LOCALIZED_NAMES_HELP,
    )
    pokemon_species = serializers.SerializerMethodField(
        "get_species", help_text="A list of all Pokémon species that are members of this egg group."
    )

    class Meta:
        model = EggGroup
        fields = ("id", "name", "names", "pokemon_species")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
        )

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
    generation = GenerationSummarySerializer(help_text=GAME_INDEX_GENERATION_HELP)

    class Meta:
        model = TypeGameIndex
        fields = ("game_index", "generation")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            game_index=GAME_INDEX_HELP,
        )


class TypeNameSerializer(serializers.ModelSerializer[TypeName]):
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = TypeName
        fields = ("name", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=LOCALIZED_NAME_HELP,
        )


class TypeGameSpriteSerializer(serializers.Serializer[Any]):
    name_icon = serializers.CharField(
        allow_null=True,
        required=False,
        help_text="The URL of the icon displaying the type name in this game, or null if unavailable.",
    )
    symbol_icon = serializers.CharField(
        allow_null=True,
        required=False,
        help_text="The URL of the type symbol icon in this game, or null if unavailable.",
    )


class TypeRelationshipsSerializer(serializers.Serializer[Any]):
    no_damage_to = TypeSummarySerializer(many=True, help_text="A list of types this type has no effect on.")
    half_damage_to = TypeSummarySerializer(many=True, help_text="A list of types this type is not very effect against.")
    double_damage_to = TypeSummarySerializer(many=True, help_text="A list of types this type is very effect against.")
    no_damage_from = TypeSummarySerializer(many=True, help_text="A list of types that have no effect on this type.")
    half_damage_from = TypeSummarySerializer(
        many=True, help_text="A list of types that are not very effective against this type."
    )
    double_damage_from = TypeSummarySerializer(
        many=True, help_text="A list of types that are very effective against this type."
    )


class TypePastRelationshipsSerializer(serializers.Serializer[Any]):
    generation = GenerationSummarySerializer(
        help_text="The last generation in which the referenced type had the listed damage relations"
    )
    damage_relations = TypeRelationshipsSerializer(
        help_text="The damage relations the referenced type had up to and including the listed generation"
    )


class TypePokemonSerializer(serializers.ModelSerializer[PokemonType]):
    pokemon = PokemonSummarySerializer(help_text="The Pokémon that has the referenced type.")

    class Meta:
        model = PokemonType
        fields = ("slot", "pokemon")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            slot=POKEMON_TYPE_SLOT_HELP,
        )


class TypeDetailSerializer(serializers.ModelSerializer[Type]):
    """
    Serializer for the Type resource
    """

    generation = GenerationSummarySerializer(help_text="The generation this type was introduced in.")
    names = TypeNameSerializer(
        many=True,
        read_only=True,
        source="typename",
        help_text=LOCALIZED_NAMES_HELP,
    )
    game_indices = TypeGameIndexSerializer(
        many=True,
        read_only=True,
        source="typegameindex",
        help_text="A list of game indices relevent to this item by generation.",
    )
    move_damage_class = MoveDamageClassSummarySerializer(
        allow_null=True, help_text="The class of damage inflicted by this type."
    )
    damage_relations = serializers.SerializerMethodField(
        "get_type_relationships", help_text="A detail of how effective this type is toward others and vice versa."
    )
    past_damage_relations = serializers.SerializerMethodField(
        "get_type_past_relationships",
        help_text="A list of details of how effective this type was toward others and vice versa in previous generations",
    )
    pokemon = serializers.SerializerMethodField(
        "get_type_pokemon", help_text="A list of details of Pokémon that have this type."
    )
    moves = MoveSummarySerializer(
        many=True, read_only=True, source="move", help_text="A list of moves that have this type."
    )
    sprites = serializers.SerializerMethodField(
        "get_type_sprites",
        help_text="Type icons grouped by generation and game, with name_icon and symbol_icon URLs. Unavailable icons are null.",
    )

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
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
        )

    @extend_schema_field(serializers.DictField(child=serializers.DictField(child=TypeGameSpriteSerializer())))
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
    item = ItemSummarySerializer(help_text="The TM or HM item that corresponds to this machine.")
    version_group = VersionGroupSummarySerializer(help_text="The version group that this machine applies to.")
    move = MoveSummarySerializer(help_text="The move that is taught by this machine.")

    class Meta:
        model = Machine
        fields = ("id", "item", "version_group", "move")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
        )


###################################
#  MOVE BATTLE STYLE SERIALIZERS  #
###################################


class MoveBattleStyleNameSerializer(serializers.ModelSerializer[MoveBattleStyleName]):
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = MoveBattleStyleName
        fields = ("name", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=LOCALIZED_NAME_HELP,
        )


class MoveBattleStyleDetailSerializer(serializers.ModelSerializer[MoveBattleStyle]):
    names = MoveBattleStyleNameSerializer(
        many=True,
        read_only=True,
        source="movebattlestylename",
        help_text=LOCALIZED_NAMES_HELP,
    )

    class Meta:
        model = MoveBattleStyle
        fields = ("id", "name", "names")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
        )


###################################
#  MOVE DAMAGE CLASS SERIALIZERS  #
###################################


class MoveDamageClassNameSerializer(serializers.ModelSerializer[MoveDamageClassName]):
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = MoveDamageClassName
        fields = ("name", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=LOCALIZED_NAME_HELP,
        )


class MoveDamageClassDescriptionSerializer(serializers.ModelSerializer[MoveDamageClassDescription]):
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = MoveDamageClassDescription
        fields = ("description", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            description=LOCALIZED_DESCRIPTION_HELP,
        )


class MoveDamageClassDetailSerializer(serializers.ModelSerializer[MoveDamageClass]):
    names = MoveDamageClassNameSerializer(
        many=True,
        read_only=True,
        source="movedamageclassname",
        help_text=LOCALIZED_NAMES_HELP,
    )
    descriptions = MoveDamageClassDescriptionSerializer(
        many=True,
        read_only=True,
        source="movedamageclassdescription",
        help_text=LOCALIZED_DESCRIPTIONS_HELP,
    )
    moves = MoveSummarySerializer(
        many=True, read_only=True, source="move", help_text="A list of moves that fall into this damage class."
    )

    class Meta:
        model = MoveDamageClass
        fields = (
            "id",
            "name",
            "descriptions",
            "moves",
            "names",
        )
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
        )


###########################
#  MOVE META SERIALIZERS  #
###########################


class MoveMetaAilmentNameSerializer(serializers.ModelSerializer[MoveMetaAilmentName]):
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = MoveMetaAilmentName
        fields = ("name", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=LOCALIZED_NAME_HELP,
        )


class MoveMetaAilmentDetailSerializer(serializers.ModelSerializer[MoveMetaAilment]):
    names = MoveMetaAilmentNameSerializer(
        many=True,
        read_only=True,
        source="movemetaailmentname",
        help_text=LOCALIZED_NAMES_HELP,
    )
    moves = serializers.SerializerMethodField("get_ailment_moves", help_text="A list of moves that cause this ailment.")

    class Meta:
        model = MoveMetaAilment
        fields = ("id", "name", "moves", "names")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
        )

    @extend_schema_field(MoveSummarySerializer(many=True))
    def get_ailment_moves(self, obj: MoveMetaAilment) -> ReturnList[ReturnDict[str, Any]]:
        moves = Move.objects.filter(movemeta__move_meta_ailment=obj)
        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            MoveSummarySerializer(moves, many=True, context=self.context).data,
        )


class MoveMetaCategoryDescriptionSerializer(serializers.ModelSerializer[MoveMetaCategoryDescription]):
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = MoveMetaCategoryDescription
        fields = ("description", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            description=LOCALIZED_DESCRIPTION_HELP,
        )


class MoveMetaCategoryDetailSerializer(serializers.ModelSerializer[MoveMetaCategory]):
    descriptions = MoveMetaCategoryDescriptionSerializer(
        many=True,
        read_only=True,
        source="movemetacategorydescription",
        help_text=LOCALIZED_DESCRIPTIONS_HELP,
    )
    moves = serializers.SerializerMethodField(
        "get_category_moves", help_text="A list of moves that fall into this category."
    )

    class Meta:
        model = MoveMetaCategory
        fields = ("id", "name", "descriptions", "moves")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
        )

    @extend_schema_field(MoveSummarySerializer(many=True))
    def get_category_moves(self, obj: MoveMetaCategory) -> ReturnList[ReturnDict[str, Any]]:
        moves = Move.objects.filter(movemeta__move_meta_category=obj)
        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            MoveSummarySerializer(moves, many=True, context=self.context).data,
        )


class MoveMetaSerializer(serializers.ModelSerializer[MoveMeta]):
    ailment = MoveMetaAilmentSummarySerializer(
        source="move_meta_ailment", help_text="The status ailment this move inflicts on its target."
    )
    category = MoveMetaCategorySummarySerializer(
        source="move_meta_category", help_text="The category of move this move falls under, e.g. damage or ailment."
    )

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
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            min_hits="The minimum number of times this move hits. Null if it always only hits once.",
            max_hits="The maximum number of times this move hits. Null if it always only hits once.",
            min_turns="The minimum number of turns this move continues to take effect. Null if it always only lasts one turn.",
            max_turns="The maximum number of turns this move continues to take effect. Null if it always only lasts one turn.",
            drain="HP drain (if positive) or Recoil damage (if negative), in percent of damage done.",
            healing="The amount of hp gained by the attacking Pokemon, in percent of it's maximum HP.",
            crit_rate="Critical hit rate bonus.",
            ailment_chance="The likelihood this attack will cause an ailment.",
            flinch_chance="The likelihood this attack will cause the target Pokémon to flinch.",
            stat_chance="The likelihood this attack will cause a stat change in the target Pokémon.",
        )


#############################
#  MOVE TARGET SERIALIZERS  #
#############################


class MoveTargetNameSerializer(serializers.ModelSerializer[MoveTargetName]):
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = MoveTargetName
        fields = ("name", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=LOCALIZED_NAME_HELP,
        )


class MoveTargetDescriptionSerializer(serializers.ModelSerializer[MoveTargetDescription]):
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = MoveTargetDescription
        fields = ("description", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            description=LOCALIZED_DESCRIPTION_HELP,
        )


class MoveTargetDetailSerializer(serializers.ModelSerializer[MoveTarget]):
    names = MoveTargetNameSerializer(
        many=True,
        read_only=True,
        source="movetargetname",
        help_text=LOCALIZED_NAMES_HELP,
    )
    descriptions = MoveTargetDescriptionSerializer(
        many=True,
        read_only=True,
        source="movetargetdescription",
        help_text=LOCALIZED_DESCRIPTIONS_HELP,
    )
    moves = MoveSummarySerializer(
        many=True, read_only=True, source="move", help_text="A list of moves that that are directed at this target."
    )

    class Meta:
        model = MoveTarget
        fields = ("id", "name", "descriptions", "moves", "names")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
        )


######################
#  MOVE SERIALIZERS  #
######################


class MoveNameSerializer(serializers.ModelSerializer[MoveName]):
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = MoveName
        fields = ("name", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=LOCALIZED_NAME_HELP,
        )


class MoveEffectEffectTextSerializer(serializers.ModelSerializer[MoveEffectEffectText]):
    language = LanguageSummarySerializer(help_text=EFFECT_LANGUAGE_HELP)

    class Meta:
        model = MoveEffectEffectText
        fields = ("effect", "short_effect", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            effect=LOCALIZED_EFFECT_HELP,
            short_effect=LOCALIZED_SHORT_EFFECT_HELP,
        )


class MoveChangeSerializer(serializers.ModelSerializer[MoveChange]):
    version_group = VersionGroupSummarySerializer(
        help_text="The version group in which these move stat values were in effect."
    )
    type = TypeSummarySerializer(allow_null=True, help_text="The elemental type of this move.")
    effect_entries = serializers.SerializerMethodField(
        "get_effects", help_text="The effect of this move listed in different languages."
    )
    effect_chance = serializers.IntegerField(
        source="move_effect_chance",
        allow_null=True,
        help_text="The percent value of how likely it is this moves effect will take effect.",
    )

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
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            accuracy=MOVE_ACCURACY_HELP,
            power="The base power before the listed version group, or null if power did not change.",
            pp=MOVE_PP_HELP,
        )

    @extend_schema_field(MoveEffectEffectTextSerializer(many=True))
    def get_effects(self, obj: MoveChange) -> ReturnList[ReturnDict[str, Any]]:
        effect_texts = MoveEffectEffectText.objects.filter(move_effect=obj.move_effect).select_related("language")
        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            MoveEffectEffectTextSerializer(effect_texts, many=True, context=self.context).data,
        )


class MoveEffectChangeEffectTextSerializer(serializers.ModelSerializer[MoveEffectChangeEffectText]):
    language = LanguageSummarySerializer(help_text=EFFECT_LANGUAGE_HELP)

    class Meta:
        model = MoveEffectChangeEffectText
        fields = ("effect", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            effect=LOCALIZED_EFFECT_HELP,
        )


class MoveEffectChangeSerializer(serializers.ModelSerializer[MoveEffectChange]):
    version_group = VersionGroupSummarySerializer(
        help_text="The version group in which the previous effect of this ability originated."
    )
    effect_entries = MoveEffectChangeEffectTextSerializer(
        many=True,
        read_only=True,
        source="moveeffectchangeeffecttext",
        help_text="The previous effect of this ability listed in different languages.",
    )

    class Meta:
        model = MoveEffectChange
        fields = ("version_group", "effect_entries")


class MoveFlavorTextSerializer(serializers.ModelSerializer[MoveFlavorText]):
    flavor_text = serializers.CharField(
        help_text="The localized flavor text for an api resource in a specific language."
    )
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)
    version_group = VersionGroupSummarySerializer(help_text="The version group that uses this flavor text.")

    class Meta:
        model = MoveFlavorText
        fields = ("flavor_text", "language", "version_group")


class MoveComboUsageSerializer(serializers.Serializer[Any]):
    use_before = MoveSummarySerializer(many=True, allow_null=True, help_text="A list of moves to use before this move.")
    use_after = MoveSummarySerializer(many=True, allow_null=True, help_text="A list of moves to use after this move.")


class MoveCombosSerializer(serializers.Serializer[Any]):
    normal = MoveComboUsageSerializer(
        help_text="A detail of moves this move can be used before or after, granting additional appeal points in contests."
    )
    super = MoveComboUsageSerializer(
        help_text="A detail of moves this move can be used before or after, granting additional appeal points in super contests."
    )


class MoveMetaStatChangeSerializer(serializers.ModelSerializer[MoveMetaStatChange]):
    stat = StatSummarySerializer(help_text="The stat being affected.")

    class Meta:
        model = MoveMetaStatChange
        fields = ("change", "stat")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            change="The amount of change.",
        )


class MoveDetailSerializer(serializers.ModelSerializer[Move]):
    generation = GenerationSummarySerializer(help_text="The generation in which this move was introduced.")
    type = TypeSummarySerializer(help_text="The elemental type of this move.")
    target = MoveTargetSummarySerializer(
        source="move_target", help_text="The type of target that will receive the effects of the attack."
    )
    contest_type = ContestTypeSummarySerializer(
        allow_null=True, help_text="The type of appeal this move gives a Pokémon when used in a contest."
    )
    contest_effect = ContestEffectSummarySerializer(
        allow_null=True, help_text="The effect the move has when used in a contest."
    )
    damage_class = MoveDamageClassSummarySerializer(
        source="move_damage_class", help_text="The type of damage the move inflicts on the target, e.g. physical."
    )
    meta = MoveMetaSerializer(read_only=True, source="movemeta", allow_null=True, help_text="Metadata about this move")
    names = MoveNameSerializer(
        many=True,
        read_only=True,
        source="movename",
        help_text=LOCALIZED_NAMES_HELP,
    )
    effect_entries = serializers.SerializerMethodField(
        "get_effect_text", help_text="The effect of this move listed in different languages."
    )
    effect_chance = serializers.IntegerField(
        source="move_effect_chance",
        allow_null=True,
        help_text="The percent value of how likely it is this moves effect will happen.",
    )
    contest_combos = serializers.SerializerMethodField(
        "get_combos", help_text="A detail of normal and super contest combos that require this move."
    )
    stat_changes = serializers.SerializerMethodField(
        "get_move_stat_change", help_text="A list of stats this moves effects and how much it effects them."
    )
    super_contest_effect = SuperContestEffectSummarySerializer(
        allow_null=True, help_text="The effect the move has when used in a super contest."
    )
    past_values = MoveChangeSerializer(
        many=True,
        read_only=True,
        source="movechange",
        help_text="A list of move resource value changes across version groups of the game.",
    )
    effect_changes = serializers.SerializerMethodField(
        "get_effect_change_text",
        help_text="The list of previous effects this move has had across version groups of the games.",
    )
    machines = serializers.SerializerMethodField(
        "get_move_machines", help_text="A list of the machines that teach this move."
    )
    flavor_text_entries = MoveFlavorTextSerializer(
        many=True,
        read_only=True,
        source="moveflavortext",
        help_text="The flavor text of this move listed in different languages.",
    )
    learned_by_pokemon = serializers.SerializerMethodField(help_text="List of Pokemon that can learn the move")

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
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
            accuracy=MOVE_ACCURACY_HELP,
            pp=MOVE_PP_HELP,
            priority="A value between -8 and 8. Sets the order in which moves are executed during battle. See [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Priority) for greater detail.",
            power="The base power of this move, or null if it has no fixed base power.",
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
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = PalParkAreaName
        fields = ("name", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=LOCALIZED_NAME_HELP,
        )


class PalParkEncounterSerializer(serializers.ModelSerializer[PalPark]):
    pokemon_species = PokemonSpeciesSummarySerializer(help_text="The Pokémon species being encountered.")

    class Meta:
        model = PalPark
        fields = ("base_score", "rate", "pokemon_species")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            base_score="The base score given to the player when this Pokémon is caught during a pal park run.",
            rate="The base rate for encountering this Pokémon in this pal park area.",
        )


class PalParkAreaDetailSerializer(serializers.ModelSerializer[PalParkArea]):
    names = PalParkAreaNameSerializer(
        many=True,
        read_only=True,
        source="palparkareaname",
        help_text=LOCALIZED_NAMES_HELP,
    )
    pokemon_encounters = serializers.SerializerMethodField(
        "get_encounters", help_text="A list of Pokémon encountered in thi pal park area along with details."
    )

    class Meta:
        model = PalParkArea
        fields = ("id", "name", "names", "pokemon_encounters")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
        )

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
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = PokemonColorName
        fields = ("name", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=LOCALIZED_NAME_HELP,
        )


class PokemonColorDetailSerializer(serializers.ModelSerializer[PokemonColor]):
    names = PokemonColorNameSerializer(
        many=True,
        read_only=True,
        source="pokemoncolorname",
        help_text=LOCALIZED_NAMES_HELP,
    )
    pokemon_species = PokemonSpeciesSummarySerializer(
        many=True,
        read_only=True,
        source="pokemonspecies",
        help_text="A list of the Pokémon species that have this color.",
    )

    class Meta:
        model = PokemonColor
        fields = ("id", "name", "names", "pokemon_species")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
        )


##############################
#  POKEMON FORM SERIALIZERS  #
##############################


class PokemonSpritesOtherDreamWorldSerializer(serializers.Serializer[Any]):
    front_default = serializers.CharField(
        allow_null=True,
        help_text="The URL of the default Pokémon Dream World front image, or null if unavailable.",
    )
    front_female = serializers.CharField(
        allow_null=True,
        help_text="The URL of the female Pokémon Dream World front image, or null if unavailable.",
    )


class PokemonSpritesOtherHomeSerializer(serializers.Serializer[Any]):
    front_default = serializers.CharField(
        allow_null=True,
        help_text="The URL of the default Pokémon HOME front image, or null if unavailable.",
    )
    front_female = serializers.CharField(
        allow_null=True,
        help_text="The URL of the female Pokémon HOME front image, or null if unavailable.",
    )
    front_shiny = serializers.CharField(
        allow_null=True,
        help_text="The URL of the shiny Pokémon HOME front image, or null if unavailable.",
    )
    front_shiny_female = serializers.CharField(
        allow_null=True,
        help_text="The URL of the shiny female Pokémon HOME front image, or null if unavailable.",
    )


class PokemonSpritesOtherOfficialArtworkSerializer(serializers.Serializer[Any]):
    front_default = serializers.CharField(
        allow_null=True,
        help_text="The URL of the default front official artwork, or null if unavailable.",
    )
    front_shiny = serializers.CharField(
        allow_null=True,
        help_text="The URL of the shiny front official artwork, or null if unavailable.",
    )
    versions = serializers.DictField(
        child=serializers.DictField(child=serializers.JSONField()),
        required=False,
        help_text="Additional official artwork grouped by version. Available keys vary by resource.",
    )


class PokemonSpritesOtherShowdownSerializer(serializers.Serializer[Any]):
    front_default = serializers.CharField(
        allow_null=True,
        help_text="The URL of the default Pokémon Showdown front image, or null if unavailable.",
    )
    front_female = serializers.CharField(
        allow_null=True,
        help_text="The URL of the female Pokémon Showdown front image, or null if unavailable.",
    )
    front_shiny = serializers.CharField(
        allow_null=True,
        help_text="The URL of the shiny Pokémon Showdown front image, or null if unavailable.",
    )
    front_shiny_female = serializers.CharField(
        allow_null=True,
        help_text="The URL of the shiny female Pokémon Showdown front image, or null if unavailable.",
    )
    back_default = serializers.CharField(
        allow_null=True,
        help_text="The URL of the default Pokémon Showdown back image, or null if unavailable.",
    )
    back_female = serializers.CharField(
        allow_null=True,
        help_text="The URL of the female Pokémon Showdown back image, or null if unavailable.",
    )
    back_shiny = serializers.CharField(
        allow_null=True,
        help_text="The URL of the shiny Pokémon Showdown back image, or null if unavailable.",
    )
    back_shiny_female = serializers.CharField(
        allow_null=True,
        help_text="The URL of the shiny female Pokémon Showdown back image, or null if unavailable.",
    )


class PokemonSpritesOtherSerializer(serializers.Serializer[Any]):
    dream_world = PokemonSpritesOtherDreamWorldSerializer(required=False, help_text="Pokémon Dream World artwork URLs.")
    home = PokemonSpritesOtherHomeSerializer(required=False, help_text="Pokémon HOME sprite URLs.")
    showdown = PokemonSpritesOtherShowdownSerializer(required=False, help_text="Pokémon Showdown sprite URLs.")


PokemonSpritesOtherSerializer._declared_fields["official-artwork"] = PokemonSpritesOtherOfficialArtworkSerializer(
    required=False, help_text="Official Pokémon artwork URLs, including shiny artwork and version-specific variants."
)


class PokemonSpritesSerializer(serializers.Serializer[Any]):
    front_default = serializers.CharField(
        allow_null=True, help_text="The default depiction of this Pokémon from the front in battle."
    )
    front_shiny = serializers.CharField(
        allow_null=True, help_text="The shiny depiction of this Pokémon from the front in battle."
    )
    front_female = serializers.CharField(
        allow_null=True, help_text="The female depiction of this Pokémon from the front in battle."
    )
    front_shiny_female = serializers.CharField(
        allow_null=True, help_text="The shiny female depiction of this Pokémon from the front in battle."
    )
    back_default = serializers.CharField(
        allow_null=True, help_text="The default depiction of this Pokémon from the back in battle."
    )
    back_shiny = serializers.CharField(
        allow_null=True, help_text="The shiny depiction of this Pokémon from the back in battle."
    )
    back_female = serializers.CharField(
        allow_null=True, help_text="The female depiction of this Pokémon from the back in battle."
    )
    back_shiny_female = serializers.CharField(
        allow_null=True, help_text="The shiny female depiction of this Pokémon from the back in battle."
    )
    other = PokemonSpritesOtherSerializer(
        required=False,
        help_text="Additional sprites grouped by source, such as official artwork, HOME, and Showdown. Available keys vary by resource.",
    )
    versions = serializers.DictField(
        child=serializers.DictField(child=serializers.JSONField()),
        required=False,
        help_text="Sprites grouped by generation and game. Available keys vary by resource.",
    )


class PokemonFormSpritesSerializer(PokemonSpritesSerializer):
    pass


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
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = PokemonFormName
        fields = ("name", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=LOCALIZED_NAME_HELP,
        )


class PokemonFormTypeSerializer(serializers.ModelSerializer[PokemonFormType]):
    type = TypeSummarySerializer(help_text="The type the referenced Form has.")

    class Meta:
        model = PokemonFormType
        fields = ("slot", "type")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            slot=POKEMON_TYPE_SLOT_HELP,
        )


class PokemonTypeSerializer(serializers.ModelSerializer[PokemonType]):
    type = TypeSummarySerializer(help_text="The type the referenced Pokémon has.")

    class Meta:
        model = PokemonType
        fields = ("slot", "type")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            slot=POKEMON_TYPE_SLOT_HELP,
        )


class PokemonFormTriggerConditionSerializer(serializers.Serializer[Any]):
    trigger = serializers.CharField(help_text="The trigger for this form change.")
    name = serializers.CharField(
        required=False,
        help_text="The name of the required item, ability, or move. Only present for a resource-based trigger.",
    )
    url = serializers.URLField(
        required=False,
        help_text="The URL of the required item, ability, or move. Only present for a resource-based trigger.",
    )
    base_form = PokemonFormSummarySerializer(
        required=False, help_text="The required base form. Only present when the trigger specifies one."
    )


class PokemonShapeNameSerializer(serializers.ModelSerializer[PokemonShapeName]):
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = PokemonShapeName
        fields = ("name", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=LOCALIZED_NAME_HELP,
        )


class PokemonShapeAwesomeNameSerializer(serializers.ModelSerializer[PokemonShapeName]):
    language = LanguageSummarySerializer(help_text='The language this "scientific" name is in.')

    class Meta:
        model = PokemonShapeName
        fields = ("awesome_name", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            awesome_name='The localized "scientific" name for an API resource in a specific language.',
        )


class PokemonFormFlavorTextSerializer(serializers.ModelSerializer[PokemonFormFlavorText]):
    flavor_text = serializers.CharField(
        help_text="The localized flavor text for an API resource in a specific language. Note that this text is left unprocessed as it is found in game files. This means that it contains special characters that one might want to replace with their visible decodable version. Please check out this <a href='https://github.com/veekun/pokedex/issues/218#issuecomment-339841781' >issue</a> to find out more. "
    )
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)
    version = VersionSummarySerializer(help_text="The game version this flavor text is extracted from.")

    class Meta:
        model = PokemonFormFlavorText
        fields = ("flavor_text", "language", "version")


class PokemonFormDetailSerializer(serializers.ModelSerializer[PokemonForm]):
    pokemon = PokemonSummarySerializer(help_text="The Pokémon that can take on this form.")
    version_group = VersionGroupSummarySerializer(help_text="The version group this Pokémon form was introduced in.")
    sprites = serializers.SerializerMethodField(
        "get_pokemon_form_sprites", help_text="A set of sprites used to depict this Pokémon form in the game."
    )
    form_names = serializers.SerializerMethodField(
        "get_pokemon_form_names",
        help_text="The form specific form name of this Pokémon form, or empty if the form does not have a specific name.",
    )
    names = serializers.SerializerMethodField(
        "get_pokemon_form_pokemon_names",
        help_text="The form specific full name of this Pokémon form, or empty if the form does not have a specific name.",
    )
    types = serializers.SerializerMethodField(
        "get_pokemon_form_types", help_text="A list of details showing types this Pokémon form has."
    )
    trigger_conditions = serializers.SerializerMethodField(
        "get_pokemon_form_triggers_conditions",
        help_text="The conditions that trigger this form. Resource names and URLs are included when the trigger requires a resource.",
    )
    flavor_text_entries = PokemonFormFlavorTextSerializer(
        many=True,
        read_only=True,
        source="pokemonformflavortext",
        help_text="The flavor text of this form listed in different languages and versions.",
    )

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
            "flavor_text_entries",
        )
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
            order="The order in which forms should be sorted within all forms. Multiple forms may have equal order, in which case they should fall back on sorting by name.",
            form_order="The order in which forms should be sorted within a species' forms.",
            is_default="True for exactly one form used as the default for each Pokémon.",
            is_battle_only="Whether or not this form can only happen during battle.",
            is_mega="Whether or not this form requires mega evolution.",
            form_name="The name of this form.",
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
        form_types = PokemonFormType.objects.filter(pokemon_form=obj).select_related("type").order_by("slot", "pk")

        if form_types:
            return cast(
                "ReturnList[ReturnDict[str, Any]]",
                PokemonFormTypeSerializer(form_types, many=True, context=self.context).data,
            )

        # Fall back to parent Pokemon's types if no form-specific types exist
        pokemon_types = PokemonType.objects.filter(pokemon=obj.pokemon).select_related("type").order_by("slot", "pk")
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
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = PokemonHabitatName
        fields = ("name", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=LOCALIZED_NAME_HELP,
        )


class PokemonHabitatDetailSerializer(serializers.ModelSerializer[PokemonHabitat]):
    names = PokemonHabitatNameSerializer(
        many=True,
        read_only=True,
        source="pokemonhabitatname",
        help_text=LOCALIZED_NAMES_HELP,
    )
    pokemon_species = PokemonSpeciesSummarySerializer(
        many=True,
        read_only=True,
        source="pokemonspecies",
        help_text="A list of the Pokémon species that can be found in this habitat.",
    )

    class Meta:
        model = PokemonHabitat
        fields = ("id", "name", "names", "pokemon_species")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
        )


##############################
#  POKEMON MOVE SERIALIZERS  #
##############################


class MoveLearnMethodNameSerializer(serializers.HyperlinkedModelSerializer[MoveLearnMethodName]):
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = MoveLearnMethodName
        fields = ("name", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=LOCALIZED_NAME_HELP,
        )


class MoveLearnMethodDescriptionSerializer(serializers.HyperlinkedModelSerializer[MoveLearnMethodDescription]):
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = MoveLearnMethodDescription
        fields = ("description", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            description=LOCALIZED_DESCRIPTION_HELP,
        )


class MoveLearnMethodDetailSerializer(serializers.ModelSerializer[MoveLearnMethod]):
    names = MoveLearnMethodNameSerializer(
        many=True,
        read_only=True,
        source="movelearnmethodname",
        help_text=LOCALIZED_NAMES_HELP,
    )
    descriptions = MoveLearnMethodDescriptionSerializer(
        many=True,
        read_only=True,
        source="movelearnmethoddescription",
        help_text=LOCALIZED_DESCRIPTIONS_HELP,
    )
    version_groups = serializers.SerializerMethodField(
        "get_method_version_groups",
        help_text="A list of version groups where moves can be learned through this method.",
    )

    class Meta:
        model = MoveLearnMethod
        fields = ("id", "name", "names", "descriptions", "version_groups")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
        )

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
    names = serializers.SerializerMethodField("get_shape_names", help_text=LOCALIZED_NAMES_HELP)
    awesome_names = serializers.SerializerMethodField(
        "get_shape_awesome_names",
        help_text='The "scientific" name of this Pokémon shape listed in different languages.',
    )
    pokemon_species = PokemonSpeciesSummarySerializer(
        many=True,
        read_only=True,
        source="pokemonspecies",
        help_text="A list of the Pokémon species that have this shape.",
    )

    class Meta:
        model = PokemonShape
        fields = ("id", "name", "awesome_names", "names", "pokemon_species")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
        )

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
    version = VersionSummarySerializer(help_text="The version relevent to this game index.")

    class Meta:
        model = PokemonGameIndex
        fields = ("game_index", "version")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            game_index=GAME_INDEX_HELP,
        )


class PokemonAbilitySerializer(serializers.ModelSerializer[PokemonAbility]):
    ability = AbilitySummarySerializer(help_text="The ability the Pokémon may have.")

    class Meta:
        model = PokemonAbility
        fields = ("is_hidden", "slot", "ability")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            is_hidden=POKEMON_ABILITY_HIDDEN_HELP,
            slot=POKEMON_ABILITY_SLOT_HELP,
        )


class PokemonCriesSerializer(serializers.Serializer[Any]):
    latest = serializers.CharField(allow_null=True, help_text="The latest depiction of this Pokémon's cry.")
    legacy = serializers.CharField(allow_null=True, help_text="The legacy depiction of this Pokémon's cry.")


class PokemonMoveVersionGroupSerializer(serializers.Serializer[Any]):
    level_learned_at = serializers.IntegerField(help_text="The minimum level to learn the move.")
    move_learn_method = MoveLearnMethodSummarySerializer(help_text="The method by which the move is learned.")
    version_group = VersionGroupSummarySerializer(help_text="The version group in which the move is learned.")
    order = serializers.IntegerField(
        allow_null=True,
        required=False,
        help_text="Order by which the pokemon will learn the move. A newly learnt move will replace the move with lowest order.",
    )


class PokemonMoveSerializer(serializers.Serializer[Any]):
    move = MoveSummarySerializer(help_text="The move the Pokémon can learn.")
    version_group_details = PokemonMoveVersionGroupSerializer(
        many=True, help_text="The details of the version in which the Pokémon can learn the move."
    )


class PokemonAbilityPastSerializer(serializers.ModelSerializer[PokemonAbilityPast]):
    ability = AbilitySummarySerializer(allow_null=True, help_text="The ability the Pokémon may have.")

    class Meta:
        model = PokemonAbilityPast
        fields = ("is_hidden", "slot", "ability")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            is_hidden=POKEMON_ABILITY_HIDDEN_HELP,
            slot=POKEMON_ABILITY_SLOT_HELP,
        )


class PokemonPastAbilitySerializer(serializers.Serializer[Any]):
    abilities = PokemonAbilityPastSerializer(
        many=True,
        help_text="The abilities the referenced pokémon had up to and including the listed generation. If null, the slot was previously empty.",
    )
    generation = GenerationSummarySerializer(
        help_text="The last generation in which the referenced pokémon had the listed abilities."
    )


class PokemonStatSerializer(serializers.ModelSerializer[PokemonStat]):
    stat = StatSummarySerializer(help_text="The stat the Pokémon has.")

    class Meta:
        model = PokemonStat
        fields = ("base_stat", "effort", "stat")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            base_stat=POKEMON_BASE_STAT_HELP,
            effort=POKEMON_EFFORT_HELP,
        )


class PokemonPastStatSerializer(serializers.Serializer[Any]):
    generation = GenerationSummarySerializer(
        help_text="The last generation in which the referenced pokémon had the listed stats."
    )
    stats = PokemonStatSerializer(
        many=True, help_text="The stat the Pokémon had up to and including the listed generation."
    )


class PokemonPastTypeSerializer(serializers.Serializer[Any]):
    generation = GenerationSummarySerializer(
        help_text="The last generation in which the referenced pokémon had the listed types."
    )
    types = PokemonTypeSerializer(
        many=True, help_text="The types the referenced pokémon had up to and including the listed generation."
    )


class PokemonSpeciesNameSerializer(serializers.ModelSerializer[PokemonSpeciesName]):
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = PokemonSpeciesName
        fields = ("name", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=LOCALIZED_NAME_HELP,
        )


class PokemonSpeciesGenusSerializer(serializers.ModelSerializer[PokemonSpeciesName]):
    language = LanguageSummarySerializer(help_text="The language this genus is in.")

    class Meta:
        model = PokemonSpeciesName
        fields = ("genus", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            genus="The localized genus for the referenced Pokémon species",
        )


class PokemonSpeciesVarietySerializer(serializers.Serializer[Any]):
    is_default = serializers.BooleanField(help_text="Whether this variety is the default variety.")
    pokemon = PokemonSummarySerializer(help_text="The Pokémon variety.")


class PokemonSpeciesPalParkEncounterSerializer(serializers.ModelSerializer[PalPark]):
    area = PalParkAreaSummarySerializer(
        source="pal_park_area", help_text="The pal park area where this encounter happens."
    )

    class Meta:
        model = PalPark
        fields = ("base_score", "rate", "area")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            base_score="The base score given to the player when the referenced Pokémon is caught during a pal park run.",
            rate="The base rate for encountering the referenced Pokémon in this pal park area.",
        )


class PokemonStatPastSerializer(serializers.ModelSerializer[PokemonStatPast]):
    stat = StatSummarySerializer(help_text="The stat the Pokémon has.")

    class Meta:
        model = PokemonStatPast
        fields = ("base_stat", "effort", "stat")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            base_stat=POKEMON_BASE_STAT_HELP,
            effort=POKEMON_EFFORT_HELP,
        )


class PokemonTypePastSerializer(serializers.ModelSerializer[PokemonTypePast]):
    type = TypeSummarySerializer(help_text="The type the referenced Pokémon has.")

    class Meta:
        model = PokemonTypePast
        fields = ("slot", "type")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            slot=POKEMON_TYPE_SLOT_HELP,
        )


class PokemonDetailSerializer(serializers.ModelSerializer[Pokemon]):
    abilities = serializers.SerializerMethodField(
        "get_pokemon_abilities", help_text="A list of abilities this Pokémon could potentially have."
    )
    past_abilities = serializers.SerializerMethodField(
        "get_past_pokemon_abilities",
        help_text="A list of details showing abilities this pokémon had in previous generations",
    )
    game_indices = PokemonGameIndexSerializer(
        many=True,
        read_only=True,
        source="pokemongameindex",
        help_text="A list of game indices relevent to Pokémon item by generation.",
    )
    moves = serializers.SerializerMethodField(
        "get_pokemon_moves",
        help_text="A list of moves along with learn methods and level details pertaining to specific version groups.",
    )
    species = PokemonSpeciesSummarySerializer(
        source="pokemon_species", help_text="The species this Pokémon belongs to."
    )
    stats = PokemonStatSerializer(
        many=True, read_only=True, source="pokemonstat", help_text="A list of base stat values for this Pokémon."
    )
    past_stats = serializers.SerializerMethodField(
        "get_past_pokemon_stats", help_text="A list of details showing stats this pokémon had in previous generations"
    )
    types = serializers.SerializerMethodField(
        "get_pokemon_types", help_text="A list of details showing types this Pokémon has."
    )
    past_types = serializers.SerializerMethodField(
        "get_past_pokemon_types", help_text="A list of details showing types this pokémon had in previous generations"
    )
    forms = PokemonFormSummarySerializer(
        many=True, read_only=True, source="pokemonform", help_text="A list of forms this Pokémon can take on."
    )
    held_items = serializers.SerializerMethodField(
        "get_pokemon_held_items", help_text="A list of items this Pokémon may be holding when encountered."
    )
    location_area_encounters = serializers.SerializerMethodField(
        "get_encounters",
        help_text="A link to a list of location areas, as well as encounter details pertaining to specific versions.",
    )
    sprites = serializers.SerializerMethodField(
        "get_pokemon_sprites",
        help_text="A set of sprites used to depict this Pokémon in the game. A visual representation of the various sprites can be found at <a href='https://github.com/PokeAPI/sprites#sprites'>PokeAPI/sprites</a>",
    )
    cries = serializers.SerializerMethodField(
        "get_pokemon_cries",
        help_text="A set of cries used to depict this Pokémon in the game. A visual representation of the various cries can be found at <a href='https://github.com/PokeAPI/cries#cries'>PokeAPI/cries</a>",
    )

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
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
            base_experience="The base experience gained for defeating this Pokémon.",
            height="The height of this Pokémon in decimetres.",
            is_default="Set for exactly one Pokémon used as the default for each species.",
            order="Order for sorting. Almost national order, except families are grouped together.",
            weight="The weight of this Pokémon in hectograms.",
        )

    _FEMALE_FALLBACKS: ClassVar[dict[str, str]] = {
        "front_female": "front_default",
        "back_female": "back_default",
        "front_shiny_female": "front_shiny",
        "back_shiny_female": "back_shiny",
    }

    @extend_schema_field(PokemonSpritesSerializer)
    def get_pokemon_sprites(self, obj: Pokemon) -> dict[str, Any]:
        sprites_list = list(cast("PokemonWithRelations", obj).pokemonsprites.all())
        if not sprites_list:
            return {}
        sprites = sprites_list[0].sprites
        if obj.pokemon_species and obj.pokemon_species.gender_rate == 8:
            self._fill_female_sprites(sprites)
        return sprites

    def _fill_female_sprites(self, sprites: dict[str, Any]) -> None:
        for female_key, default_key in self._FEMALE_FALLBACKS.items():
            if female_key in sprites and sprites[female_key] is None and sprites.get(default_key) is not None:
                sprites[female_key] = sprites[default_key]
        for value in sprites.values():
            if isinstance(value, dict):
                self._fill_female_sprites(cast("dict[str, Any]", value))

    @extend_schema_field(PokemonCriesSerializer)
    def get_pokemon_cries(self, obj: Pokemon) -> dict[str, str | None]:
        cries_list = list(cast("PokemonWithRelations", obj).pokemoncries.all())
        return cries_list[0].cries if cries_list else {}

    @extend_schema_field(PokemonMoveSerializer(many=True))
    def get_pokemon_moves(self, obj: Pokemon) -> list[dict[str, Any]]:
        pokemon_moves = (
            PokemonMove.objects.filter(pokemon=obj, move__isnull=False)
            .select_related("move", "version_group", "move_learn_method")
            .order_by("move__id", "version_group_id", "move_learn_method_id", "level", "pk")
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

    @extend_schema_field(PokemonHeldItemSummarySerializer(many=True))
    def get_pokemon_held_items(self, obj: Pokemon) -> list[dict[str, Any]]:
        pokemon_items = (
            PokemonItem.objects.filter(pokemon=obj, item__isnull=False)
            .select_related("item", "version")
            .order_by("item__id", "version_id", "pk")
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
            .order_by("generation_id", "slot", "pk")
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
            .order_by("generation_id", "stat_id", "pk")
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
        types = PokemonType.objects.filter(pokemon=obj).select_related("type").order_by("slot", "pk")
        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            PokemonTypeSerializer(types, many=True, context=self.context).data,
        )

    @extend_schema_field(PokemonPastTypeSerializer(many=True))
    def get_past_pokemon_types(self, obj: Pokemon) -> list[dict[str, Any]]:
        past_types = (
            PokemonTypePast.objects.filter(pokemon=obj, generation__isnull=False)
            .select_related("generation", "type")
            .order_by("generation_id", "slot", "pk")
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
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = EvolutionTriggerName
        fields = ("name", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=LOCALIZED_NAME_HELP,
        )


class EvolutionTriggerDetailSerializer(serializers.HyperlinkedModelSerializer[EvolutionTrigger]):
    names = EvolutionTriggerNameSerializer(
        many=True,
        read_only=True,
        source="evolutiontriggername",
        help_text=LOCALIZED_NAMES_HELP,
    )
    pokemon_species = serializers.SerializerMethodField(
        "get_species", help_text="A list of pokemon species that result from this evolution trigger."
    )

    class Meta:
        model = EvolutionTrigger
        fields = ("id", "name", "names", "pokemon_species")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
        )

    @extend_schema_field(PokemonSpeciesSummarySerializer(many=True))
    def get_species(self, obj: EvolutionTrigger) -> ReturnList[ReturnDict[str, Any]]:
        species = PokemonSpecies.objects.filter(evolved_species__evolution_trigger=obj).distinct().order_by("id")
        return cast(
            "ReturnList[ReturnDict[str, Any]]",
            PokemonSpeciesSummarySerializer(species, many=True, context=self.context).data,
        )


class EvolutionVariableNameSerializer(serializers.ModelSerializer[EvolutionVariableName]):
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = EvolutionVariableName
        fields = ("name", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=LOCALIZED_NAME_HELP,
        )


class EvolutionVariableDescriptionSerializer(serializers.ModelSerializer[EvolutionVariableDescription]):
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = EvolutionVariableDescription
        fields = ("description", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            description=LOCALIZED_DESCRIPTION_HELP,
        )


class EvolutionVariableDetailSerializer(serializers.HyperlinkedModelSerializer[EvolutionVariable]):
    version_group = VersionGroupSummarySerializer(help_text="The version group in which this variable was introduced.")
    names = EvolutionVariableNameSerializer(
        many=True,
        read_only=True,
        source="evolutionvariablename",
        help_text=LOCALIZED_NAMES_HELP,
    )
    descriptions = EvolutionVariableDescriptionSerializer(
        many=True,
        read_only=True,
        source="evolutionvariabledescription",
        help_text=LOCALIZED_DESCRIPTIONS_HELP,
    )

    class Meta:
        model = EvolutionVariable
        fields = ("id", "name", "symbol", "data_type", "source", "version_group", "names", "descriptions")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
            symbol="The symbol used for this variable in evolution condition expressions.",
            data_type="The data type of this variable.",
            source="The source of the variable value.",
        )


class PokemonSpeciesDescriptionSerializer(serializers.ModelSerializer[PokemonSpeciesDescription]):
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = PokemonSpeciesDescription
        fields = ("description", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            description=LOCALIZED_DESCRIPTION_HELP,
        )


class PokemonSpeciesFlavorTextSerializer(serializers.ModelSerializer[PokemonSpeciesFlavorText]):
    flavor_text = serializers.CharField(
        help_text="The localized flavor text for an API resource in a specific language. Note that this text is left unprocessed as it is found in game files. This means that it contains special characters that one might want to replace with their visible decodable version. Please check out this <a href='https://github.com/veekun/pokedex/issues/218#issuecomment-339841781' >issue</a> to find out more. "
    )
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)
    version = VersionSummarySerializer(help_text="The game version this flavor text is extracted from.")

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
    names = serializers.SerializerMethodField("get_pokemon_names", help_text=LOCALIZED_NAMES_HELP)
    form_descriptions = PokemonSpeciesDescriptionSerializer(
        many=True,
        read_only=True,
        source="pokemonspeciesdescription",
        help_text="Descriptions of different forms Pokémon take on within the Pokémon species.",
    )
    pokedex_numbers = PokemonDexEntrySerializer(
        many=True,
        read_only=True,
        source="pokemondexnumber",
        help_text="A list of Pokedexes and the indexes reserved within them for this Pokémon species.",
    )
    egg_groups = serializers.SerializerMethodField(
        "get_pokemon_egg_groups", help_text="A list of egg groups this Pokémon species is a member of."
    )
    flavor_text_entries = PokemonSpeciesFlavorTextSerializer(
        many=True,
        read_only=True,
        source="pokemonspeciesflavortext",
        help_text="A list of flavor text entries for this Pokémon species.",
    )
    genera = serializers.SerializerMethodField(
        "get_pokemon_genera", help_text="The genus of this Pokémon species listed in multiple languages."
    )
    generation = GenerationSummarySerializer(help_text="The generation this Pokémon species was introduced in.")
    growth_rate = GrowthRateSummarySerializer(help_text="The rate at which this Pokémon species gains levels.")
    color = PokemonColorSummarySerializer(
        source="pokemon_color", help_text="The color of this Pokémon for Pokédex search."
    )
    habitat = PokemonHabitatSummarySerializer(
        source="pokemon_habitat", allow_null=True, help_text="The habitat this Pokémon species can be encountered in."
    )
    shape = PokemonShapeSummarySerializer(
        source="pokemon_shape", help_text="The shape of this Pokémon for Pokédex search."
    )
    evolves_from_species = PokemonSpeciesSummarySerializer(
        allow_null=True, help_text="The Pokémon species that evolves into this Pokemon_species."
    )
    varieties = serializers.SerializerMethodField(
        "get_pokemon_varieties", help_text="A list of the Pokémon that exist within this Pokémon species."
    )
    evolution_chain = EvolutionChainSummarySerializer(
        help_text="The evolution chain this Pokémon species is a member of."
    )
    pal_park_encounters = serializers.SerializerMethodField(
        "get_encounters", help_text="A list of encounters that can be had with this Pokémon species in pal park."
    )

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
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
            order="The order in which species should be sorted. Based on National Dex order, except families are grouped together and sorted by stage.",
            gender_rate="The chance of this Pokémon being female, in eighths; or -1 for genderless.",
            capture_rate="The base capture rate; up to 255. The higher the number, the easier the catch.",
            base_happiness="The happiness when caught by a normal Pokéball; up to 255. The higher the number, the happier the Pokémon.",
            is_baby="Whether or not this is a baby Pokémon.",
            is_legendary="Whether or not this is a legendary Pokémon.",
            is_mythical="Whether or not this is a mythical Pokémon.",
            hatch_counter="Initial hatch counter: one must walk Y × (hatch_counter + 1) steps before this Pokémon's egg hatches, unless utilizing bonuses like Flame Body's. Y varies per generation. In Generations II, III, and VII, Egg cycles are 256 steps long. In Generation IV, Egg cycles are 255 steps long. In Pokémon Brilliant Diamond and Shining Pearl, Egg cycles are also 255 steps long, but are shorter on special dates. In Generations V and VI, Egg cycles are 257 steps long. In Pokémon Sword and Shield, and in Pokémon Scarlet and Violet, Egg cycles are 128 steps long.",  # noqa: RUF001
            has_gender_differences="Whether or not this Pokémon has visual gender differences.",
            forms_switchable="Whether or not this Pokémon has multiple forms and can switch between them.",
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
    version_group = VersionGroupSummarySerializer(
        help_text="The version group in which these evolution requirements apply."
    )
    item = ItemSummarySerializer(
        source="evolution_item",
        allow_null=True,
        help_text="The item required to cause evolution this into Pokémon species.",
    )
    held_item = ItemSummarySerializer(
        allow_null=True,
        help_text="The item the evolving Pokémon species must be holding during the evolution trigger event to evolve into this Pokémon species.",
    )
    known_move = MoveSummarySerializer(
        allow_null=True,
        help_text="The move that must be known by the evolving Pokémon species during the evolution trigger event in order to evolve into this Pokémon species.",
    )
    known_move_type = TypeSummarySerializer(
        allow_null=True,
        help_text="The evolving Pokémon species must know a move with this type during the evolution trigger event in order to evolve into this Pokémon species.",
    )
    party_species = PokemonSpeciesSummarySerializer(
        allow_null=True,
        help_text="The Pokémon species that must be in the players party in order for the evolving Pokémon species to evolve into this Pokémon species.",
    )
    party_type = TypeSummarySerializer(
        allow_null=True,
        help_text="The player must have a Pokémon of this type in their party during the evolution trigger event in order for the evolving Pokémon species to evolve into this Pokémon species.",
    )
    trade_species = PokemonSpeciesSummarySerializer(
        allow_null=True, help_text="Pokémon species for which this one must be traded."
    )
    location = LocationSummarySerializer(allow_null=True, help_text="The location the evolution must be triggered at.")
    trigger = EvolutionTriggerSummarySerializer(
        source="evolution_trigger", help_text="The type of event that triggers evolution into this Pokémon species."
    )
    region = RegionSummarySerializer(
        allow_null=True, help_text="The required region in which this evolution can occur."
    )
    required_pokemon_form = PokemonFormSummarySerializer(
        allow_null=True, help_text="The Pokémon form required before evolving, or null if unrestricted."
    )
    evolved_pokemon_form = PokemonFormSummarySerializer(
        allow_null=True, help_text="The Pokémon form produced by this evolution, or null if unspecified."
    )
    used_move = MoveSummarySerializer(
        allow_null=True,
        help_text="The move that must be used by the evolving Pokémon species during the evolution trigger event in order to evolve into this Pokémon species.",
    )
    allowed_natures = serializers.SerializerMethodField(
        "get_allowed_natures", help_text="The natures that allow this evolution, or null if unrestricted."
    )
    condition_expression = serializers.SerializerMethodField(
        "get_condition_expression",
        help_text="An additional evolution condition expressed in reverse Polish notation, or null if none.",
    )

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
            "required_pokemon_form",
            "evolved_pokemon_form",
            "used_move",
            "min_move_count",
            "min_steps",
            "min_damage_taken",
            "allowed_natures",
            "condition_expression",
        )
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            is_default="Whether the evolution is considered as the expected evolution in a main series game. Each unique Pokémon variety of a line capable of evolution should have exactly one 'default' evolution. For example, the Meowth species has three default evolutions as there are three distinct varieties it can evolve into: Persian, Alolan Persian, and Perrserker.",
            gender="The id of the gender of the evolving Pokémon species must be in order to evolve into this Pokémon species.",
            min_level="The minimum required level of the evolving Pokémon species to evolve into this Pokémon species.",
            min_happiness="The minimum required level of happiness the evolving Pokémon species to evolve into this Pokémon species.",
            min_beauty="The minimum required level of beauty the evolving Pokémon species to evolve into this Pokémon species.",
            min_affection="The minimum required level of affection the evolving Pokémon species to evolve into this Pokémon species.",
            near_special_rock="Whether or not you need to be near a Moss Rock or Icy Rock to evolve into this Pokémon species.",
            needs_multiplayer="Whether or not multiplayer link play is needed to evolve into this Pokémon species (e.g. Union Circle).",
            needs_overworld_rain="Whether or not it must be raining in the overworld to cause evolution this Pokémon species.",
            relative_physical_stats="The required relation between the Pokémon's Attack and Defense stats. 1 means Attack > Defense. 0 means Attack = Defense. -1 means Attack < Defense.",
            time_of_day="The required time of day. Day or night.",
            turn_upside_down="Whether or not the 3DS needs to be turned upside-down as this Pokémon levels up.",
            min_move_count="The minimum number of times a move must be used in order to evolve into this Pokémon species.",
            min_steps="The minimum number of steps that must be taken in order to evolve into this Pokémon species.",
            min_damage_taken="The minimum amount of damage taken during the evolution trigger event in order to evolve into this Pokémon species.",
        )

    @cached_property
    def _serialized_natures(self) -> list[tuple[int, dict[str, Any]]]:
        natures = Nature.objects.order_by("id")
        data = NatureSummarySerializer(natures, many=True, context=self.context).data
        return [(nature.pk, item) for nature, item in zip(natures, data, strict=True)]

    @cached_property
    def _serialized_evolution_variables(self) -> list[tuple[str, dict[str, Any]]]:
        variables = EvolutionVariable.objects.order_by("pk")
        data = EvolutionVariableSummarySerializer(variables, many=True, context=self.context).data
        return [(variable.symbol, item) for variable, item in zip(variables, data, strict=True)]

    @extend_schema_field(NatureSummarySerializer(many=True, allow_null=True))
    def get_allowed_natures(self, obj: PokemonEvolution) -> list[dict[str, Any]] | None:
        if obj.nature_bitmask is None:
            return None
        nature_ids = {i for i in range(1, 26) if (obj.nature_bitmask & (1 << (i - 1)))}
        if not nature_ids:
            return None
        return [item for nature_id, item in self._serialized_natures if nature_id in nature_ids]

    @extend_schema_field(EvolutionConditionExpressionSerializer(allow_null=True))
    def get_condition_expression(self, obj: PokemonEvolution) -> dict[str, Any] | None:
        if not obj.condition_expression:
            return None
        tokens = set(obj.condition_expression.split())
        return {
            "expression": obj.condition_expression,
            "percentage_chance": obj.percentage_chance,
            "variables": [item for symbol, item in self._serialized_evolution_variables if symbol in tokens],
        }


class EvolutionChainLinkSerializer(serializers.Serializer[Any]):
    is_baby = serializers.BooleanField(
        help_text="Whether or not this link is for a baby Pokémon. This would only ever be true on the base link."
    )
    species = PokemonSpeciesSummarySerializer(help_text="The Pokémon species at this point in the evolution chain.")
    evolution_details = PokemonEvolutionSerializer(
        many=True, help_text="All details regarding the specific details of the referenced Pokémon species evolution."
    )
    evolves_to = serializers.SerializerMethodField(help_text="A List of chain objects.")

    @extend_schema_field(lazy_serializer("pokemon_v2.serializers.EvolutionChainLinkSerializer")(many=True))  # pyright: ignore[reportArgumentType]
    def get_evolves_to(self, obj: dict[str, Any]) -> list[dict[str, Any]]:
        return obj["evolves_to"]


class EvolutionChainDetailSerializer(serializers.ModelSerializer[EvolutionChain]):
    baby_trigger_item = ItemSummarySerializer(
        allow_null=True,
        help_text="The item that a Pokémon would be holding when mating that would trigger the egg hatching a baby Pokémon rather than a basic Pokémon.",
    )
    chain = serializers.SerializerMethodField(
        "build_chain",
        help_text="The base chain link object. Each link contains evolution details for a Pokémon in the chain. Each link references the next Pokémon in the natural evolution order.",
    )

    POKEMON_EVOLUTION_FK_FIELDS: ClassVar[list[str]] = [
        field.name
        for field in PokemonEvolution._meta.get_fields()
        if field.is_relation and (field.many_to_one or field.one_to_one)
    ]

    class Meta:
        model = EvolutionChain
        fields = ("id", "baby_trigger_item", "chain")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
        )

    @extend_schema_field(EvolutionChainLinkSerializer)
    def build_chain(self, obj: EvolutionChain) -> dict[str, Any]:
        pokemon_objects = PokemonSpecies.objects.filter(evolution_chain=obj).order_by("order", "pk")
        summary_data = cast(
            "ReturnList[ReturnDict[str, Any]]",
            PokemonSpeciesSummarySerializer(pokemon_objects, many=True, context=self.context).data,
        )
        ref_data = cast(
            "ReturnList[ReturnDict[str, Any]]",
            PokemonSpeciesEvolutionSerializer(pokemon_objects, many=True, context=self.context).data,
        )

        evolutions_by_species: dict[int, list[PokemonEvolution]] = defaultdict(list)
        if any(species["evolves_from_species"] for species in ref_data):
            for evolution in (
                PokemonEvolution.objects.filter(evolved_species__evolution_chain=obj)
                .select_related(*self.POKEMON_EVOLUTION_FK_FIELDS)
                .order_by("pk")
            ):
                evolutions_by_species[evolution.evolved_species_id].append(evolution)  # pyright: ignore[reportAttributeAccessIssue]

        evolution_tree = self.build_evolution_tree(ref_data)
        return self.build_chain_link_entry(evolution_tree, summary_data, evolutions_by_species)

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
        self,
        chain_link: dict[str, Any],
        summary_data: ReturnList[ReturnDict[str, Any]],
        evolutions_by_species: dict[int, list[PokemonEvolution]],
    ) -> dict[str, Any]:
        species = chain_link["species"]
        evolution_data = None

        if species["evolves_from_species"]:
            evolution_objects = evolutions_by_species.get(species["id"], [])
            evolution_data = cast(
                "ReturnList[ReturnDict[str, Any]]",
                PokemonEvolutionSerializer(evolution_objects, many=True, context=self.context).data,
            )

        return {
            "is_baby": species["is_baby"],
            "species": next(x for x in summary_data if x["name"] == species["name"]),
            "evolution_details": evolution_data or [],
            "evolves_to": [
                self.build_chain_link_entry(c, summary_data, evolutions_by_species) for c in chain_link["children"]
            ],
        }


############################
#  POKEATHLON SERIALIZERS  #
############################


class PokeathlonStatNameSerializer(serializers.HyperlinkedModelSerializer[PokeathlonStatName]):
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = PokeathlonStatName
        fields = ("name", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=LOCALIZED_NAME_HELP,
        )


class PokeathlonStatAffectingNatureSerializer(serializers.ModelSerializer[NaturePokeathlonStat]):
    nature = NatureSummarySerializer(help_text="The nature causing the change.")

    class Meta:
        model = NaturePokeathlonStat
        fields = ("max_change", "nature")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            max_change="The maximum amount of change to the referenced Pokéathlon stat.",
        )


class PokeathlonStatAffectingNaturesSerializer(serializers.Serializer[Any]):
    increase = PokeathlonStatAffectingNatureSerializer(
        many=True, help_text="A list of natures and how they change the referenced Pokéathlon stat."
    )
    decrease = PokeathlonStatAffectingNatureSerializer(
        many=True, help_text="A list of natures and how they change the referenced Pokéathlon stat."
    )


class PokeathlonStatDetailSerializer(serializers.HyperlinkedModelSerializer[PokeathlonStat]):
    names = PokeathlonStatNameSerializer(
        many=True,
        read_only=True,
        source="pokeathlonstatname",
        help_text=LOCALIZED_NAMES_HELP,
    )
    affecting_natures = serializers.SerializerMethodField(
        "get_natures_that_affect",
        help_text="A detail of natures which affect this Pokéathlon stat positively or negatively.",
    )

    class Meta:
        model = PokeathlonStat
        fields = ("id", "name", "affecting_natures", "names")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
        )

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
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = PokedexName
        fields = ("name", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=LOCALIZED_NAME_HELP,
        )


class PokedexDescriptionSerializer(serializers.HyperlinkedModelSerializer[PokedexDescription]):
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = PokedexDescription
        fields = ("description", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            description=LOCALIZED_DESCRIPTION_HELP,
        )


class PokemonDexNumberSerializer(serializers.ModelSerializer[PokemonDexNumber]):
    entry_number = serializers.IntegerField(
        source="pokedex_number", help_text="The index of this Pokémon species entry within the Pokédex."
    )
    pokemon_species = PokemonSpeciesSummarySerializer(help_text="The Pokémon species being encountered.")

    class Meta:
        model = PokemonDexNumber
        fields = ("entry_number", "pokemon_species")


class PokedexDetailSerializer(serializers.ModelSerializer[Pokedex]):
    region = RegionSummarySerializer(allow_null=True, help_text="The region this Pokédex catalogues Pokémon for.")
    names = PokedexNameSerializer(
        many=True,
        read_only=True,
        source="pokedexname",
        help_text=LOCALIZED_NAMES_HELP,
    )
    descriptions = PokedexDescriptionSerializer(
        many=True,
        read_only=True,
        source="pokedexdescription",
        help_text=LOCALIZED_DESCRIPTIONS_HELP,
    )
    pokemon_entries = serializers.SerializerMethodField(
        "get_pokedex_entries", help_text="A list of Pokémon catalogued in this Pokédex and their indexes."
    )
    version_groups = serializers.SerializerMethodField(
        "get_pokedex_version_groups", help_text="A list of version groups this Pokédex is relevant to."
    )

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
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
            is_main_series="Whether or not this Pokédex originated in the main series of the video games.",
        )

    @extend_schema_field(PokemonDexNumberSerializer(many=True))
    def get_pokedex_entries(self, obj: Pokedex) -> ReturnList[ReturnDict[str, Any]]:
        entries = (
            PokemonDexNumber.objects.filter(pokedex=obj)
            .select_related("pokemon_species")
            .order_by("pokedex_number", "pokemon_species_id", "pk")
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
    language = LanguageSummarySerializer(help_text=NAME_LANGUAGE_HELP)

    class Meta:
        model = VersionName
        fields = ("name", "language")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            name=LOCALIZED_NAME_HELP,
        )


class VersionDetailSerializer(serializers.ModelSerializer[Version]):
    """
    Should have a link to Version Group info but the Circular
    dependency and compilation order fight eachother and I'm
    not sure how to add anything other than a hyperlink
    """

    names = VersionNameSerializer(
        many=True,
        read_only=True,
        source="versionname",
        help_text=LOCALIZED_NAMES_HELP,
    )
    version_group = VersionGroupSummarySerializer(help_text="The version group this version belongs to.")

    class Meta:
        model = Version
        fields = ("id", "name", "names", "version_group")
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
        )


class VersionGroupDetailSerializer(serializers.ModelSerializer[VersionGroup]):
    generation = GenerationSummarySerializer(help_text="The generation this version was introduced in.")
    versions = VersionSummarySerializer(
        many=True, read_only=True, source="version", help_text="The versions this version group owns."
    )
    regions = serializers.SerializerMethodField(
        "get_version_group_regions", help_text="A list of regions that can be visited in this version group."
    )
    move_learn_methods = serializers.SerializerMethodField(
        "get_learn_methods", help_text="A list of methods in which Pokémon can learn moves in this version group."
    )
    pokedexes = serializers.SerializerMethodField(
        "get_version_groups_pokedexes", help_text="A list of Pokédexes introduces in this version group."
    )

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
        extra_kwargs: ClassVar[dict[str, dict[str, str]]] = format_help_text(
            id=RESOURCE_ID_HELP,
            name=RESOURCE_NAME_HELP,
            order="Order for sorting. Almost by date of release, except similar versions are grouped together.",
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
