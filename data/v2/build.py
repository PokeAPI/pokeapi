#  To build out the data you'll need to jump into the Django shell
#
#     $ uv run manage.py shell
#
#  and run the build script with
#
#     $ from data.v2.build import build_all
#     $ build_all()
#
#  Each time the build script is run it will iterate over each table in the database,
#  wipe it and rewrite each row using the data found in data/v2/csv.


import re
from collections.abc import Iterator
from copy import deepcopy

from data.v2.utils.helpers import build_generic, load_data
from data.v2.utils.media import (
    POKEMON_SPRITE_CONFIG,
    TYPE_SPRITE_GAME_MAP,
    file_path_or_none,
    pokemon_form_sprite_lookup,
    pokemon_sprite_lookup,
    resolve_sprite_config,
)
from pokemon_v2.models import (
    Ability,
    AbilityChange,
    AbilityChangeEffectText,
    AbilityEffectText,
    AbilityFlavorText,
    AbilityName,
    Berry,
    BerryFirmness,
    BerryFirmnessName,
    BerryFlavor,
    BerryFlavorMap,
    BerryFlavorName,
    Characteristic,
    CharacteristicDescription,
    ContestCombo,
    ContestEffect,
    ContestEffectEffectText,
    ContestEffectFlavorText,
    ContestType,
    ContestTypeName,
    Currency,
    CurrencyName,
    EggGroup,
    EggGroupName,
    Encounter,
    EncounterCondition,
    EncounterConditionName,
    EncounterConditionValue,
    EncounterConditionValueMap,
    EncounterConditionValueName,
    EncounterMethod,
    EncounterMethodName,
    EncounterPokemonDetail,
    EncounterSlot,
    EvolutionChain,
    EvolutionTrigger,
    EvolutionTriggerName,
    EvolutionVariable,
    EvolutionVariableDescription,
    EvolutionVariableName,
    Experience,
    Gender,
    Generation,
    GenerationName,
    GrowthRate,
    GrowthRateDescription,
    Item,
    ItemAttribute,
    ItemAttributeDescription,
    ItemAttributeMap,
    ItemAttributeName,
    ItemCategory,
    ItemCategoryName,
    ItemEffectText,
    ItemFlavorText,
    ItemFlingEffect,
    ItemFlingEffectEffectText,
    ItemGameIndex,
    ItemName,
    ItemPocket,
    ItemPocketName,
    ItemPrice,
    ItemSprites,
    Language,
    LanguageName,
    Location,
    LocationArea,
    LocationAreaEncounterRate,
    LocationAreaName,
    LocationGameIndex,
    LocationName,
    Machine,
    Move,
    MoveAttribute,
    MoveAttributeDescription,
    MoveAttributeMap,
    MoveAttributeName,
    MoveBattleStyle,
    MoveBattleStyleName,
    MoveChange,
    MoveDamageClass,
    MoveDamageClassDescription,
    MoveDamageClassName,
    MoveEffect,
    MoveEffectChange,
    MoveEffectChangeEffectText,
    MoveEffectEffectText,
    MoveFlavorText,
    MoveLearnMethod,
    MoveLearnMethodDescription,
    MoveLearnMethodName,
    MoveMeta,
    MoveMetaAilment,
    MoveMetaAilmentName,
    MoveMetaCategory,
    MoveMetaCategoryDescription,
    MoveMetaStatChange,
    MoveName,
    MoveTarget,
    MoveTargetDescription,
    MoveTargetName,
    Nature,
    NatureBattleStylePreference,
    NatureName,
    NaturePokeathlonStat,
    PalPark,
    PalParkArea,
    PalParkAreaName,
    PokeathlonStat,
    PokeathlonStatName,
    Pokedex,
    PokedexDescription,
    PokedexName,
    PokedexVersionGroup,
    Pokemon,
    PokemonAbility,
    PokemonAbilityPast,
    PokemonColor,
    PokemonColorName,
    PokemonCries,
    PokemonDexNumber,
    PokemonEggGroup,
    PokemonEvolution,
    PokemonForm,
    PokemonFormCondition,
    PokemonFormFlavorText,
    PokemonFormGeneration,
    PokemonFormName,
    PokemonFormSprites,
    PokemonFormTrigger,
    PokemonFormType,
    PokemonGameIndex,
    PokemonHabitat,
    PokemonHabitatName,
    PokemonItem,
    PokemonMove,
    PokemonShape,
    PokemonShapeName,
    PokemonSpecies,
    PokemonSpeciesDescription,
    PokemonSpeciesFlavorText,
    PokemonSpeciesName,
    PokemonSprites,
    PokemonStat,
    PokemonStatPast,
    PokemonType,
    PokemonTypePast,
    Region,
    RegionName,
    Stat,
    StatName,
    SuperContestCombo,
    SuperContestEffect,
    SuperContestEffectFlavorText,
    Type,
    TypeEfficacy,
    TypeEfficacyPast,
    TypeGameIndex,
    TypeName,
    TypeSprites,
    Version,
    VersionGroup,
    VersionGroupMoveLearnMethod,
    VersionGroupRegion,
    VersionName,
)


def _build_languages() -> None:
    def languages_from_rows(info: list[str]) -> Iterator[Language]:
        yield Language(
            id=int(info[0]),
            iso639=info[1],
            iso3166=info[2],
            name=info[3],
            official=bool(int(info[4])),
            order=info[5],
        )

    build_generic((Language,), "languages.csv", languages_from_rows)

    def language_names_from_rows(info: list[str]) -> Iterator[LanguageName]:
        yield LanguageName(language_id=int(info[0]), local_language_id=int(info[1]), name=info[2])

    build_generic((LanguageName,), "language_names.csv", language_names_from_rows)


def _build_regions() -> None:
    def regions_from_rows(info: list[str]) -> Iterator[Region]:
        yield Region(id=int(info[0]), name=info[1])

    build_generic((Region,), "regions.csv", regions_from_rows)

    def region_names_from_rows(info: list[str]) -> Iterator[RegionName]:
        yield RegionName(region_id=int(info[0]), language_id=int(info[1]), name=info[2])

    build_generic((RegionName,), "region_names.csv", region_names_from_rows)


def _build_generations() -> None:
    def generations_from_rows(info: list[str]) -> Iterator[Generation]:
        yield Generation(id=int(info[0]), region_id=int(info[1]), name=info[2])

    build_generic((Generation,), "generations.csv", generations_from_rows)

    def generation_names_from_rows(info: list[str]) -> Iterator[GenerationName]:
        yield GenerationName(generation_id=int(info[0]), language_id=int(info[1]), name=info[2])

    build_generic((GenerationName,), "generation_names.csv", generation_names_from_rows)


def _build_versions() -> None:
    def version_groups_from_rows(info: list[str]) -> Iterator[VersionGroup]:
        yield VersionGroup(
            id=int(info[0]),
            name=info[1],
            generation_id=int(info[2]),
            order=int(info[3]),
        )

    build_generic((VersionGroup,), "version_groups.csv", version_groups_from_rows)

    def version_group_regions_from_rows(info: list[str]) -> Iterator[VersionGroupRegion]:
        yield VersionGroupRegion(version_group_id=int(info[0]), region_id=int(info[1]))

    build_generic((VersionGroupRegion,), "version_group_regions.csv", version_group_regions_from_rows)

    def versions_from_rows(info: list[str]) -> Iterator[Version]:
        yield Version(id=int(info[0]), version_group_id=int(info[1]), name=info[2])

    build_generic((Version,), "versions.csv", versions_from_rows)

    def version_names_from_rows(info: list[str]) -> Iterator[VersionName]:
        yield VersionName(version_id=int(info[0]), language_id=int(info[1]), name=info[2])

    build_generic((VersionName,), "version_names.csv", version_names_from_rows)


def _build_damage_classes() -> None:
    def move_damage_classes_from_rows(info: list[str]) -> Iterator[MoveDamageClass]:
        yield MoveDamageClass(id=int(info[0]), name=info[1])

    build_generic((MoveDamageClass,), "move_damage_classes.csv", move_damage_classes_from_rows)

    def move_damage_class_prose_from_rows(
        info: list[str],
    ) -> Iterator[MoveDamageClassName | MoveDamageClassDescription]:
        yield MoveDamageClassName(move_damage_class_id=int(info[0]), language_id=int(info[1]), name=info[2])
        yield MoveDamageClassDescription(
            move_damage_class_id=int(info[0]),
            language_id=int(info[1]),
            description=info[3],
        )

    build_generic(
        (MoveDamageClassName, MoveDamageClassDescription),
        "move_damage_class_prose.csv",
        move_damage_class_prose_from_rows,
    )


def _build_stats() -> None:
    def stats_from_rows(info: list[str]) -> Iterator[Stat]:
        yield Stat(
            id=int(info[0]),
            move_damage_class_id=int(info[1]) if info[1] != "" else None,
            name=info[2],
            is_battle_only=bool(int(info[3])),
            game_index=int(info[4]) if info[4] else 0,
        )

    build_generic((Stat,), "stats.csv", stats_from_rows)

    def stat_names_from_rows(info: list[str]) -> Iterator[StatName]:
        yield StatName(stat_id=int(info[0]), language_id=int(info[1]), name=info[2])

    build_generic((StatName,), "stat_names.csv", stat_names_from_rows)

    def pokeathlon_stats_from_rows(info: list[str]) -> Iterator[PokeathlonStat]:
        yield PokeathlonStat(id=int(info[0]), name=info[1])

    build_generic((PokeathlonStat,), "pokeathlon_stats.csv", pokeathlon_stats_from_rows)

    def pokeathlon_stat_names_from_rows(info: list[str]) -> Iterator[PokeathlonStatName]:
        yield PokeathlonStatName(pokeathlon_stat_id=int(info[0]), language_id=int(info[1]), name=info[2])

    build_generic((PokeathlonStatName,), "pokeathlon_stat_names.csv", pokeathlon_stat_names_from_rows)


def _build_abilities() -> None:
    def abilities_from_rows(info: list[str]) -> Iterator[Ability]:
        yield Ability(
            id=int(info[0]),
            name=info[1],
            generation_id=int(info[2]),
            is_main_series=bool(int(info[3])),
        )

    build_generic((Ability,), "abilities.csv", abilities_from_rows)

    def ability_names_from_rows(info: list[str]) -> Iterator[AbilityName]:
        yield AbilityName(ability_id=int(info[0]), language_id=int(info[1]), name=info[2])

    build_generic((AbilityName,), "ability_names.csv", ability_names_from_rows)

    def ability_changes_from_rows(info: list[str]) -> Iterator[AbilityChange]:
        yield AbilityChange(id=int(info[0]), ability_id=int(info[1]), version_group_id=int(info[2]))

    build_generic((AbilityChange,), "ability_changelog.csv", ability_changes_from_rows)

    def ability_effect_texts_from_rows(info: list[str]) -> Iterator[AbilityEffectText]:
        yield AbilityEffectText(
            ability_id=int(info[0]),
            language_id=int(info[1]),
            short_effect=info[2],
            effect=info[3],
        )

    build_generic((AbilityEffectText,), "ability_prose.csv", ability_effect_texts_from_rows)

    def ability_change_effect_texts_from_rows(info: list[str]) -> Iterator[AbilityChangeEffectText]:
        yield AbilityChangeEffectText(
            ability_change_id=int(info[0]),
            language_id=int(info[1]),
            effect=info[2],
        )

    build_generic((AbilityChangeEffectText,), "ability_changelog_prose.csv", ability_change_effect_texts_from_rows)

    def ability_flavor_texts_from_rows(info: list[str]) -> Iterator[AbilityFlavorText]:
        yield AbilityFlavorText(
            ability_id=int(info[0]),
            version_group_id=int(info[1]),
            language_id=int(info[2]),
            flavor_text=info[3],
        )

    build_generic((AbilityFlavorText,), "ability_flavor_text.csv", ability_flavor_texts_from_rows)


def _build_characteristics() -> None:
    def characteristics_from_rows(info: list[str]) -> Iterator[Characteristic]:
        yield Characteristic(id=int(info[0]), stat_id=int(info[1]), gene_mod_5=int(info[2]))

    build_generic((Characteristic,), "characteristics.csv", characteristics_from_rows)

    def characteristic_descriptions_from_rows(info: list[str]) -> Iterator[CharacteristicDescription]:
        yield CharacteristicDescription(
            characteristic_id=int(info[0]),
            language_id=int(info[1]),
            description=info[2],
        )

    build_generic((CharacteristicDescription,), "characteristic_text.csv", characteristic_descriptions_from_rows)


def _build_egg_groups() -> None:
    def egg_groups_from_rows(info: list[str]) -> Iterator[EggGroup]:
        yield EggGroup(id=int(info[0]), name=info[1])

    build_generic((EggGroup,), "egg_groups.csv", egg_groups_from_rows)

    def egg_group_names_from_rows(info: list[str]) -> Iterator[EggGroupName]:
        yield EggGroupName(egg_group_id=int(info[0]), language_id=int(info[1]), name=info[2])

    build_generic((EggGroupName,), "egg_group_prose.csv", egg_group_names_from_rows)


def _build_growth_rates() -> None:
    def growth_rates_from_rows(info: list[str]) -> Iterator[GrowthRate]:
        yield GrowthRate(id=int(info[0]), name=info[1], formula=info[2])

    build_generic((GrowthRate,), "growth_rates.csv", growth_rates_from_rows)

    def growth_rate_descriptions_from_rows(info: list[str]) -> Iterator[GrowthRateDescription]:
        yield GrowthRateDescription(growth_rate_id=int(info[0]), language_id=int(info[1]), description=info[2])

    build_generic((GrowthRateDescription,), "growth_rate_prose.csv", growth_rate_descriptions_from_rows)


def _build_items() -> None:
    def currencies_from_rows(info: list[str]) -> Iterator[Currency]:
        yield Currency(id=int(info[0]), name=info[1])

    build_generic((Currency,), "currencies.csv", currencies_from_rows)

    def currency_names_from_rows(info: list[str]) -> Iterator[CurrencyName]:
        yield CurrencyName(currency_id=int(info[0]), language_id=int(info[1]), name=info[2])

    build_generic((CurrencyName,), "currency_names.csv", currency_names_from_rows)

    def item_pockets_from_rows(info: list[str]) -> Iterator[ItemPocket]:
        yield ItemPocket(id=int(info[0]), name=info[1])

    build_generic((ItemPocket,), "item_pockets.csv", item_pockets_from_rows)

    def item_pocket_names_from_rows(info: list[str]) -> Iterator[ItemPocketName]:
        yield ItemPocketName(item_pocket_id=int(info[0]), language_id=int(info[1]), name=info[2])

    build_generic((ItemPocketName,), "item_pocket_names.csv", item_pocket_names_from_rows)

    def item_fling_effects_from_rows(info: list[str]) -> Iterator[ItemFlingEffect]:
        yield ItemFlingEffect(id=int(info[0]), name=info[1])

    build_generic((ItemFlingEffect,), "item_fling_effects.csv", item_fling_effects_from_rows)

    def item_fling_effect_effect_texts_from_rows(info: list[str]) -> Iterator[ItemFlingEffectEffectText]:
        yield ItemFlingEffectEffectText(
            item_fling_effect_id=int(info[0]),
            language_id=int(info[1]),
            effect=info[2],
        )

    build_generic(
        (ItemFlingEffectEffectText,),
        "item_fling_effect_prose.csv",
        item_fling_effect_effect_texts_from_rows,
    )

    def item_categories_from_rows(info: list[str]) -> Iterator[ItemCategory]:
        yield ItemCategory(id=int(info[0]), item_pocket_id=int(info[1]), name=info[2])

    build_generic((ItemCategory,), "item_categories.csv", item_categories_from_rows)

    def item_category_names_from_rows(info: list[str]) -> Iterator[ItemCategoryName]:
        yield ItemCategoryName(item_category_id=int(info[0]), language_id=int(info[1]), name=info[2])

    build_generic((ItemCategoryName,), "item_category_prose.csv", item_category_names_from_rows)

    def items_from_rows(info: list[str]) -> Iterator[Item]:
        yield Item(
            id=int(info[0]),
            name=info[1],
            item_category_id=int(info[2]),
            fling_power=int(info[4]) if info[4] != "" else None,
            item_fling_effect_id=int(info[5]) if info[5] != "" else None,
        )

    build_generic((Item,), "items.csv", items_from_rows)

    def item_sprites_from_rows(info: list[str]) -> Iterator[ItemSprites]:
        if re.search(r"^data-card", info[1]):
            file_name = "data-card.png"
        elif re.search(r"^tm[0-9]", info[1]):
            file_name = "tm-normal.png"
        elif re.search(r"^hm[0-9]", info[1]):
            file_name = "hm-normal.png"
        else:
            file_name = f"{info[1]}.png"

        item_sprites = "items/{0}"
        sprites = {"default": file_path_or_none(item_sprites.format(file_name))}
        yield ItemSprites(id=int(info[0]), item_id=int(info[0]), sprites=sprites)

    build_generic((ItemSprites,), "items.csv", item_sprites_from_rows)

    def item_names_from_rows(info: list[str]) -> Iterator[ItemName]:
        yield ItemName(item_id=int(info[0]), language_id=int(info[1]), name=info[2])

    build_generic((ItemName,), "item_names.csv", item_names_from_rows)

    def item_effect_texts_from_rows(info: list[str]) -> Iterator[ItemEffectText]:
        yield ItemEffectText(
            item_id=int(info[0]),
            language_id=int(info[1]),
            short_effect=info[2],
            effect=info[3],
        )

    build_generic((ItemEffectText,), "item_prose.csv", item_effect_texts_from_rows)

    def item_game_indexes_from_rows(info: list[str]) -> Iterator[ItemGameIndex]:
        yield ItemGameIndex(item_id=int(info[0]), generation_id=int(info[1]), game_index=int(info[2]))

    build_generic((ItemGameIndex,), "item_game_indices.csv", item_game_indexes_from_rows)

    def item_prices_from_rows(info: list[str]) -> Iterator[ItemPrice]:
        # Keep backward compatibility with 4-column files (no currency_id).
        has_currency_id = len(info) >= 5
        purchase_price_index = 3 if has_currency_id else 2
        sell_price_index = 4 if has_currency_id else 3

        yield ItemPrice(
            item_id=int(info[0]),
            version_group_id=int(info[1]),
            currency_id=int(info[2]) if has_currency_id and info[2] else 1,
            purchase_price=(int(info[purchase_price_index]) if info[purchase_price_index] else None),
            sell_price=int(info[sell_price_index]) if info[sell_price_index] else None,
        )

    build_generic((ItemPrice,), "item_prices.csv", item_prices_from_rows)

    def item_flavor_texts_from_rows(info: list[str]) -> Iterator[ItemFlavorText]:
        yield ItemFlavorText(
            item_id=int(info[0]),
            version_group_id=int(info[1]),
            language_id=int(info[2]),
            flavor_text=info[3],
        )

    build_generic((ItemFlavorText,), "item_flavor_text.csv", item_flavor_texts_from_rows)

    def item_attributes_from_rows(info: list[str]) -> Iterator[ItemAttribute]:
        yield ItemAttribute(id=int(info[0]), name=info[1])

    build_generic((ItemAttribute,), "item_flags.csv", item_attributes_from_rows)

    def item_flag_prose_from_rows(info: list[str]) -> Iterator[ItemAttributeName | ItemAttributeDescription]:
        yield ItemAttributeName(item_attribute_id=int(info[0]), language_id=int(info[1]), name=info[2])
        yield ItemAttributeDescription(
            item_attribute_id=int(info[0]),
            language_id=int(info[1]),
            description=info[3],
        )

    build_generic(
        (ItemAttributeName, ItemAttributeDescription),
        "item_flag_prose.csv",
        item_flag_prose_from_rows,
    )

    def item_attribute_maps_from_rows(info: list[str]) -> Iterator[ItemAttributeMap]:
        yield ItemAttributeMap(item_id=int(info[0]), item_attribute_id=int(info[1]))

    build_generic((ItemAttributeMap,), "item_flag_map.csv", item_attribute_maps_from_rows)


def _build_types() -> None:
    def types_from_rows(info: list[str]) -> Iterator[Type]:
        yield Type(
            id=int(info[0]),
            name=info[1],
            generation_id=int(info[2]),
            move_damage_class_id=int(info[3]) if info[3] != "" else None,
        )

    build_generic((Type,), "types.csv", types_from_rows)

    def type_names_from_rows(info: list[str]) -> Iterator[TypeName]:
        yield TypeName(type_id=int(info[0]), language_id=int(info[1]), name=info[2])

    build_generic((TypeName,), "type_names.csv", type_names_from_rows)

    def type_game_indexes_from_rows(info: list[str]) -> Iterator[TypeGameIndex]:
        yield TypeGameIndex(type_id=int(info[0]), generation_id=int(info[1]), game_index=int(info[2]))

    build_generic((TypeGameIndex,), "type_game_indices.csv", type_game_indexes_from_rows)

    def type_efficacies_from_rows(info: list[str]) -> Iterator[TypeEfficacy]:
        yield TypeEfficacy(
            damage_type_id=int(info[0]),
            target_type_id=int(info[1]),
            damage_factor=int(info[2]),
        )

    build_generic((TypeEfficacy,), "type_efficacy.csv", type_efficacies_from_rows)

    def type_efficacies_past_from_rows(info: list[str]) -> Iterator[TypeEfficacyPast]:
        yield TypeEfficacyPast(
            damage_type_id=int(info[0]),
            target_type_id=int(info[1]),
            damage_factor=int(info[2]),
            generation_id=int(info[3]),
        )

    build_generic((TypeEfficacyPast,), "type_efficacy_past.csv", type_efficacies_past_from_rows)

    def type_sprites_from_rows(info: list[str]) -> Iterator[TypeSprites]:
        sprites = {}
        for generation, games in TYPE_SPRITE_GAME_MAP.items():
            for game in games:
                if generation not in sprites:
                    sprites[generation] = {}
                sprites[generation][game] = {
                    "name_icon": file_path_or_none(f"types/{generation}/{game}/{info[0]}.png"),
                    "symbol_icon": file_path_or_none(f"types/{generation}/{game}/small/{info[0]}.png"),
                }

        yield TypeSprites(type_id=int(info[0]), sprites=sprites)

    build_generic((TypeSprites,), "types.csv", type_sprites_from_rows)


def _build_contests() -> None:
    def contest_types_from_rows(info: list[str]) -> Iterator[ContestType]:
        yield ContestType(id=int(info[0]), name=info[1])

    build_generic((ContestType,), "contest_types.csv", contest_types_from_rows)

    def contest_type_names_from_rows(info: list[str]) -> Iterator[ContestTypeName]:
        yield ContestTypeName(
            contest_type_id=int(info[0]),
            language_id=int(info[1]),
            name=info[2],
            flavor=info[3],
            color=info[4],
        )

    build_generic((ContestTypeName,), "contest_type_names.csv", contest_type_names_from_rows)

    def contest_effects_from_rows(info: list[str]) -> Iterator[ContestEffect]:
        yield ContestEffect(id=int(info[0]), appeal=int(info[1]), jam=int(info[2]))

    build_generic((ContestEffect,), "contest_effects.csv", contest_effects_from_rows)

    def contest_effect_prose_from_rows(info: list[str]) -> Iterator[ContestEffectEffectText | ContestEffectFlavorText]:
        yield ContestEffectEffectText(contest_effect_id=int(info[0]), language_id=int(info[1]), effect=info[3])
        yield ContestEffectFlavorText(
            contest_effect_id=int(info[0]),
            language_id=int(info[1]),
            flavor_text=info[2],
        )

    build_generic(
        (ContestEffectEffectText, ContestEffectFlavorText),
        "contest_effect_prose.csv",
        contest_effect_prose_from_rows,
    )

    def super_contest_effects_from_rows(info: list[str]) -> Iterator[SuperContestEffect]:
        yield SuperContestEffect(id=int(info[0]), appeal=int(info[1]))

    build_generic((SuperContestEffect,), "super_contest_effects.csv", super_contest_effects_from_rows)

    def super_contest_effect_flavor_texts_from_rows(info: list[str]) -> Iterator[SuperContestEffectFlavorText]:
        yield SuperContestEffectFlavorText(
            super_contest_effect_id=int(info[0]),
            language_id=int(info[1]),
            flavor_text=info[2],
        )

    build_generic(
        (SuperContestEffectFlavorText,),
        "super_contest_effect_prose.csv",
        super_contest_effect_flavor_texts_from_rows,
    )


def _build_moves() -> None:
    def move_effects_from_rows(info: list[str]) -> Iterator[MoveEffect]:
        yield MoveEffect(id=int(info[0]))

    build_generic((MoveEffect,), "move_effects.csv", move_effects_from_rows)

    def move_effect_effect_texts_from_rows(info: list[str]) -> Iterator[MoveEffectEffectText]:
        yield MoveEffectEffectText(
            move_effect_id=int(info[0]),
            language_id=int(info[1]),
            short_effect=info[2],
            effect=info[3],
        )

    build_generic((MoveEffectEffectText,), "move_effect_prose.csv", move_effect_effect_texts_from_rows)

    def move_effect_changes_from_rows(info: list[str]) -> Iterator[MoveEffectChange]:
        yield MoveEffectChange(id=int(info[0]), move_effect_id=int(info[1]), version_group_id=int(info[2]))

    build_generic((MoveEffectChange,), "move_effect_changelog.csv", move_effect_changes_from_rows)

    def move_effect_change_effect_texts_from_rows(info: list[str]) -> Iterator[MoveEffectChangeEffectText]:
        yield MoveEffectChangeEffectText(
            move_effect_change_id=int(info[0]),
            language_id=int(info[1]),
            effect=info[2],
        )

    build_generic(
        (MoveEffectChangeEffectText,),
        "move_effect_changelog_prose.csv",
        move_effect_change_effect_texts_from_rows,
    )

    def move_learn_methods_from_rows(info: list[str]) -> Iterator[MoveLearnMethod]:
        yield MoveLearnMethod(id=int(info[0]), name=info[1])

    build_generic((MoveLearnMethod,), "pokemon_move_methods.csv", move_learn_methods_from_rows)

    def version_group_move_learn_methods_from_rows(info: list[str]) -> Iterator[VersionGroupMoveLearnMethod]:
        yield VersionGroupMoveLearnMethod(version_group_id=int(info[0]), move_learn_method_id=int(info[1]))

    build_generic(
        (VersionGroupMoveLearnMethod,),
        "version_group_pokemon_move_methods.csv",
        version_group_move_learn_methods_from_rows,
    )

    def pokemon_move_method_prose_from_rows(
        info: list[str],
    ) -> Iterator[MoveLearnMethodName | MoveLearnMethodDescription]:
        yield MoveLearnMethodName(move_learn_method_id=int(info[0]), language_id=int(info[1]), name=info[2])
        yield MoveLearnMethodDescription(
            move_learn_method_id=int(info[0]),
            language_id=int(info[1]),
            description=info[3],
        )

    build_generic(
        (MoveLearnMethodName, MoveLearnMethodDescription),
        "pokemon_move_method_prose.csv",
        pokemon_move_method_prose_from_rows,
    )

    def move_targets_from_rows(info: list[str]) -> Iterator[MoveTarget]:
        yield MoveTarget(id=int(info[0]), name=info[1])

    build_generic((MoveTarget,), "move_targets.csv", move_targets_from_rows)

    def move_target_prose_from_rows(info: list[str]) -> Iterator[MoveTargetName | MoveTargetDescription]:
        yield MoveTargetName(move_target_id=int(info[0]), language_id=int(info[1]), name=info[2])
        yield MoveTargetDescription(move_target_id=int(info[0]), language_id=int(info[1]), description=info[3])

    build_generic(
        (MoveTargetName, MoveTargetDescription),
        "move_target_prose.csv",
        move_target_prose_from_rows,
    )

    def moves_from_rows(info: list[str]) -> Iterator[Move]:
        yield Move(
            id=int(info[0]),
            name=info[1],
            generation_id=int(info[2]),
            type_id=int(info[3]),
            power=int(info[4]) if info[4] != "" else None,
            pp=int(info[5]) if info[5] != "" else None,
            accuracy=int(info[6]) if info[6] != "" else None,
            priority=int(info[7]) if info[7] != "" else None,
            move_target_id=int(info[8]) if info[8] != "" else None,
            move_damage_class_id=int(info[9]) if info[9] != "" else None,
            move_effect_id=int(info[10]) if info[10] != "" else None,
            move_effect_chance=int(info[11]) if info[11] != "" else None,
            contest_type_id=int(info[12]) if info[12] != "" else None,
            contest_effect_id=int(info[13]) if info[13] != "" else None,
            super_contest_effect_id=int(info[14]) if info[14] != "" else None,
        )

    build_generic((Move,), "moves.csv", moves_from_rows)

    def move_names_from_rows(info: list[str]) -> Iterator[MoveName]:
        yield MoveName(move_id=int(info[0]), language_id=int(info[1]), name=info[2])

    build_generic((MoveName,), "move_names.csv", move_names_from_rows)

    def move_flavor_texts_from_rows(info: list[str]) -> Iterator[MoveFlavorText]:
        yield MoveFlavorText(
            move_id=int(info[0]),
            version_group_id=int(info[1]),
            language_id=int(info[2]),
            flavor_text=info[3],
        )

    build_generic((MoveFlavorText,), "move_flavor_text.csv", move_flavor_texts_from_rows)

    existing_effect_ids = set(MoveEffect.objects.values_list("pk", flat=True))

    def move_changes_from_rows(info: list[str]) -> Iterator[MoveChange]:
        effect_id = int(info[8]) if info[8] != "" else None
        if effect_id not in existing_effect_ids:
            effect_id = None

        yield MoveChange(
            move_id=int(info[0]),
            version_group_id=int(info[1]),
            type_id=int(info[2]) if info[2] != "" else None,
            power=int(info[3]) if info[3] != "" else None,
            pp=int(info[4]) if info[4] != "" else None,
            accuracy=int(info[5]) if info[5] != "" else None,
            move_effect_id=effect_id,
            move_effect_chance=int(info[9]) if info[9] != "" else None,
        )

    build_generic((MoveChange,), "move_changelog.csv", move_changes_from_rows)

    def move_battle_styles_from_rows(info: list[str]) -> Iterator[MoveBattleStyle]:
        yield MoveBattleStyle(id=int(info[0]), name=info[1])

    build_generic((MoveBattleStyle,), "move_battle_styles.csv", move_battle_styles_from_rows)

    def move_battle_style_names_from_rows(info: list[str]) -> Iterator[MoveBattleStyleName]:
        yield MoveBattleStyleName(move_battle_style_id=int(info[0]), language_id=int(info[1]), name=info[2])

    build_generic((MoveBattleStyleName,), "move_battle_style_prose.csv", move_battle_style_names_from_rows)

    def move_attributes_from_rows(info: list[str]) -> Iterator[MoveAttribute]:
        yield MoveAttribute(id=int(info[0]), name=info[1])

    build_generic((MoveAttribute,), "move_flags.csv", move_attributes_from_rows)

    def move_attribute_maps_from_rows(info: list[str]) -> Iterator[MoveAttributeMap]:
        yield MoveAttributeMap(move_id=int(info[0]), move_attribute_id=int(info[1]))

    build_generic((MoveAttributeMap,), "move_flag_map.csv", move_attribute_maps_from_rows)

    def move_flag_prose_from_rows(info: list[str]) -> Iterator[MoveAttributeName | MoveAttributeDescription]:
        yield MoveAttributeName(move_attribute_id=int(info[0]), language_id=int(info[1]), name=info[2])
        yield MoveAttributeDescription(
            move_attribute_id=int(info[0]),
            language_id=int(info[1]),
            description=info[3],
        )

    build_generic(
        (MoveAttributeName, MoveAttributeDescription),
        "move_flag_prose.csv",
        move_flag_prose_from_rows,
    )

    def move_meta_ailments_from_rows(info: list[str]) -> Iterator[MoveMetaAilment]:
        yield MoveMetaAilment(id=int(info[0]), name=info[1])

    build_generic((MoveMetaAilment,), "move_meta_ailments.csv", move_meta_ailments_from_rows)

    def move_meta_ailment_names_from_rows(info: list[str]) -> Iterator[MoveMetaAilmentName]:
        yield MoveMetaAilmentName(move_meta_ailment_id=int(info[0]), language_id=int(info[1]), name=info[2])

    build_generic((MoveMetaAilmentName,), "move_meta_ailment_names.csv", move_meta_ailment_names_from_rows)

    def move_meta_categories_from_rows(info: list[str]) -> Iterator[MoveMetaCategory]:
        yield MoveMetaCategory(id=int(info[0]), name=info[1])

    build_generic((MoveMetaCategory,), "move_meta_categories.csv", move_meta_categories_from_rows)

    def move_meta_category_descriptions_from_rows(info: list[str]) -> Iterator[MoveMetaCategoryDescription]:
        yield MoveMetaCategoryDescription(
            move_meta_category_id=int(info[0]),
            language_id=int(info[1]),
            description=info[2],
        )

    build_generic(
        (MoveMetaCategoryDescription,),
        "move_meta_category_prose.csv",
        move_meta_category_descriptions_from_rows,
    )

    def move_metadata_from_rows(info: list[str]) -> Iterator[MoveMeta]:
        yield MoveMeta(
            move_id=int(info[0]),
            move_meta_category_id=int(info[1]),
            move_meta_ailment_id=int(info[2]),
            min_hits=int(info[3]) if info[3] != "" else None,
            max_hits=int(info[4]) if info[4] != "" else None,
            min_turns=int(info[5]) if info[5] != "" else None,
            max_turns=int(info[6]) if info[6] != "" else None,
            drain=int(info[7]) if info[7] != "" else None,
            healing=int(info[8]) if info[8] != "" else None,
            crit_rate=int(info[9]) if info[9] != "" else None,
            ailment_chance=int(info[10]) if info[10] != "" else None,
            flinch_chance=int(info[11]) if info[11] != "" else None,
            stat_chance=int(info[12]) if info[12] != "" else None,
        )

    build_generic((MoveMeta,), "move_meta.csv", move_metadata_from_rows)

    def move_meta_stat_changes_from_rows(info: list[str]) -> Iterator[MoveMetaStatChange]:
        yield MoveMetaStatChange(move_id=int(info[0]), stat_id=int(info[1]), change=int(info[2]))

    build_generic((MoveMetaStatChange,), "move_meta_stat_changes.csv", move_meta_stat_changes_from_rows)

    def contest_combos_from_rows(info: list[str]) -> Iterator[ContestCombo]:
        yield ContestCombo(first_move_id=int(info[0]), second_move_id=int(info[1]))

    build_generic((ContestCombo,), "contest_combos.csv", contest_combos_from_rows)

    def super_contest_combos_from_rows(info: list[str]) -> Iterator[SuperContestCombo]:
        yield SuperContestCombo(first_move_id=int(info[0]), second_move_id=int(info[1]))

    build_generic((SuperContestCombo,), "super_contest_combos.csv", super_contest_combos_from_rows)


def _build_berries() -> None:
    def berry_firmnesses_from_rows(info: list[str]) -> Iterator[BerryFirmness]:
        yield BerryFirmness(id=int(info[0]), name=info[1])

    build_generic((BerryFirmness,), "berry_firmness.csv", berry_firmnesses_from_rows)

    def berry_firmness_names_from_rows(info: list[str]) -> Iterator[BerryFirmnessName]:
        yield BerryFirmnessName(berry_firmness_id=int(info[0]), language_id=int(info[1]), name=info[2])

    build_generic((BerryFirmnessName,), "berry_firmness_names.csv", berry_firmness_names_from_rows)

    item_names = dict(Item.objects.values_list("pk", "name"))

    def berries_from_rows(info: list[str]) -> Iterator[Berry]:
        item_id = int(info[1])
        item_name = item_names[item_id] if item_id in item_names else Item.objects.get(pk=item_id).name
        yield Berry(
            id=int(info[0]),
            item_id=item_id,
            name=item_name.split("-berry")[0],
            berry_firmness_id=int(info[2]) if info[2] else None,
            natural_gift_power=int(info[3]) if info[3] else None,
            natural_gift_type_id=int(info[4]) if info[4] else None,
            size=int(info[5]) if info[5] else None,
            max_harvest=int(info[6]) if info[6] else None,
            growth_time=int(info[7]) if info[7] else None,
            soil_dryness=int(info[8]) if info[8] else None,
            smoothness=int(info[9]) if info[9] else None,
        )

    build_generic((Berry,), "berries.csv", berries_from_rows)

    contest_type_ids = set(ContestType.objects.values_list("pk", flat=True))
    contest_flavors: dict[int, list[str]] = {}
    english_flavors = ContestTypeName.objects.filter(language_id=9).values_list("contest_type_id", "flavor")
    for contest_type_id, flavor in english_flavors:
        contest_flavors.setdefault(contest_type_id, []).append(flavor)

    def berry_flavors_from_rows(info: list[str]) -> Iterator[BerryFlavor]:
        contest_type_id = int(info[0])
        flavors = contest_flavors.get(contest_type_id, [])
        if len(flavors) == 1:
            flavor = flavors[0]
        else:
            # Preserve Django's missing and duplicate reference errors.
            flavor = ContestTypeName.objects.get(contest_type_id=contest_type_id, language_id=9).flavor
        if contest_type_id not in contest_type_ids:
            ContestType.objects.get(pk=contest_type_id)
        yield BerryFlavor(
            id=contest_type_id,
            name=flavor.lower(),
            contest_type_id=contest_type_id,
        )

    build_generic((BerryFlavor,), "contest_types.csv", berry_flavors_from_rows)

    def berry_flavor_names_from_rows(info: list[str]) -> Iterator[BerryFlavorName]:
        yield BerryFlavorName(berry_flavor_id=int(info[0]), language_id=int(info[1]), name=info[3])

    build_generic((BerryFlavorName,), "contest_type_names.csv", berry_flavor_names_from_rows)

    def berry_flavor_maps_from_rows(info: list[str]) -> Iterator[BerryFlavorMap]:
        yield BerryFlavorMap(berry_id=int(info[0]), berry_flavor_id=int(info[1]), potency=int(info[2]))

    build_generic((BerryFlavorMap,), "berry_flavors.csv", berry_flavor_maps_from_rows)


def _build_natures() -> None:
    stat_ids = set(Stat.objects.values_list("pk", flat=True))
    flavor_ids = set(BerryFlavor.objects.values_list("pk", flat=True))

    def natures_from_rows(info: list[str]) -> Iterator[Nature]:
        decreased_stat_id = None
        increased_stat_id = None
        hates_flavor_id = None
        likes_flavor_id = None

        if info[2] != info[3]:
            decreased_stat_id = int(info[2])
            if decreased_stat_id not in stat_ids:
                Stat.objects.get(pk=decreased_stat_id)
            increased_stat_id = int(info[3])
            if increased_stat_id not in stat_ids:
                Stat.objects.get(pk=increased_stat_id)

        if info[4] != info[5]:
            hates_flavor_id = int(info[4])
            if hates_flavor_id not in flavor_ids:
                BerryFlavor.objects.get(pk=hates_flavor_id)
            likes_flavor_id = int(info[5])
            if likes_flavor_id not in flavor_ids:
                BerryFlavor.objects.get(pk=likes_flavor_id)

        yield Nature(
            id=int(info[0]),
            name=info[1],
            decreased_stat_id=decreased_stat_id,
            increased_stat_id=increased_stat_id,
            hates_flavor_id=hates_flavor_id,
            likes_flavor_id=likes_flavor_id,
            game_index=info[6],
        )

    build_generic((Nature,), "natures.csv", natures_from_rows)

    def nature_names_from_rows(info: list[str]) -> Iterator[NatureName]:
        yield NatureName(nature_id=int(info[0]), language_id=int(info[1]), name=info[2])

    build_generic((NatureName,), "nature_names.csv", nature_names_from_rows)

    def nature_pokeathlon_stats_from_rows(info: list[str]) -> Iterator[NaturePokeathlonStat]:
        yield NaturePokeathlonStat(nature_id=(info[0]), pokeathlon_stat_id=(info[1]), max_change=info[2])

    build_generic((NaturePokeathlonStat,), "nature_pokeathlon_stats.csv", nature_pokeathlon_stats_from_rows)

    def nature_battle_style_preferences_from_rows(info: list[str]) -> Iterator[NatureBattleStylePreference]:
        yield NatureBattleStylePreference(
            nature_id=int(info[0]),
            move_battle_style_id=int(info[1]),
            low_hp_preference=info[2],
            high_hp_preference=info[3],
        )

    build_generic(
        (NatureBattleStylePreference,),
        "nature_battle_style_preferences.csv",
        nature_battle_style_preferences_from_rows,
    )


def _build_genders() -> None:
    def genders_from_rows(info: list[str]) -> Iterator[Gender]:
        yield Gender(id=int(info[0]), name=info[1])

    build_generic((Gender,), "genders.csv", genders_from_rows)


def _build_experiences() -> None:
    def experiences_from_rows(info: list[str]) -> Iterator[Experience]:
        yield Experience(growth_rate_id=int(info[0]), level=int(info[1]), experience=int(info[2]))

    build_generic((Experience,), "experience.csv", experiences_from_rows)


def _build_machines() -> None:
    def machines_from_rows(info: list[str]) -> Iterator[Machine]:
        yield Machine(
            machine_number=int(info[0]),
            version_group_id=int(info[1]),
            item_id=int(info[2]),
            move_id=int(info[3]),
        )

    build_generic((Machine,), "machines.csv", machines_from_rows)


def _build_evolutions() -> None:
    def evolution_chains_from_rows(info: list[str]) -> Iterator[EvolutionChain]:
        yield EvolutionChain(
            id=int(info[0]),
            baby_trigger_item_id=int(info[1]) if info[1] != "" else None,
        )

    build_generic((EvolutionChain,), "evolution_chains.csv", evolution_chains_from_rows)

    def evolution_triggers_from_rows(info: list[str]) -> Iterator[EvolutionTrigger]:
        yield EvolutionTrigger(id=int(info[0]), name=info[1])

    build_generic((EvolutionTrigger,), "evolution_triggers.csv", evolution_triggers_from_rows)

    def evolution_trigger_names_from_rows(info: list[str]) -> Iterator[EvolutionTriggerName]:
        yield EvolutionTriggerName(evolution_trigger_id=int(info[0]), language_id=int(info[1]), name=info[2])

    build_generic((EvolutionTriggerName,), "evolution_trigger_prose.csv", evolution_trigger_names_from_rows)

    def evolution_variables_from_rows(info: list[str]) -> Iterator[EvolutionVariable]:
        yield EvolutionVariable(
            id=int(info[0]),
            name=info[1],
            symbol=info[2],
            data_type=info[3],
            version_group_id=int(info[4]),
            source=info[5],
        )

    build_generic((EvolutionVariable,), "evolution_variables.csv", evolution_variables_from_rows)

    def evolution_variable_prose_from_rows(
        info: list[str],
    ) -> Iterator[EvolutionVariableName | EvolutionVariableDescription]:
        yield EvolutionVariableName(
            evolution_variable_id=int(info[0]),
            language_id=int(info[1]),
            name=info[2],
        )
        yield EvolutionVariableDescription(
            evolution_variable_id=int(info[0]),
            language_id=int(info[1]),
            description=info[3],
        )

    build_generic(
        (EvolutionVariableName, EvolutionVariableDescription),
        "evolution_variable_prose.csv",
        evolution_variable_prose_from_rows,
    )


def _build_pokedexes() -> None:
    def pokedexes_from_rows(info: list[str]) -> Iterator[Pokedex]:
        yield Pokedex(
            id=int(info[0]),
            region_id=int(info[1]) if info[1] != "" else None,
            name=info[2],
            is_main_series=bool(int(info[3])),
        )

    build_generic((Pokedex,), "pokedexes.csv", pokedexes_from_rows)

    def pokedex_prose_from_rows(info: list[str]) -> Iterator[PokedexName | PokedexDescription]:
        yield PokedexName(pokedex_id=int(info[0]), language_id=int(info[1]), name=info[2])
        yield PokedexDescription(pokedex_id=int(info[0]), language_id=int(info[1]), description=info[3])

    build_generic((PokedexName, PokedexDescription), "pokedex_prose.csv", pokedex_prose_from_rows)

    def pokedex_version_groups_from_rows(info: list[str]) -> Iterator[PokedexVersionGroup]:
        yield PokedexVersionGroup(pokedex_id=int(info[0]), version_group_id=int(info[1]))

    build_generic((PokedexVersionGroup,), "pokedex_version_groups.csv", pokedex_version_groups_from_rows)


def _build_locations() -> None:
    def locations_from_rows(info: list[str]) -> Iterator[Location]:
        yield Location(
            id=int(info[0]),
            region_id=int(info[1]) if info[1] != "" else None,
            name=info[2],
        )

    build_generic((Location,), "locations.csv", locations_from_rows)

    def location_names_from_rows(info: list[str]) -> Iterator[LocationName]:
        yield LocationName(location_id=int(info[0]), language_id=int(info[1]), name=info[2])

    build_generic((LocationName,), "location_names.csv", location_names_from_rows)

    def location_game_indexes_from_rows(info: list[str]) -> Iterator[LocationGameIndex]:
        yield LocationGameIndex(
            location_id=int(info[0]),
            generation_id=int(info[1]),
            game_index=int(info[2]),
        )

    build_generic((LocationGameIndex,), "location_game_indices.csv", location_game_indexes_from_rows)

    location_names = dict(Location.objects.values_list("pk", "name"))

    def location_areas_from_rows(info: list[str]) -> Iterator[LocationArea]:
        location_id = int(info[1])
        location_name = (
            location_names[location_id] if location_id in location_names else Location.objects.get(pk=location_id).name
        )
        yield LocationArea(
            id=int(info[0]),
            location_id=location_id,
            game_index=int(info[2]),
            name=(f"{location_name}-{info[3]}" if info[3] else "{}-{}".format(location_name, "area")),
        )

    build_generic((LocationArea,), "location_areas.csv", location_areas_from_rows)

    def location_area_names_from_rows(info: list[str]) -> Iterator[LocationAreaName]:
        yield LocationAreaName(location_area_id=int(info[0]), language_id=int(info[1]), name=info[2])

    build_generic((LocationAreaName,), "location_area_prose.csv", location_area_names_from_rows)


def _build_pokemons() -> None:
    def pokemon_colors_from_rows(info: list[str]) -> Iterator[PokemonColor]:
        yield PokemonColor(id=int(info[0]), name=info[1])

    build_generic((PokemonColor,), "pokemon_colors.csv", pokemon_colors_from_rows)

    def pokemon_color_names_from_rows(info: list[str]) -> Iterator[PokemonColorName]:
        yield PokemonColorName(pokemon_color_id=int(info[0]), language_id=int(info[1]), name=info[2])

    build_generic((PokemonColorName,), "pokemon_color_names.csv", pokemon_color_names_from_rows)

    def pokemon_shapes_from_rows(info: list[str]) -> Iterator[PokemonShape]:
        yield PokemonShape(id=int(info[0]), name=info[1])

    build_generic((PokemonShape,), "pokemon_shapes.csv", pokemon_shapes_from_rows)

    def pokemon_shape_names_from_rows(info: list[str]) -> Iterator[PokemonShapeName]:
        yield PokemonShapeName(
            pokemon_shape_id=int(info[0]),
            language_id=int(info[1]),
            name=info[2],
            awesome_name=info[3],
        )

    build_generic((PokemonShapeName,), "pokemon_shape_prose.csv", pokemon_shape_names_from_rows)

    def pokemon_habitats_from_rows(info: list[str]) -> Iterator[PokemonHabitat]:
        yield PokemonHabitat(id=int(info[0]), name=info[1])

    build_generic((PokemonHabitat,), "pokemon_habitats.csv", pokemon_habitats_from_rows)

    def pokemon_species_from_rows(info: list[str]) -> Iterator[PokemonSpecies]:
        yield PokemonSpecies(
            id=int(info[0]),
            name=info[1],
            generation_id=int(info[2]) if info[2] != "" else None,
            evolves_from_species=None,
            evolution_chain_id=int(info[4]) if info[4] != "" else None,
            pokemon_color_id=int(info[5]) if info[5] != "" else None,
            pokemon_shape_id=int(info[6]) if info[6] != "" else None,
            pokemon_habitat_id=int(info[7]) if info[7] != "" else None,
            gender_rate=int(info[8]) if info[8] != "" else None,
            capture_rate=int(info[9]) if info[9] != "" else None,
            base_happiness=int(info[10]) if info[10] != "" else None,
            is_baby=bool(int(info[11])) if info[11] != "" else None,
            hatch_counter=int(info[12]) if info[12] != "" else None,
            has_gender_differences=bool(int(info[13])) if info[13] != "" else False,
            growth_rate_id=int(info[14]) if info[14] != "" else None,
            forms_switchable=bool(int(info[15])) if info[15] != "" else None,
            is_legendary=bool(int(info[16])) if info[16] != "" else None,
            is_mythical=bool(int(info[17])) if info[17] != "" else None,
            order=int(info[18]) if info[18] != "" else None,
        )

    build_generic((PokemonSpecies,), "pokemon_species.csv", pokemon_species_from_rows)

    # PokemonSpecies.evolves_from_species can't be set until all the species are created
    data = load_data("pokemon_species.csv")
    for index, info in enumerate(data):
        if index > 0:
            evolves = PokemonSpecies.objects.get(pk=int(info[3])) if info[3] != "" else None
            if evolves:
                species = PokemonSpecies.objects.get(pk=int(info[0]))
                species.evolves_from_species = evolves
                species.save()

    def pokemon_species_names_from_rows(info: list[str]) -> Iterator[PokemonSpeciesName]:
        yield PokemonSpeciesName(
            pokemon_species_id=int(info[0]),
            language_id=int(info[1]),
            name=info[2],
            genus=info[3],
        )

    build_generic((PokemonSpeciesName,), "pokemon_species_names.csv", pokemon_species_names_from_rows)

    def pokemon_species_descriptions_from_rows(info: list[str]) -> Iterator[PokemonSpeciesDescription]:
        yield PokemonSpeciesDescription(
            pokemon_species_id=int(info[0]),
            language_id=int(info[1]),
            description=info[2],
        )

    build_generic((PokemonSpeciesDescription,), "pokemon_species_prose.csv", pokemon_species_descriptions_from_rows)

    def pokemon_species_flavor_texts_from_rows(info: list[str]) -> Iterator[PokemonSpeciesFlavorText]:
        yield PokemonSpeciesFlavorText(
            pokemon_species_id=int(info[0]),
            version_id=int(info[1]),
            language_id=int(info[2]),
            flavor_text=info[3],
        )

    build_generic(
        (PokemonSpeciesFlavorText,),
        "pokemon_species_flavor_text.csv",
        pokemon_species_flavor_texts_from_rows,
    )

    def pokemon_from_rows(info: list[str]) -> Iterator[Pokemon]:
        yield Pokemon(
            id=int(info[0]),
            name=info[1],
            pokemon_species_id=int(info[2]) if info[2] != "" else None,
            height=int(info[3]) if info[3] != "" else None,
            weight=int(info[4]) if info[4] != "" else None,
            base_experience=int(info[5]) if info[5] != "" else None,
            order=int(info[6]) if info[6] != "" else -1,
            is_default=bool(int(info[7])) if info[7] != "" else None,
        )

    build_generic((Pokemon,), "pokemon.csv", pokemon_from_rows)

    def pokemon_sprites_from_rows(info: list[str]) -> Iterator[PokemonSprites]:
        sprites = resolve_sprite_config(POKEMON_SPRITE_CONFIG, pokemon_sprite_lookup(info))
        yield PokemonSprites(
            id=int(info[0]),
            pokemon=Pokemon.objects.get(pk=int(info[0])),
            sprites=sprites,
        )

    build_generic((PokemonSprites,), "pokemon.csv", pokemon_sprites_from_rows)

    def try_cry_names(path: str, info: list[str], extension: str) -> str | None:
        file_name = f"{info[0]}.{extension}"
        return file_path_or_none(path + file_name, image_file=False)

    def pokemon_cries_from_rows(info: list[str]) -> Iterator[PokemonCries]:
        poke_cries = "pokemon"
        latest = f"{poke_cries}/latest/"
        legacy = f"{poke_cries}/legacy/"
        cries = {
            "latest": try_cry_names(latest, info, "ogg"),
            "legacy": try_cry_names(legacy, info, "ogg"),
        }
        yield PokemonCries(
            id=int(info[0]),
            pokemon=Pokemon.objects.get(pk=int(info[0])),
            cries=cries,
        )

    build_generic((PokemonCries,), "pokemon.csv", pokemon_cries_from_rows)

    def pokemon_abilities_from_rows(info: list[str]) -> Iterator[PokemonAbility]:
        yield PokemonAbility(
            pokemon_id=int(info[0]),
            ability_id=int(info[1]),
            is_hidden=bool(int(info[2])),
            slot=int(info[3]),
        )

    build_generic((PokemonAbility,), "pokemon_abilities.csv", pokemon_abilities_from_rows)

    def pokemon_abilities_past_from_rows(info: list[str]) -> Iterator[PokemonAbilityPast]:
        yield PokemonAbilityPast(
            pokemon_id=int(info[0]),
            generation_id=int(info[1]),
            ability_id=int(info[2]) if info[2] != "" else None,
            is_hidden=bool(int(info[3])),
            slot=int(info[4]),
        )

    build_generic((PokemonAbilityPast,), "pokemon_abilities_past.csv", pokemon_abilities_past_from_rows)

    def pokemon_dex_numbers_from_rows(info: list[str]) -> Iterator[PokemonDexNumber]:
        yield PokemonDexNumber(
            pokemon_species_id=int(info[0]),
            pokedex_id=int(info[1]),
            pokedex_number=int(info[2]),
        )

    build_generic((PokemonDexNumber,), "pokemon_dex_numbers.csv", pokemon_dex_numbers_from_rows)

    def pokemon_egg_groups_from_rows(info: list[str]) -> Iterator[PokemonEggGroup]:
        yield PokemonEggGroup(pokemon_species_id=int(info[0]), egg_group_id=int(info[1]))

    build_generic((PokemonEggGroup,), "pokemon_egg_groups.csv", pokemon_egg_groups_from_rows)

    def pokemon_forms_from_rows(info: list[str]) -> Iterator[PokemonForm]:
        yield PokemonForm(
            id=int(info[0]),
            name=info[1],
            form_name=info[2],
            pokemon_id=int(info[3]),
            version_group_id=int(info[4]),
            is_default=bool(int(info[5])),
            is_battle_only=bool(int(info[6])),
            is_mega=bool(int(info[7])),
            form_order=int(info[8]),
            order=int(info[9]),
        )

    build_generic((PokemonForm,), "pokemon_forms.csv", pokemon_forms_from_rows)

    def pokemon_evolutions_from_rows(info: list[str]) -> Iterator[PokemonEvolution]:
        yield PokemonEvolution(
            id=int(info[0]),
            evolved_species_id=int(info[1]),
            evolution_trigger_id=int(info[2]),
            version_group_id=int(info[3]),
            is_default=bool(int(info[4])),
            evolution_item_id=int(info[5]) if info[5] != "" else None,
            min_level=int(info[6]) if info[6] != "" else None,
            gender_id=int(info[7]) if info[7] != "" else None,
            location_id=int(info[8]) if info[8] != "" else None,
            held_item_id=int(info[9]) if info[9] != "" else None,
            time_of_day=info[10],
            known_move_id=int(info[11]) if info[11] != "" else None,
            known_move_type_id=int(info[12]) if info[12] != "" else None,
            min_happiness=int(info[13]) if info[13] != "" else None,
            min_beauty=int(info[14]) if info[14] != "" else None,
            min_affection=int(info[15]) if info[15] != "" else None,
            relative_physical_stats=int(info[16]) if info[16] != "" else None,
            party_species_id=int(info[17]) if info[17] != "" else None,
            party_type_id=int(info[18]) if info[18] != "" else None,
            trade_species_id=int(info[19]) if info[19] != "" else None,
            needs_overworld_rain=bool(int(info[20])),
            turn_upside_down=bool(int(info[21])),
            needs_multiplayer=bool(int(info[22])),
            near_special_rock=bool(int(info[23])),
            region_id=int(info[24]) if info[24] != "" else None,
            required_pokemon_form_id=int(info[25]) if info[25] != "" else None,
            evolved_pokemon_form_id=int(info[26]) if info[26] != "" else None,
            used_move_id=int(info[27]) if info[27] != "" else None,
            min_move_count=int(info[28]) if info[28] != "" else None,
            min_steps=int(info[29]) if info[29] != "" else None,
            min_damage_taken=int(info[30]) if info[30] != "" else None,
            nature_bitmask=int(info[31]) if info[31] != "" else None,
            condition_expression=info[32],
            percentage_chance=(float(info[33]) if len(info) > 33 and info[33] != "" else None),
        )

    build_generic((PokemonEvolution,), "pokemon_evolution.csv", pokemon_evolutions_from_rows)

    pokemon_sprites_by_id = dict(PokemonSprites.objects.values_list("pokemon_id", "sprites"))

    def pokemon_form_sprites_from_rows(info: list[str]) -> Iterator[PokemonFormSprites]:
        if info[2]:
            lookup = pokemon_form_sprite_lookup(info)
            sprites = resolve_sprite_config(POKEMON_SPRITE_CONFIG, lookup)
        else:
            sprites = deepcopy(pokemon_sprites_by_id.get(int(info[3]), {}))
        yield PokemonFormSprites(id=int(info[0]), pokemon_form_id=int(info[0]), sprites=sprites)

    build_generic((PokemonFormSprites,), "pokemon_forms.csv", pokemon_form_sprites_from_rows)

    def pokemon_form_names_from_rows(info: list[str]) -> Iterator[PokemonFormName]:
        yield PokemonFormName(
            pokemon_form=PokemonForm.objects.get(pk=int(info[0])),
            language=Language.objects.get(pk=int(info[1])),
            name=info[2],
            pokemon_name=info[3],
        )

    build_generic((PokemonFormName,), "pokemon_form_names.csv", pokemon_form_names_from_rows)

    def pokemon_form_generations_from_rows(info: list[str]) -> Iterator[PokemonFormGeneration]:
        yield PokemonFormGeneration(
            pokemon_form_id=int(info[0]),
            generation_id=int(info[1]),
            game_index=int(info[2]),
        )

    build_generic((PokemonFormGeneration,), "pokemon_form_generations.csv", pokemon_form_generations_from_rows)

    def pokemon_form_types_from_rows(info: list[str]) -> Iterator[PokemonFormType]:
        yield PokemonFormType(pokemon_form_id=int(info[0]), type_id=int(info[1]), slot=int(info[2]))

    build_generic((PokemonFormType,), "pokemon_form_types.csv", pokemon_form_types_from_rows)

    def pokemon_form_triggers_from_rows(info: list[str]) -> Iterator[PokemonFormTrigger]:
        yield PokemonFormTrigger(id=int(info[0]), name=info[1])

    build_generic((PokemonFormTrigger,), "pokemon_form_triggers.csv", pokemon_form_triggers_from_rows)

    def pokemon_form_conditions_from_rows(info: list[str]) -> Iterator[PokemonFormCondition]:
        yield PokemonFormCondition(
            pokemon_form_id=int(info[0]),
            form_trigger_id=int(info[1]),
            item_id=int(info[2]) if info[2] != "" else None,
            ability_id=int(info[3]) if info[3] != "" else None,
            move_id=int(info[4]) if info[4] != "" else None,
            base_form_id=int(info[5]) if info[5] != "" else None,
        )

    build_generic((PokemonFormCondition,), "pokemon_form_conditions.csv", pokemon_form_conditions_from_rows)

    def pokemon_form_flavor_texts_from_rows(info: list[str]) -> Iterator[PokemonFormFlavorText]:
        yield PokemonFormFlavorText(
            pokemon_form_id=int(info[0]),
            version_id=int(info[1]),
            language_id=int(info[2]),
            flavor_text=info[3],
        )

    build_generic(
        (PokemonFormFlavorText,),
        "pokemon_form_flavor_text.csv",
        pokemon_form_flavor_texts_from_rows,
    )

    def pokemon_game_indexes_from_rows(info: list[str]) -> Iterator[PokemonGameIndex]:
        yield PokemonGameIndex(pokemon_id=int(info[0]), version_id=int(info[1]), game_index=int(info[2]))

    build_generic((PokemonGameIndex,), "pokemon_game_indices.csv", pokemon_game_indexes_from_rows)

    def pokemon_habitat_names_from_rows(info: list[str]) -> Iterator[PokemonHabitatName]:
        yield PokemonHabitatName(pokemon_habitat_id=int(info[0]), language_id=int(info[1]), name=info[2])

    build_generic((PokemonHabitatName,), "pokemon_habitat_names.csv", pokemon_habitat_names_from_rows)

    def pokemon_items_from_rows(info: list[str]) -> Iterator[PokemonItem]:
        yield PokemonItem(
            pokemon_id=int(info[0]),
            version_id=int(info[1]),
            item_id=int(info[2]),
            rarity=int(info[3]),
        )

    build_generic((PokemonItem,), "pokemon_items.csv", pokemon_items_from_rows)

    def pokemon_moves_from_rows(info: list[str]) -> Iterator[PokemonMove]:
        yield PokemonMove(
            pokemon_id=int(info[0]),
            version_group_id=int(info[1]),
            move_id=int(info[2]),
            move_learn_method_id=int(info[3]),
            level=int(info[4]),
            order=int(info[5]) if info[5] != "" else None,
        )

    build_generic((PokemonMove,), "pokemon_moves.csv", pokemon_moves_from_rows)

    def pokemon_stats_from_rows(info: list[str]) -> Iterator[PokemonStat]:
        yield PokemonStat(
            pokemon_id=int(info[0]),
            stat_id=int(info[1]),
            base_stat=int(info[2]),
            effort=int(info[3]),
        )

    build_generic((PokemonStat,), "pokemon_stats.csv", pokemon_stats_from_rows)

    def pokemon_stats_past_from_rows(info: list[str]) -> Iterator[PokemonStatPast]:
        yield PokemonStatPast(
            pokemon_id=int(info[0]),
            generation_id=int(info[1]),
            stat_id=int(info[2]),
            base_stat=int(info[3]),
            effort=int(info[4]),
        )

    build_generic((PokemonStatPast,), "pokemon_stats_past.csv", pokemon_stats_past_from_rows)

    def pokemon_types_from_rows(info: list[str]) -> Iterator[PokemonType]:
        yield PokemonType(pokemon_id=int(info[0]), type_id=int(info[1]), slot=int(info[2]))

    build_generic((PokemonType,), "pokemon_types.csv", pokemon_types_from_rows)

    def pokemon_types_past_from_rows(info: list[str]) -> Iterator[PokemonTypePast]:
        yield PokemonTypePast(
            pokemon_id=int(info[0]),
            generation_id=int(info[1]),
            type_id=int(info[2]),
            slot=int(info[3]),
        )

    build_generic((PokemonTypePast,), "pokemon_types_past.csv", pokemon_types_past_from_rows)


def _build_encounters() -> None:
    def encounter_methods_from_rows(info: list[str]) -> Iterator[EncounterMethod]:
        yield EncounterMethod(id=int(info[0]), name=info[1], order=int(info[2]))

    build_generic((EncounterMethod,), "encounter_methods.csv", encounter_methods_from_rows)

    def location_area_encounter_rates_from_rows(info: list[str]) -> Iterator[LocationAreaEncounterRate]:
        yield LocationAreaEncounterRate(
            location_area_id=int(info[0]),
            encounter_method_id=int(info[1]),
            version_id=int(info[2]),
            rate=int(info[3]),
        )

    build_generic(
        (LocationAreaEncounterRate,),
        "location_area_encounter_rates.csv",
        location_area_encounter_rates_from_rows,
    )

    def encounter_method_names_from_rows(info: list[str]) -> Iterator[EncounterMethodName]:
        yield EncounterMethodName(encounter_method_id=int(info[0]), language_id=int(info[1]), name=info[2])

    build_generic((EncounterMethodName,), "encounter_method_prose.csv", encounter_method_names_from_rows)

    def encounter_conditions_from_rows(info: list[str]) -> Iterator[EncounterCondition]:
        yield EncounterCondition(id=int(info[0]), name=info[1])

    build_generic((EncounterCondition,), "encounter_conditions.csv", encounter_conditions_from_rows)

    def encounter_condition_names_from_rows(info: list[str]) -> Iterator[EncounterConditionName]:
        yield EncounterConditionName(encounter_condition_id=int(info[0]), language_id=int(info[1]), name=info[2])

    build_generic(
        (EncounterConditionName,),
        "encounter_condition_prose.csv",
        encounter_condition_names_from_rows,
    )

    def encounter_slots_from_rows(info: list[str]) -> Iterator[EncounterSlot]:
        yield EncounterSlot(
            id=int(info[0]),
            version_group_id=int(info[1]),
            encounter_method_id=int(info[2]),
            slot=int(info[3]) if info[3] != "" else None,
            rarity=int(info[4]),
        )

    build_generic((EncounterSlot,), "encounter_slots.csv", encounter_slots_from_rows)

    def encounters_from_rows(info: list[str]) -> Iterator[Encounter]:
        yield Encounter(
            id=int(info[0]),
            version_id=int(info[1]),
            location_area_id=int(info[2]),
            encounter_slot_id=int(info[3]),
            pokemon_id=int(info[4]),
            min_level=int(info[5]),
            max_level=int(info[6]),
        )

    build_generic((Encounter,), "encounters.csv", encounters_from_rows)

    def encounter_condition_values_from_rows(info: list[str]) -> Iterator[EncounterConditionValue]:
        yield EncounterConditionValue(
            id=int(info[0]),
            encounter_condition_id=int(info[1]),
            name=info[2],
            is_default=bool(int(info[3])),
        )

    build_generic(
        (EncounterConditionValue,),
        "encounter_condition_values.csv",
        encounter_condition_values_from_rows,
    )

    def encounter_condition_value_names_from_rows(info: list[str]) -> Iterator[EncounterConditionValueName]:
        yield EncounterConditionValueName(
            encounter_condition_value_id=int(info[0]),
            language_id=int(info[1]),
            name=info[2],
        )

    build_generic(
        (EncounterConditionValueName,),
        "encounter_condition_value_prose.csv",
        encounter_condition_value_names_from_rows,
    )

    def encounter_condition_value_maps_from_rows(info: list[str]) -> Iterator[EncounterConditionValueMap]:
        yield EncounterConditionValueMap(encounter_id=int(info[0]), encounter_condition_value_id=int(info[1]))

    build_generic(
        (EncounterConditionValueMap,),
        "encounter_condition_value_map.csv",
        encounter_condition_value_maps_from_rows,
    )

    def encounter_pokemon_details_from_rows(info: list[str]) -> Iterator[EncounterPokemonDetail]:
        yield EncounterPokemonDetail(
            encounter_id=int(info[0]),
            min_perfect_ivs=int(info[1]) if info[1] != "" else None,
            always_shiny=bool(int(info[2])),
            never_shiny=bool(int(info[3])),
            is_alpha=bool(int(info[4])),
        )

    build_generic(
        (EncounterPokemonDetail,),
        "encounter_pokemon_details.csv",
        encounter_pokemon_details_from_rows,
    )


def _build_pal_parks() -> None:
    def pal_park_areas_from_rows(info: list[str]) -> Iterator[PalParkArea]:
        yield PalParkArea(id=int(info[0]), name=info[1])

    build_generic((PalParkArea,), "pal_park_areas.csv", pal_park_areas_from_rows)

    def pal_park_area_names_from_rows(info: list[str]) -> Iterator[PalParkAreaName]:
        yield PalParkAreaName(pal_park_area_id=int(info[0]), language_id=int(info[1]), name=info[2])

    build_generic((PalParkAreaName,), "pal_park_area_names.csv", pal_park_area_names_from_rows)

    def pal_parks_from_rows(info: list[str]) -> Iterator[PalPark]:
        yield PalPark(
            pokemon_species_id=int(info[0]),
            pal_park_area_id=int(info[1]),
            base_score=int(info[2]),
            rate=int(info[3]),
        )

    build_generic((PalPark,), "pal_park.csv", pal_parks_from_rows)


def build_all() -> None:
    _build_languages()
    _build_regions()
    _build_generations()
    _build_versions()
    _build_damage_classes()
    _build_stats()
    _build_abilities()
    _build_characteristics()
    _build_egg_groups()
    _build_growth_rates()
    _build_items()
    _build_types()
    _build_contests()
    _build_moves()
    _build_berries()
    _build_natures()
    _build_genders()
    _build_experiences()
    _build_machines()
    _build_evolutions()
    _build_pokedexes()
    _build_locations()
    _build_pokemons()
    _build_encounters()
    _build_pal_parks()


if __name__ == "__main__":
    build_all()
