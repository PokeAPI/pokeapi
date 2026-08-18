# pyright: reportIncompatibleVariableOverride=false
from __future__ import annotations

from typing import Any

from django.db import models
from typing_extensions import override

__all__: tuple[str, ...] = (
    "Ability",
    "AbilityChange",
    "AbilityChangeEffectText",
    "AbilityEffectText",
    "AbilityFlavorText",
    "AbilityName",
    "Berry",
    "BerryFirmness",
    "BerryFirmnessName",
    "BerryFlavor",
    "BerryFlavorMap",
    "BerryFlavorName",
    "Characteristic",
    "CharacteristicDescription",
    "ContestCombo",
    "ContestEffect",
    "ContestEffectEffectText",
    "ContestEffectFlavorText",
    "ContestType",
    "ContestTypeName",
    "Currency",
    "CurrencyName",
    "EggGroup",
    "EggGroupName",
    "Encounter",
    "EncounterCondition",
    "EncounterConditionName",
    "EncounterConditionValue",
    "EncounterConditionValueMap",
    "EncounterConditionValueName",
    "EncounterMethod",
    "EncounterMethodName",
    "EncounterPokemonDetail",
    "EncounterSlot",
    "EvolutionChain",
    "EvolutionTrigger",
    "EvolutionTriggerName",
    "Experience",
    "Gender",
    "Generation",
    "GenerationName",
    "GrowthRate",
    "GrowthRateDescription",
    "HasAbility",
    "HasCharacteristic",
    "HasContestEffect",
    "HasContestType",
    "HasDescription",
    "HasEffect",
    "HasEggGroup",
    "HasEncounterCondition",
    "HasEncounterMethod",
    "HasEvolutionTrigger",
    "HasFlavorText",
    "HasFlingEffect",
    "HasGameIndex",
    "HasGender",
    "HasGeneration",
    "HasGrowthRate",
    "HasItem",
    "HasItemAttribute",
    "HasItemCategory",
    "HasItemPocket",
    "HasLanguage",
    "HasLocation",
    "HasLocationArea",
    "HasMetaAilment",
    "HasMetaCategory",
    "HasMove",
    "HasMoveAttribute",
    "HasMoveDamageClass",
    "HasMoveEffect",
    "HasMoveLearnMethod",
    "HasMoveTarget",
    "HasName",
    "HasNature",
    "HasOrder",
    "HasPokeathlonStat",
    "HasPokedex",
    "HasPokemon",
    "HasPokemonColor",
    "HasPokemonForm",
    "HasPokemonHabitat",
    "HasPokemonShape",
    "HasPokemonSpecies",
    "HasRegion",
    "HasShortEffect",
    "HasStat",
    "HasSuperContestEffect",
    "HasType",
    "HasTypeEfficacy",
    "HasVersion",
    "HasVersionGroup",
    "IsDescription",
    "IsFlavorText",
    "IsName",
    "Item",
    "ItemAttribute",
    "ItemAttributeDescription",
    "ItemAttributeMap",
    "ItemAttributeName",
    "ItemCategory",
    "ItemCategoryName",
    "ItemEffectText",
    "ItemFlavorText",
    "ItemFlingEffect",
    "ItemFlingEffectEffectText",
    "ItemGameIndex",
    "ItemName",
    "ItemPocket",
    "ItemPocketName",
    "ItemPrice",
    "ItemSprites",
    "Language",
    "LanguageName",
    "Location",
    "LocationArea",
    "LocationAreaEncounterRate",
    "LocationAreaName",
    "LocationGameIndex",
    "LocationName",
    "Machine",
    "Move",
    "MoveAttribute",
    "MoveAttributeDescription",
    "MoveAttributeMap",
    "MoveAttributeName",
    "MoveBattleStyle",
    "MoveBattleStyleName",
    "MoveChange",
    "MoveDamageClass",
    "MoveDamageClassDescription",
    "MoveDamageClassName",
    "MoveEffect",
    "MoveEffectChange",
    "MoveEffectChangeEffectText",
    "MoveEffectEffectText",
    "MoveFlavorText",
    "MoveLearnMethod",
    "MoveLearnMethodDescription",
    "MoveLearnMethodName",
    "MoveMeta",
    "MoveMetaAilment",
    "MoveMetaAilmentName",
    "MoveMetaCategory",
    "MoveMetaCategoryDescription",
    "MoveMetaStatChange",
    "MoveName",
    "MoveTarget",
    "MoveTargetDescription",
    "MoveTargetName",
    "Nature",
    "NatureBattleStylePreference",
    "NatureName",
    "NaturePokeathlonStat",
    "PalPark",
    "PalParkArea",
    "PalParkAreaName",
    "PokeApiModel",
    "PokeathlonStat",
    "PokeathlonStatName",
    "Pokedex",
    "PokedexDescription",
    "PokedexName",
    "PokedexVersionGroup",
    "Pokemon",
    "PokemonAbility",
    "PokemonAbilityPast",
    "PokemonColor",
    "PokemonColorName",
    "PokemonCries",
    "PokemonDexNumber",
    "PokemonEggGroup",
    "PokemonEvolution",
    "PokemonForm",
    "PokemonFormCondition",
    "PokemonFormGeneration",
    "PokemonFormName",
    "PokemonFormSprites",
    "PokemonFormTrigger",
    "PokemonFormType",
    "PokemonGameIndex",
    "PokemonHabitat",
    "PokemonHabitatName",
    "PokemonItem",
    "PokemonMove",
    "PokemonShape",
    "PokemonShapeName",
    "PokemonSpecies",
    "PokemonSpeciesDescription",
    "PokemonSpeciesFlavorText",
    "PokemonSpeciesName",
    "PokemonSprites",
    "PokemonStat",
    "PokemonStatPast",
    "PokemonType",
    "PokemonTypePast",
    "Region",
    "RegionName",
    "Stat",
    "StatName",
    "SuperContestCombo",
    "SuperContestEffect",
    "SuperContestEffectFlavorText",
    "Type",
    "TypeEfficacy",
    "TypeEfficacyPast",
    "TypeGameIndex",
    "TypeName",
    "TypeSprites",
    "Version",
    "VersionGroup",
    "VersionGroupMoveLearnMethod",
    "VersionGroupRegion",
    "VersionName",
)


############################
#  BASE MODEL FOR POKEAPI  #
############################


class PokeApiModel(models.Model):
    class Meta:
        abstract = True

    @override
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"


#####################
#  ABSTRACT MODELS  #
#####################


class HasAbility(PokeApiModel):
    ability = models.ForeignKey(
        "Ability",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class HasCharacteristic(PokeApiModel):
    characteristic = models.ForeignKey(
        "Characteristic",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class HasContestType(PokeApiModel):
    contest_type = models.ForeignKey(
        "ContestType",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class HasContestEffect(PokeApiModel):
    contest_effect = models.ForeignKey(
        "ContestEffect",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class HasCurrency(PokeApiModel):
    currency = models.ForeignKey(
        "Currency",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class HasSuperContestEffect(PokeApiModel):
    super_contest_effect = models.ForeignKey(
        "SuperContestEffect",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class HasDescription(PokeApiModel):
    description = models.CharField(max_length=2000, default="")

    class Meta:
        abstract = True


class HasGender(PokeApiModel):
    gender = models.ForeignKey(
        "Gender",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class HasEffect(PokeApiModel):
    effect = models.CharField(max_length=6000)

    class Meta:
        abstract = True


class HasEggGroup(PokeApiModel):
    egg_group = models.ForeignKey(
        "EggGroup",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class HasEncounterMethod(PokeApiModel):
    encounter_method = models.ForeignKey(
        "EncounterMethod",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class HasEncounterCondition(PokeApiModel):
    encounter_condition = models.ForeignKey(
        "EncounterCondition",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class HasEvolutionTrigger(PokeApiModel):
    evolution_trigger = models.ForeignKey(
        "EvolutionTrigger",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class HasFlavorText(PokeApiModel):
    flavor_text = models.CharField(max_length=500)

    class Meta:
        abstract = True


class HasFlingEffect(PokeApiModel):
    item_fling_effect = models.ForeignKey(
        "ItemFlingEffect",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class HasGameIndex(PokeApiModel):
    game_index = models.IntegerField()

    class Meta:
        abstract = True


class HasGeneration(PokeApiModel):
    generation = models.ForeignKey(
        "Generation",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class HasGrowthRate(PokeApiModel):
    growth_rate = models.ForeignKey(
        "GrowthRate",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class HasItem(PokeApiModel):
    item = models.ForeignKey(
        "Item",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class HasItemAttribute(PokeApiModel):
    item_attribute = models.ForeignKey(
        "ItemAttribute",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class HasItemCategory(PokeApiModel):
    item_category = models.ForeignKey(
        "ItemCategory",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class HasItemPocket(PokeApiModel):
    item_pocket = models.ForeignKey(
        "ItemPocket",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class HasLanguage(PokeApiModel):
    language = models.ForeignKey(
        "Language",
        blank=True,
        null=True,
        related_name="%(class)s_language",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class HasLocation(PokeApiModel):
    location = models.ForeignKey(
        "Location",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class HasLocationArea(PokeApiModel):
    location_area = models.ForeignKey(
        "LocationArea",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class HasMetaAilment(PokeApiModel):
    move_meta_ailment = models.ForeignKey(
        "MoveMetaAilment",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class HasMetaCategory(PokeApiModel):
    move_meta_category = models.ForeignKey(
        "MoveMetaCategory",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class HasMove(PokeApiModel):
    move = models.ForeignKey(
        "Move",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class HasMoveDamageClass(PokeApiModel):
    move_damage_class = models.ForeignKey(
        "MoveDamageClass",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class HasMoveEffect(PokeApiModel):
    move_effect = models.ForeignKey("MoveEffect", blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class HasMoveAttribute(PokeApiModel):
    move_attribute = models.ForeignKey("MoveAttribute", blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class HasMoveTarget(PokeApiModel):
    move_target = models.ForeignKey(
        "MoveTarget",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class HasName(PokeApiModel):
    name = models.CharField(max_length=200, db_index=True)

    class Meta:
        abstract = True


class HasNature(PokeApiModel):
    nature = models.ForeignKey(
        "Nature",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class HasOrder(PokeApiModel):
    order = models.IntegerField(blank=True, null=True)

    class Meta:
        abstract = True


class HasPokeathlonStat(PokeApiModel):
    pokeathlon_stat = models.ForeignKey(
        "PokeathlonStat",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class HasPokedex(PokeApiModel):
    pokedex = models.ForeignKey(
        "Pokedex",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class HasPokemon(PokeApiModel):
    pokemon = models.ForeignKey(
        "Pokemon",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class HasPokemonColor(PokeApiModel):
    pokemon_color = models.ForeignKey(
        "PokemonColor",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class HasPokemonForm(PokeApiModel):
    pokemon_form = models.ForeignKey(
        "PokemonForm",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class HasPokemonHabitat(PokeApiModel):
    pokemon_habitat = models.ForeignKey(
        "PokemonHabitat",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


# HasPokemonMoveMethod
class HasMoveLearnMethod(PokeApiModel):
    move_learn_method = models.ForeignKey(
        "MoveLearnMethod",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class HasPokemonShape(PokeApiModel):
    pokemon_shape = models.ForeignKey(
        "PokemonShape",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class HasPokemonSpecies(PokeApiModel):
    pokemon_species = models.ForeignKey(
        "PokemonSpecies",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class HasRegion(PokeApiModel):
    region = models.ForeignKey(
        "Region",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class HasShortEffect(PokeApiModel):
    short_effect = models.CharField(max_length=300)

    class Meta:
        abstract = True


class HasStat(PokeApiModel):
    stat = models.ForeignKey(
        "Stat",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class HasType(PokeApiModel):
    type = models.ForeignKey(
        "Type",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class HasTypeEfficacy(PokeApiModel):
    damage_type = models.ForeignKey(
        "Type",
        blank=True,
        null=True,
        related_name="%(class)s_damage_type",
        on_delete=models.CASCADE,
    )

    target_type = models.ForeignKey(
        "Type",
        blank=True,
        null=True,
        related_name="%(class)s_target_type",
        on_delete=models.CASCADE,
    )

    damage_factor = models.IntegerField()

    class Meta:
        abstract = True


class HasVersion(PokeApiModel):
    version = models.ForeignKey(
        "Version",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class HasVersionGroup(PokeApiModel):
    version_group = models.ForeignKey(
        "VersionGroup",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class IsDescription(HasLanguage, HasDescription):
    class Meta:
        abstract = True


class IsName(HasLanguage, HasName):
    class Meta:
        abstract = True


class IsFlavorText(HasLanguage, HasFlavorText):
    class Meta:
        abstract = True


####################
#  VERSION MODELS  #
####################


class Version(HasName, HasVersionGroup):
    pass


class VersionName(IsName, HasVersion):
    pass


class VersionGroup(HasName, HasGeneration, HasOrder):
    pass


class VersionGroupRegion(HasVersionGroup, HasRegion):
    pass


# VersionGroupPokemonMoveMethod
class VersionGroupMoveLearnMethod(HasVersionGroup, HasMoveLearnMethod):
    pass


#####################
#  LANGUAGE MODELS  #
#####################


class Language(HasName, HasOrder):
    iso639 = models.CharField(max_length=10)

    iso3166 = models.CharField(max_length=2)

    official = models.BooleanField(default=False)


class LanguageName(IsName):
    local_language = models.ForeignKey(
        "Language",
        blank=True,
        null=True,
        related_name="locallanguage",
        on_delete=models.CASCADE,
    )


#######################
#  GENERATION MODELS  #
#######################


class Generation(HasName):
    region = models.OneToOneField(
        "Region",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )


class GenerationName(IsName, HasGeneration):
    pass


###################
#  REGION MODELS  #
###################


class Region(HasName):
    pass


class RegionName(IsName, HasRegion):
    pass


####################
#  ABILITY MODELS  #
####################


class Ability(HasName, HasGeneration):
    is_main_series = models.BooleanField(default=False)


class AbilityEffectText(HasLanguage, HasEffect, HasShortEffect, HasAbility):
    pass


class AbilityFlavorText(IsFlavorText, HasAbility, HasVersionGroup):
    pass


class AbilityName(IsName, HasAbility):
    pass


class AbilityChange(HasAbility, HasVersionGroup):
    pass


class AbilityChangeEffectText(HasLanguage, HasEffect):
    ability_change = models.ForeignKey(
        AbilityChange,
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )


#################
#  TYPE MODELS  #
#################


class Type(HasName, HasGeneration, HasMoveDamageClass):
    pass


class TypeName(IsName, HasType):
    pass


class TypeGameIndex(HasType, HasGeneration, HasGameIndex):
    pass


class TypeEfficacy(HasTypeEfficacy):
    pass


# model for a type's efficacy that was used until a given generation
class TypeEfficacyPast(HasTypeEfficacy, HasGeneration):
    pass


class TypeSprites(HasType):
    sprites: models.JSONField[Any] = models.JSONField()


#################
#  STAT MODELS  #
#################


class Stat(HasName, HasMoveDamageClass):
    is_battle_only = models.BooleanField(default=False)

    game_index = models.IntegerField()


class StatName(IsName, HasStat):
    pass


###########################
#  CHARACTERISTIC MODELS  #
###########################


class Characteristic(HasStat):
    gene_mod_5 = models.IntegerField()


class CharacteristicDescription(HasCharacteristic, IsDescription):
    pass


######################
#  EGG GROUP MODELS  #
######################


class EggGroup(HasName):
    pass


class EggGroupName(IsName, HasEggGroup):
    pass


#################
#  ITEM MODELS  #
#################


class Currency(HasName):
    pass


class CurrencyName(IsName, HasCurrency, HasLanguage):
    pass


class ItemPocket(HasName):
    pass


class ItemPocketName(IsName, HasItemPocket):
    pass


class ItemCategory(HasName, HasItemPocket):
    pass


class ItemCategoryName(IsName, HasItemCategory):
    pass


class ItemFlingEffect(HasName):
    pass


class ItemFlingEffectEffectText(HasLanguage, HasEffect, HasFlingEffect):
    pass


class Item(HasName, HasItemCategory, HasFlingEffect):
    fling_power = models.IntegerField(blank=True, null=True)


class ItemEffectText(HasItem, HasLanguage, HasEffect, HasShortEffect):
    pass


class ItemName(HasItem, IsName):
    pass


class ItemFlavorText(HasItem, HasVersionGroup, IsFlavorText):
    pass


class ItemAttribute(HasName):
    pass


class ItemAttributeName(IsName, HasItemAttribute):
    pass


class ItemAttributeDescription(IsDescription, HasItemAttribute):
    pass


class ItemAttributeMap(HasItem, HasItemAttribute):
    pass


class ItemGameIndex(HasItem, HasGeneration, HasGameIndex):
    pass


class ItemPrice(HasItem, HasVersionGroup, HasCurrency):
    purchase_price = models.IntegerField(blank=True, null=True)
    sell_price = models.IntegerField(blank=True, null=True)


class ItemSprites(HasItem):
    sprites: models.JSONField[Any] = models.JSONField()


####################
#  CONTEST MODELS  #
####################


class ContestType(HasName):
    pass


class ContestTypeName(HasContestType, IsName):
    flavor = models.CharField(max_length=10)

    color = models.CharField(max_length=10)


class ContestEffect(PokeApiModel):
    appeal = models.IntegerField()

    jam = models.IntegerField()


class ContestEffectEffectText(HasLanguage, HasEffect, HasContestEffect):
    pass


class ContestEffectFlavorText(HasLanguage, HasFlavorText, HasContestEffect):
    pass


class ContestCombo(PokeApiModel):
    first_move = models.ForeignKey(
        "Move",
        blank=True,
        null=True,
        related_name="first_move",
        on_delete=models.CASCADE,
    )

    second_move = models.ForeignKey(
        "Move",
        blank=True,
        null=True,
        related_name="second_move",
        on_delete=models.CASCADE,
    )


##################
#  BERRY MODELS  #
##################


class BerryFirmness(HasName):
    pass


class BerryFirmnessName(IsName):
    berry_firmness = models.ForeignKey(
        BerryFirmness,
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )


class Berry(HasName, HasItem):
    berry_firmness = models.ForeignKey(
        BerryFirmness,
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    natural_gift_power = models.IntegerField(blank=True, null=True)

    natural_gift_type = models.ForeignKey(
        Type, blank=True, null=True, related_name="%(class)s", on_delete=models.CASCADE
    )

    size = models.IntegerField(blank=True, null=True)

    max_harvest = models.IntegerField(blank=True, null=True)

    growth_time = models.IntegerField(blank=True, null=True)

    soil_dryness = models.IntegerField(blank=True, null=True)

    smoothness = models.IntegerField(blank=True, null=True)


# Berry Flavors are a bit of a hack because their relationship
# in terms of flavors to contest types is really awkward the
# way it was handled in the veekun data set. Berry Flavor here
# does not match the csv table. Berry Flavor Map
# is a table fabricated just to suit this project.


class BerryFlavor(HasName):
    contest_type = models.OneToOneField(
        "ContestType",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )


class BerryFlavorName(IsName):
    berry_flavor = models.ForeignKey(
        BerryFlavor,
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )


class BerryFlavorMap(PokeApiModel):
    berry = models.ForeignKey(Berry, blank=True, null=True, related_name="%(class)s", on_delete=models.CASCADE)

    berry_flavor = models.ForeignKey(
        BerryFlavor,
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    potency = models.IntegerField()


########################
#  GROWTH RATE MODELS  #
########################


class GrowthRate(HasName):
    formula = models.CharField(max_length=500)


class GrowthRateDescription(HasGrowthRate, IsDescription):
    pass


###################
#  NATURE MODELS  #
###################


class Nature(HasName):
    decreased_stat = models.ForeignKey(Stat, blank=True, null=True, related_name="decreased", on_delete=models.CASCADE)

    increased_stat = models.ForeignKey(Stat, blank=True, null=True, related_name="increased", on_delete=models.CASCADE)

    hates_flavor = models.ForeignKey(
        BerryFlavor,
        blank=True,
        null=True,
        related_name="hates_flavor",
        on_delete=models.CASCADE,
    )

    likes_flavor = models.ForeignKey(
        BerryFlavor,
        blank=True,
        null=True,
        related_name="likes_flavor",
        on_delete=models.CASCADE,
    )

    game_index = models.IntegerField()


class NatureName(IsName, HasNature):
    pass


class NaturePokeathlonStat(HasNature, HasPokeathlonStat):
    max_change = models.IntegerField()


class NatureBattleStylePreference(HasNature):
    move_battle_style = models.ForeignKey(
        "MoveBattleStyle",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    low_hp_preference = models.IntegerField()

    high_hp_preference = models.IntegerField()


#####################
#  LOCATION MODELS  #
#####################


class Location(HasRegion, HasName):
    pass


class LocationName(HasLocation, IsName):
    pass


class LocationGameIndex(HasLocation, HasGeneration, HasGameIndex):
    pass


class LocationArea(HasLocation, HasGameIndex, HasName):
    pass


class LocationAreaName(IsName, HasLocationArea):
    pass


class LocationAreaEncounterRate(HasEncounterMethod, HasLocationArea, HasVersion):
    rate = models.IntegerField()


######################
#  ENCOUNTER MODELS  #
######################


class EncounterMethod(HasName, HasOrder):
    pass


class EncounterMethodName(HasEncounterMethod, IsName):
    pass


class EncounterSlot(HasVersionGroup, HasEncounterMethod):
    slot = models.IntegerField(blank=True, null=True)

    rarity = models.IntegerField()


class Encounter(HasVersion, HasLocationArea, HasPokemon):
    encounter_slot = models.ForeignKey(EncounterSlot, blank=True, null=True, on_delete=models.CASCADE)

    min_level = models.IntegerField()

    max_level = models.IntegerField()


class EncounterCondition(HasName):
    pass


class EncounterConditionName(HasEncounterCondition, IsName):
    pass


class EncounterConditionValue(HasEncounterCondition, HasName):
    is_default = models.BooleanField(default=False)


class EncounterConditionValueName(IsName):
    encounter_condition_value = models.ForeignKey(
        EncounterConditionValue,
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )


class EncounterConditionValueMap(PokeApiModel):
    encounter = models.ForeignKey(Encounter, blank=True, null=True, on_delete=models.CASCADE)

    encounter_condition_value = models.ForeignKey(
        EncounterConditionValue, blank=True, null=True, on_delete=models.CASCADE
    )


class EncounterPokemonDetail(PokeApiModel):
    encounter = models.ForeignKey(Encounter, blank=True, null=True, on_delete=models.CASCADE)

    min_perfect_ivs = models.IntegerField(blank=True, null=True)

    always_shiny = models.BooleanField(default=False)

    never_shiny = models.BooleanField(default=False)

    is_alpha = models.BooleanField(default=False)


#################
#  MOVE MODELS  #
#################


class Move(
    HasName,
    HasGeneration,
    HasType,
    HasMoveDamageClass,
    HasMoveEffect,
    HasMoveTarget,
    HasContestType,
    HasContestEffect,
    HasSuperContestEffect,
):
    power = models.IntegerField(blank=True, null=True)

    pp = models.IntegerField(blank=True, null=True)

    accuracy = models.IntegerField(blank=True, null=True)

    priority = models.IntegerField(blank=True, null=True)

    move_effect_chance = models.IntegerField(blank=True, null=True)


class MoveName(HasMove, IsName):
    pass


class MoveFlavorText(HasMove, HasVersionGroup, IsFlavorText):
    pass


class MoveChange(HasMove, HasVersionGroup, HasType, HasMoveEffect):
    power = models.IntegerField(blank=True, null=True)

    pp = models.IntegerField(blank=True, null=True)

    accuracy = models.IntegerField(blank=True, null=True)

    move_effect_chance = models.IntegerField(blank=True, null=True)


##############################
#  MOVE DAMAGE CLASS MODELS  #
##############################


class MoveDamageClass(HasName):
    pass


class MoveDamageClassName(HasMoveDamageClass, IsName):
    pass


class MoveDamageClassDescription(HasMoveDamageClass, IsDescription):
    pass


##############################
#  MOVE BATTLE STYLE MODELS  #
##############################


class MoveBattleStyle(HasName):
    pass


class MoveBattleStyleName(IsName):
    move_battle_style = models.ForeignKey(
        MoveBattleStyle,
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )


########################
#  MOVE EFFECT MODELS  #
########################


class MoveEffect(PokeApiModel):
    pass


class MoveEffectEffectText(HasLanguage, HasMoveEffect, HasEffect, HasShortEffect):
    pass


class MoveEffectChange(HasMoveEffect, HasVersionGroup):
    pass


class MoveEffectChangeEffectText(HasLanguage, HasEffect):
    move_effect_change = models.ForeignKey(
        "MoveEffectChange",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )


################################
#  MOVE FLAG/ATTRIBUTE MODELS  #
################################


class MoveAttribute(HasName):
    pass


class MoveAttributeName(HasMoveAttribute, IsName):
    pass


class MoveAttributeDescription(HasMoveAttribute, IsDescription):
    pass


class MoveAttributeMap(HasMove, HasMoveAttribute):
    pass


########################
#  MOVE TARGET MODELS  #
########################


class MoveTarget(HasName):
    pass


class MoveTargetName(HasMoveTarget, IsName):
    pass


class MoveTargetDescription(HasMoveTarget, IsDescription):
    pass


######################
#  MOVE META MODELS  #
######################


class MoveMeta(HasMetaAilment, HasMetaCategory):
    move = models.OneToOneField(
        Move,
        blank=False,
        null=False,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    min_hits = models.IntegerField(blank=True, null=True)

    max_hits = models.IntegerField(blank=True, null=True)

    min_turns = models.IntegerField(blank=True, null=True)

    max_turns = models.IntegerField(blank=True, null=True)

    drain = models.IntegerField(blank=True, null=True)

    healing = models.IntegerField(blank=True, null=True)

    crit_rate = models.IntegerField(blank=True, null=True)

    ailment_chance = models.IntegerField(blank=True, null=True)

    flinch_chance = models.IntegerField(blank=True, null=True)

    stat_chance = models.IntegerField(blank=True, null=True)


class MoveMetaAilment(HasName):
    pass


class MoveMetaAilmentName(HasMetaAilment, IsName):
    pass


class MoveMetaCategory(HasName):
    pass


class MoveMetaCategoryDescription(HasMetaCategory, IsDescription):
    pass


class MoveMetaStatChange(HasMove, HasStat):
    change = models.IntegerField()


#######################
#  EXPERIENCE MODELS  #
#######################


class Experience(HasGrowthRate):
    level = models.IntegerField()

    experience = models.IntegerField()


###################
#  GENDER MODELS  #
###################


class Gender(HasName):
    pass


####################
#  MACHINE MODELS  #
####################


class Machine(HasGrowthRate, HasItem):
    machine_number = models.IntegerField()

    version_group = models.ForeignKey(VersionGroup, blank=True, null=True, on_delete=models.CASCADE)

    move = models.ForeignKey(Move, blank=True, null=True, on_delete=models.CASCADE)


#######################
#  POKEATHLON MODELS  #
#######################


class PokeathlonStat(HasName):
    pass


class PokeathlonStatName(IsName, HasPokeathlonStat):
    pass


#####################
#  PAL PARK MODELS  #
#####################


class PalParkArea(HasName):
    pass


class PalParkAreaName(IsName):
    pal_park_area = models.ForeignKey(
        PalParkArea,
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )


class PalPark(HasPokemonSpecies):
    pal_park_area = models.ForeignKey(
        PalParkArea,
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    base_score = models.IntegerField(blank=True, null=True)

    rate = models.IntegerField()


##########################
#  SUPER CONTEST MODELS  #
##########################


class SuperContestEffect(PokeApiModel):
    appeal = models.IntegerField()


class SuperContestEffectFlavorText(IsFlavorText, HasSuperContestEffect):
    pass


class SuperContestCombo(PokeApiModel):
    first_move = models.ForeignKey(Move, blank=True, null=True, related_name="first", on_delete=models.CASCADE)

    second_move = models.ForeignKey(Move, blank=True, null=True, related_name="second", on_delete=models.CASCADE)


######################
#  EVOLUTION MODELS  #
######################


class EvolutionChain(PokeApiModel):
    baby_trigger_item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.CASCADE)


class EvolutionTrigger(HasName):
    pass


class EvolutionTriggerName(HasEvolutionTrigger, IsName):
    pass


####################
#  POKEDEX MODELS  #
####################


class Pokedex(HasName, HasRegion):
    is_main_series = models.BooleanField(default=False)


class PokedexName(HasPokedex, IsName):
    pass


class PokedexDescription(HasPokedex, IsDescription):
    pass


class PokedexVersionGroup(HasPokedex, HasVersionGroup):
    pass


####################
#  POKEMON MODELS  #
####################


class PokemonSpecies(HasName, HasGeneration, HasPokemonColor, HasPokemonShape, HasGrowthRate, HasOrder):
    evolves_from_species = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE)

    evolution_chain = models.ForeignKey(EvolutionChain, blank=True, null=True, on_delete=models.CASCADE)

    pokemon_habitat = models.ForeignKey(
        "PokemonHabitat",
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )

    gender_rate = models.IntegerField(blank=True, null=True)

    capture_rate = models.IntegerField(blank=True, null=True)

    base_happiness = models.IntegerField(blank=True, null=True)

    is_baby = models.BooleanField(default=False)

    is_legendary = models.BooleanField(default=False)

    is_mythical = models.BooleanField(default=False)

    hatch_counter = models.IntegerField(blank=True, null=True)

    has_gender_differences = models.BooleanField(default=False)

    forms_switchable = models.BooleanField(default=False)


class PokemonSpeciesName(IsName, HasPokemonSpecies):
    genus = models.CharField(max_length=30)


class PokemonSpeciesDescription(HasPokemonSpecies, IsDescription):
    pass


class PokemonSpeciesFlavorText(IsFlavorText, HasPokemonSpecies, HasVersion):
    pass


class Pokemon(HasName, HasPokemonSpecies, HasOrder):
    height = models.IntegerField(blank=True, null=True)

    weight = models.IntegerField(blank=True, null=True)

    base_experience = models.IntegerField(blank=True, null=True)

    is_default = models.BooleanField(default=False)


class PokemonAbility(HasPokemon, HasAbility):
    is_hidden = models.BooleanField(default=False)

    slot = models.IntegerField()


# model for a Pokemon's abilities that were used until a given generation
class PokemonAbilityPast(HasPokemon, HasAbility, HasGeneration):
    is_hidden = models.BooleanField(default=False)

    slot = models.IntegerField()


class PokemonColor(HasName):
    pass


class PokemonColorName(HasPokemonColor, IsName):
    pass


class PokemonDexNumber(HasPokemonSpecies, HasPokedex):
    pokedex_number = models.IntegerField()


class PokemonEggGroup(HasPokemonSpecies, HasEggGroup):
    pass


class PokemonEvolution(HasEvolutionTrigger, HasGender):
    evolution_item = models.ForeignKey(
        Item,
        blank=True,
        null=True,
        related_name="evolution_item",
        on_delete=models.CASCADE,
    )

    evolved_species = models.ForeignKey(
        PokemonSpecies,
        related_name="evolved_species",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    version_group = models.ForeignKey(
        VersionGroup,
        related_name="version_group",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    is_default = models.BooleanField(default=False)

    min_level = models.IntegerField(blank=True, null=True)

    location = models.ForeignKey(
        Location,
        related_name="location",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    held_item = models.ForeignKey(Item, blank=True, null=True, related_name="held_item", on_delete=models.CASCADE)

    time_of_day = models.CharField(max_length=10, blank=True, default="")

    known_move = models.ForeignKey(Move, blank=True, null=True, on_delete=models.CASCADE)

    known_move_type = models.ForeignKey(
        Type, related_name="known_move", blank=True, null=True, on_delete=models.CASCADE
    )

    min_happiness = models.IntegerField(blank=True, null=True)

    min_beauty = models.IntegerField(blank=True, null=True)

    min_affection = models.IntegerField(blank=True, null=True)

    relative_physical_stats = models.IntegerField(blank=True, null=True)

    party_species = models.ForeignKey(
        PokemonSpecies,
        related_name="party_species",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    party_type = models.ForeignKey(Type, related_name="party_type", blank=True, null=True, on_delete=models.CASCADE)

    trade_species = models.ForeignKey(
        PokemonSpecies,
        related_name="trade_species",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    needs_overworld_rain = models.BooleanField(default=False)

    turn_upside_down = models.BooleanField(default=False)

    needs_multiplayer = models.BooleanField(default=False)

    near_special_rock = models.BooleanField(default=False)

    # Regional evolution fields
    region = models.ForeignKey(
        "Region",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        help_text="Region where this evolution can occur (null = any region)",
    )

    base_form = models.ForeignKey(
        "Pokemon",
        blank=True,
        null=True,
        related_name="base_form_evolutions",
        on_delete=models.CASCADE,
        help_text="Specific form required for evolution (null = any form)",
    )

    evolved_form = models.ForeignKey(
        "Pokemon",
        blank=True,
        null=True,
        related_name="evolved_form",
        on_delete=models.CASCADE,
        help_text="Specific form of the evolved species",
    )

    used_move = models.ForeignKey(Move, related_name="used_move", blank=True, null=True, on_delete=models.CASCADE)

    min_move_count = models.IntegerField(blank=True, null=True)

    min_steps = models.IntegerField(blank=True, null=True)

    min_damage_taken = models.IntegerField(blank=True, null=True)


class PokemonForm(HasName, HasPokemon, HasOrder):
    form_name = models.CharField(max_length=30)

    version_group = models.ForeignKey(VersionGroup, blank=True, null=True, on_delete=models.CASCADE)

    is_default = models.BooleanField(default=False)

    is_battle_only = models.BooleanField(default=False)

    is_mega = models.BooleanField(default=False)

    form_order = models.IntegerField(blank=True, null=True)


class PokemonFormGeneration(HasPokemonForm, HasGeneration, HasGameIndex):
    pass


class PokemonFormName(HasPokemonForm, IsName):
    pokemon_name = models.CharField(max_length=60)


class PokemonFormSprites(HasPokemonForm):
    sprites: models.JSONField[Any] = models.JSONField()


class PokemonFormTrigger(HasName):
    pass


class PokemonFormCondition(HasPokemonForm):
    form_trigger = models.ForeignKey(PokemonFormTrigger, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.CASCADE)
    ability = models.ForeignKey(Ability, blank=True, null=True, on_delete=models.CASCADE)
    move = models.ForeignKey(Move, blank=True, null=True, on_delete=models.CASCADE)
    base_form = models.ForeignKey(
        PokemonForm,
        blank=True,
        null=True,
        related_name="base_form_conditions",
        on_delete=models.CASCADE,
    )


class PokemonGameIndex(HasPokemon, HasGameIndex, HasVersion):
    pass


class PokemonHabitat(HasName):
    pass


class PokemonHabitatName(IsName):
    pokemon_habitat = models.ForeignKey(
        PokemonHabitat,
        blank=True,
        null=True,
        related_name="%(class)s",
        on_delete=models.CASCADE,
    )


class PokemonItem(HasPokemon, HasVersion, HasItem):
    rarity = models.IntegerField()


# PokemonMoveMethod
class MoveLearnMethod(HasName):
    pass


# PokemonMoveMethodName
class MoveLearnMethodName(IsName, HasMoveLearnMethod):
    pass


class MoveLearnMethodDescription(IsDescription, HasMoveLearnMethod):
    pass


class PokemonMove(HasPokemon, HasMoveLearnMethod, HasVersionGroup, HasMove, HasOrder):
    level = models.IntegerField()
    mastery = models.IntegerField(null=True, blank=True)


class PokemonShape(HasName):
    pass


class PokemonShapeName(IsName):
    awesome_name = models.CharField(max_length=30)

    pokemon_shape = models.ForeignKey(
        PokemonShape,
        blank=True,
        null=True,
        related_name="pokemonshapename",
        on_delete=models.CASCADE,
    )


class PokemonStat(HasPokemon, HasStat):
    base_stat = models.IntegerField()

    effort = models.IntegerField()


class PokemonStatPast(HasPokemon, HasStat, HasGeneration):
    base_stat = models.IntegerField()

    effort = models.IntegerField()


class PokemonType(HasPokemon, HasType):
    slot = models.IntegerField()


class PokemonFormType(HasPokemonForm, HasType):
    slot = models.IntegerField()


# model for a Pokemon's types that were used until a given generation
class PokemonTypePast(HasPokemon, HasType, HasGeneration):
    slot = models.IntegerField()


class PokemonSprites(HasPokemon):
    sprites: models.JSONField[Any] = models.JSONField()


class PokemonCries(HasPokemon):
    cries: models.JSONField[Any] = models.JSONField()
