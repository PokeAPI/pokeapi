#  To build out the data you'll need to jump into the Django shell
#
#     $ python manage.py shell
#
#  and run the build script with
#
#     $ from data.v2.build import build_all
#     $ build_all()
#
#  Each time the build script is run it will iterate over each table in the database,
#  wipe it and rewrite each row using the data found in data/v2/csv.


import csv
import os
import os.path
import re
import json
from django.db import connection
from pokemon_v2.models import *


# why this way? how about use `__file__`
DATA_LOCATION = "data/v2/csv/"
DATA_LOCATION2 = os.path.join(os.path.dirname(__file__), "csv")
GROUP_RGX = r"\[(.*?)\]\{(.*?)\}"
SUB_RGX = r"\[.*?\]\{.*?\}"

DB_CURSOR = connection.cursor()
DB_VENDOR = connection.vendor


MEDIA_DIR = "{prefix}{{file_name}}".format(
    prefix=os.environ.get(
        "POKEAPI_SPRITES_PREFIX",
        "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/",
    )
)
IMAGE_DIR = os.getcwd() + "/data/v2/sprites/sprites/"
RESOURCE_IMAGES = []

for root, dirs, files in os.walk(IMAGE_DIR):
    for file in files:
        image_path = os.path.join(root.replace(IMAGE_DIR, ""), file)
        image_path = image_path.replace("\\", "/")  # convert Windows-style path to Unix
        RESOURCE_IMAGES.append(image_path)


def file_path_or_none(file_name):
    return (
        MEDIA_DIR.format(file_name=file_name) if file_name in RESOURCE_IMAGES else None
    )


def with_iter(context, iterable=None):
    if iterable is None:
        iterable = context
    with context:
        for value in iterable:
            yield value


def load_data(file_name):
    # with_iter closes the file when it has finished
    return csv.reader(
        with_iter(open(DATA_LOCATION + file_name, "rt", encoding="utf8")), delimiter=","
    )


def clear_table(model):
    table_name = model._meta.db_table
    model.objects.all().delete()
    print("building " + table_name)
    # Reset DB auto increments to start at 1
    if DB_VENDOR == "sqlite":
        DB_CURSOR.execute(
            "DELETE FROM sqlite_sequence WHERE name = " + "'" + table_name + "'"
        )
    else:
        DB_CURSOR.execute(
            "SELECT setval(pg_get_serial_sequence("
            + "'"
            + table_name
            + "'"
            + ",'id'), 1, false);"
        )


def build_generic(model_classes, file_name, csv_record_to_objects):
    batches = {}
    for model_class in model_classes:
        clear_table(model_class)
        batches[model_class] = []  # one batch per model class

    csv_data = load_data(file_name)
    next(csv_data, None)  # skip header

    for csv_record in csv_data:
        for obj in csv_record_to_objects(csv_record):
            model_class = type(obj)
            batches[model_class].append(obj)

            # Limit the batch size
            if len(batches[model_class]) > 200:
                model_class.objects.bulk_create(batches[model_class])
                batches[model_class] = []

    for model_class, batch in batches.items():
        model_class.objects.bulk_create(batch)


def scrub_str(string):
    """
    The purpose of this function is to scrub the weird template mark-up out of strings
    that Veekun is using for their pokedex.
    Example:
        []{move:dragon-tail} will effect the opponents [HP]{mechanic:hp}.
    Becomes:
        dragon tail will effect the opponents HP.

    If you find this results in weird strings please take a stab at improving or re-writing.
    """
    groups = re.findall(GROUP_RGX, string)
    for group in groups:
        if group[0]:
            sub = group[0]
        else:
            sub = group[1].split(":")
            if len(sub) >= 2:
                sub = sub[1]
            else:
                sub = sub[0]
            sub = sub.replace("-", " ")
        string = re.sub(SUB_RGX, sub, string, 1)
    return string


##############
#  LANGUAGE  #
##############


def _build_languages():
    def csv_record_to_objects(info):
        yield Language(
            id=int(info[0]),
            iso639=info[1],
            iso3166=info[2],
            name=info[3],
            official=bool(int(info[4])),
            order=info[5],
        )

    build_generic((Language,), "languages.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield LanguageName(
            language_id=int(info[0]), local_language_id=int(info[1]), name=info[2]
        )

    build_generic((LanguageName,), "language_names.csv", csv_record_to_objects)


############
#  REGION  #
############


def _build_regions():
    def csv_record_to_objects(info):
        yield Region(id=int(info[0]), name=info[1])

    build_generic((Region,), "regions.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield RegionName(region_id=int(info[0]), language_id=int(info[1]), name=info[2])

    build_generic((RegionName,), "region_names.csv", csv_record_to_objects)


################
#  GENERATION  #
################


def _build_generations():
    def csv_record_to_objects(info):
        yield Generation(id=int(info[0]), region_id=int(info[1]), name=info[2])

    build_generic((Generation,), "generations.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield GenerationName(
            generation_id=int(info[0]), language_id=int(info[1]), name=info[2]
        )

    build_generic((GenerationName,), "generation_names.csv", csv_record_to_objects)


#############
#  VERSION  #
#############


def _build_versions():
    def csv_record_to_objects(info):
        yield VersionGroup(
            id=int(info[0]),
            name=info[1],
            generation_id=int(info[2]),
            order=int(info[3]),
        )

    build_generic((VersionGroup,), "version_groups.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield VersionGroupRegion(version_group_id=int(info[0]), region_id=int(info[1]))

    build_generic(
        (VersionGroupRegion,), "version_group_regions.csv", csv_record_to_objects
    )

    def csv_record_to_objects(info):
        yield Version(id=int(info[0]), version_group_id=int(info[1]), name=info[2])

    build_generic((Version,), "versions.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield VersionName(
            version_id=int(info[0]), language_id=int(info[1]), name=info[2]
        )

    build_generic((VersionName,), "version_names.csv", csv_record_to_objects)


##################
#  DAMAGE CLASS  #
##################


def _build_damage_classes():
    def csv_record_to_objects(info):
        yield MoveDamageClass(id=int(info[0]), name=info[1])

    build_generic((MoveDamageClass,), "move_damage_classes.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield MoveDamageClassName(
            move_damage_class_id=int(info[0]), language_id=int(info[1]), name=info[2]
        )
        yield MoveDamageClassDescription(
            move_damage_class_id=int(info[0]),
            language_id=int(info[1]),
            description=info[3],
        )

    build_generic(
        (MoveDamageClassName, MoveDamageClassDescription),
        "move_damage_class_prose.csv",
        csv_record_to_objects,
    )


###########
#  STATS  #
###########


def _build_stats():
    def csv_record_to_objects(info):
        yield Stat(
            id=int(info[0]),
            move_damage_class_id=int(info[1]) if info[1] != "" else None,
            name=info[2],
            is_battle_only=bool(int(info[3])),
            game_index=int(info[4]) if info[4] else 0,
        )

    build_generic((Stat,), "stats.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield StatName(stat_id=int(info[0]), language_id=int(info[1]), name=info[2])

    build_generic((StatName,), "stat_names.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield PokeathlonStat(id=int(info[0]), name=info[1])

    build_generic((PokeathlonStat,), "pokeathlon_stats.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield PokeathlonStatName(
            pokeathlon_stat_id=int(info[0]), language_id=int(info[1]), name=info[2]
        )

    build_generic(
        (PokeathlonStatName,), "pokeathlon_stat_names.csv", csv_record_to_objects
    )


# ###############
# #  ABILITIES  #
# ###############


def _build_abilities():
    def csv_record_to_objects(info):
        yield Ability(
            id=int(info[0]),
            name=info[1],
            generation_id=int(info[2]),
            is_main_series=bool(int(info[3])),
        )

    build_generic((Ability,), "abilities.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield AbilityName(
            ability_id=int(info[0]), language_id=int(info[1]), name=info[2]
        )

    build_generic((AbilityName,), "ability_names.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield AbilityChange(
            id=int(info[0]), ability_id=int(info[1]), version_group_id=int(info[2])
        )

    build_generic((AbilityChange,), "ability_changelog.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield AbilityEffectText(
            ability_id=int(info[0]),
            language_id=int(info[1]),
            short_effect=scrub_str(info[2]),
            effect=scrub_str(info[3]),
        )

    build_generic((AbilityEffectText,), "ability_prose.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield AbilityChangeEffectText(
            ability_change_id=int(info[0]),
            language_id=int(info[1]),
            effect=scrub_str(info[2]),
        )

    build_generic(
        (AbilityChangeEffectText,), "ability_changelog_prose.csv", csv_record_to_objects
    )

    def csv_record_to_objects(info):
        yield AbilityFlavorText(
            ability_id=int(info[0]),
            version_group_id=int(info[1]),
            language_id=int(info[2]),
            flavor_text=info[3],
        )

    build_generic(
        (AbilityFlavorText,), "ability_flavor_text.csv", csv_record_to_objects
    )


####################
#  CHARACTERISTIC  #
####################


def _build_characteristics():
    def csv_record_to_objects(info):
        yield Characteristic(
            id=int(info[0]), stat_id=int(info[1]), gene_mod_5=int(info[2])
        )

    build_generic((Characteristic,), "characteristics.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield CharacteristicDescription(
            characteristic_id=int(info[0]),
            language_id=int(info[1]),
            description=info[2],
        )

    build_generic(
        (CharacteristicDescription,), "characteristic_text.csv", csv_record_to_objects
    )


###############
#  EGG GROUP  #
###############


def _build_egg_groups():
    def csv_record_to_objects(info):
        yield EggGroup(id=int(info[0]), name=info[1])

    build_generic((EggGroup,), "egg_groups.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield EggGroupName(
            egg_group_id=int(info[0]), language_id=int(info[1]), name=info[2]
        )

    build_generic((EggGroupName,), "egg_group_prose.csv", csv_record_to_objects)


#################
#  GROWTH RATE  #
#################


def _build_growth_rates():
    def csv_record_to_objects(info):
        yield GrowthRate(id=int(info[0]), name=info[1], formula=info[2])

    build_generic((GrowthRate,), "growth_rates.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield GrowthRateDescription(
            growth_rate_id=int(info[0]), language_id=int(info[1]), description=info[2]
        )

    build_generic(
        (GrowthRateDescription,), "growth_rate_prose.csv", csv_record_to_objects
    )


# ###########
# #  ITEMS  #
# ###########


def _build_items():
    def csv_record_to_objects(info):
        yield ItemPocket(id=int(info[0]), name=info[1])

    build_generic((ItemPocket,), "item_pockets.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield ItemPocketName(
            item_pocket_id=int(info[0]), language_id=int(info[1]), name=info[2]
        )

    build_generic((ItemPocketName,), "item_pocket_names.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield ItemFlingEffect(id=int(info[0]), name=info[1])

    build_generic((ItemFlingEffect,), "item_fling_effects.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield ItemFlingEffectEffectText(
            item_fling_effect_id=int(info[0]),
            language_id=int(info[1]),
            effect=scrub_str(info[2]),
        )

    build_generic(
        (ItemFlingEffectEffectText,),
        "item_fling_effect_prose.csv",
        csv_record_to_objects,
    )

    def csv_record_to_objects(info):
        yield ItemCategory(id=int(info[0]), item_pocket_id=int(info[1]), name=info[2])

    build_generic((ItemCategory,), "item_categories.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield ItemCategoryName(
            item_category_id=int(info[0]), language_id=int(info[1]), name=info[2]
        )

    build_generic((ItemCategoryName,), "item_category_prose.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield Item(
            id=int(info[0]),
            name=info[1],
            item_category_id=int(info[2]),
            cost=int(info[3]),
            fling_power=int(info[4]) if info[4] != "" else None,
            item_fling_effect_id=int(info[5]) if info[5] != "" else None,
        )

    build_generic((Item,), "items.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        if re.search(r"^data-card", info[1]):
            file_name = "data-card.png"
        elif re.search(r"^tm[0-9]", info[1]):
            file_name = "tm-normal.png"
        elif re.search(r"^hm[0-9]", info[1]):
            file_name = "hm-normal.png"
        else:
            file_name = "%s.png" % info[1]

        item_sprites = "items/{0}"
        sprites = {"default": file_path_or_none(item_sprites.format(file_name))}
        yield ItemSprites(id=int(info[0]), item_id=int(info[0]), sprites=sprites)

    build_generic((ItemSprites,), "items.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield ItemName(item_id=int(info[0]), language_id=int(info[1]), name=info[2])

    build_generic((ItemName,), "item_names.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield ItemEffectText(
            item_id=int(info[0]),
            language_id=int(info[1]),
            short_effect=scrub_str(info[2]),
            effect=scrub_str(info[3]),
        )

    build_generic((ItemEffectText,), "item_prose.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield ItemGameIndex(
            item_id=int(info[0]), generation_id=int(info[1]), game_index=int(info[2])
        )

    build_generic((ItemGameIndex,), "item_game_indices.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield ItemFlavorText(
            item_id=int(info[0]),
            version_group_id=int(info[1]),
            language_id=int(info[2]),
            flavor_text=info[3],
        )

    build_generic((ItemFlavorText,), "item_flavor_text.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield ItemAttribute(id=int(info[0]), name=info[1])

    build_generic((ItemAttribute,), "item_flags.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield ItemAttributeName(
            item_attribute_id=int(info[0]), language_id=int(info[1]), name=info[2]
        )
        yield ItemAttributeDescription(
            item_attribute_id=int(info[0]),
            language_id=int(info[1]),
            description=info[3],
        )

    build_generic(
        (ItemAttributeName, ItemAttributeDescription),
        "item_flag_prose.csv",
        csv_record_to_objects,
    )

    def csv_record_to_objects(info):
        yield ItemAttributeMap(item_id=int(info[0]), item_attribute_id=int(info[1]))

    build_generic((ItemAttributeMap,), "item_flag_map.csv", csv_record_to_objects)


###########
#  TYPES  #
###########


def _build_types():
    def csv_record_to_objects(info):
        yield Type(
            id=int(info[0]),
            name=info[1],
            generation_id=int(info[2]),
            move_damage_class_id=int(info[3]) if info[3] != "" else None,
        )

    build_generic((Type,), "types.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield TypeName(type_id=int(info[0]), language_id=int(info[1]), name=info[2])

    build_generic((TypeName,), "type_names.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield TypeGameIndex(
            type_id=int(info[0]), generation_id=int(info[1]), game_index=int(info[2])
        )

    build_generic((TypeGameIndex,), "type_game_indices.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield TypeEfficacy(
            damage_type_id=int(info[0]),
            target_type_id=int(info[1]),
            damage_factor=int(info[2]),
        )

    build_generic((TypeEfficacy,), "type_efficacy.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield TypeEfficacyPast(
            damage_type_id=int(info[0]),
            target_type_id=int(info[1]),
            damage_factor=int(info[2]),
            generation_id=int(info[3]),
        )

    build_generic((TypeEfficacyPast,), "type_efficacy_past.csv", csv_record_to_objects)


#############
#  CONTEST  #
#############


def _build_contests():
    def csv_record_to_objects(info):
        yield ContestType(id=int(info[0]), name=info[1])

    build_generic((ContestType,), "contest_types.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield ContestTypeName(
            contest_type_id=int(info[0]),
            language_id=int(info[1]),
            name=info[2],
            flavor=info[3],
            color=info[4],
        )

    build_generic((ContestTypeName,), "contest_type_names.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield ContestEffect(id=int(info[0]), appeal=int(info[1]), jam=int(info[2]))

    build_generic((ContestEffect,), "contest_effects.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield ContestEffectEffectText(
            contest_effect_id=int(info[0]), language_id=int(info[1]), effect=info[3]
        )
        yield ContestEffectFlavorText(
            contest_effect_id=int(info[0]),
            language_id=int(info[1]),
            flavor_text=info[2],
        )

    build_generic(
        (ContestEffectEffectText, ContestEffectFlavorText),
        "contest_effect_prose.csv",
        csv_record_to_objects,
    )

    def csv_record_to_objects(info):
        yield SuperContestEffect(id=int(info[0]), appeal=int(info[1]))

    build_generic(
        (SuperContestEffect,), "super_contest_effects.csv", csv_record_to_objects
    )

    def csv_record_to_objects(info):
        yield SuperContestEffectFlavorText(
            super_contest_effect_id=int(info[0]),
            language_id=int(info[1]),
            flavor_text=info[2],
        )

    build_generic(
        (SuperContestEffectFlavorText,),
        "super_contest_effect_prose.csv",
        csv_record_to_objects,
    )


###########
#  MOVES  #
###########


def _build_moves():
    def csv_record_to_objects(info):
        yield MoveEffect(id=int(info[0]))

    build_generic((MoveEffect,), "move_effects.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield MoveEffectEffectText(
            move_effect_id=int(info[0]),
            language_id=int(info[1]),
            short_effect=scrub_str(info[2]),
            effect=scrub_str(info[3]),
        )

    build_generic(
        (MoveEffectEffectText,), "move_effect_prose.csv", csv_record_to_objects
    )

    def csv_record_to_objects(info):
        yield MoveEffectChange(
            id=int(info[0]), move_effect_id=int(info[1]), version_group_id=int(info[2])
        )

    build_generic(
        (MoveEffectChange,), "move_effect_changelog.csv", csv_record_to_objects
    )

    def csv_record_to_objects(info):
        yield MoveEffectChangeEffectText(
            move_effect_change_id=int(info[0]),
            language_id=int(info[1]),
            effect=scrub_str(info[2]),
        )

    build_generic(
        (MoveEffectChangeEffectText,),
        "move_effect_changelog_prose.csv",
        csv_record_to_objects,
    )

    def csv_record_to_objects(info):
        yield MoveLearnMethod(id=int(info[0]), name=info[1])

    build_generic((MoveLearnMethod,), "pokemon_move_methods.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield VersionGroupMoveLearnMethod(
            version_group_id=int(info[0]), move_learn_method_id=int(info[1])
        )

    build_generic(
        (VersionGroupMoveLearnMethod,),
        "version_group_pokemon_move_methods.csv",
        csv_record_to_objects,
    )

    def csv_record_to_objects(info):
        yield MoveLearnMethodName(
            move_learn_method_id=int(info[0]), language_id=int(info[1]), name=info[2]
        )
        yield MoveLearnMethodDescription(
            move_learn_method_id=int(info[0]),
            language_id=int(info[1]),
            description=info[3],
        )

    build_generic(
        (MoveLearnMethodName, MoveLearnMethodDescription),
        "pokemon_move_method_prose.csv",
        csv_record_to_objects,
    )

    def csv_record_to_objects(info):
        yield MoveTarget(id=int(info[0]), name=info[1])

    build_generic((MoveTarget,), "move_targets.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield MoveTargetName(
            move_target_id=int(info[0]), language_id=int(info[1]), name=info[2]
        )
        yield MoveTargetDescription(
            move_target_id=int(info[0]), language_id=int(info[1]), description=info[3]
        )

    build_generic(
        (MoveTargetName, MoveTargetDescription),
        "move_target_prose.csv",
        csv_record_to_objects,
    )

    def csv_record_to_objects(info):
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

    build_generic((Move,), "moves.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield MoveName(move_id=int(info[0]), language_id=int(info[1]), name=info[2])

    build_generic((MoveName,), "move_names.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield MoveFlavorText(
            move_id=int(info[0]),
            version_group_id=int(info[1]),
            language_id=int(info[2]),
            flavor_text=info[3],
        )

    build_generic((MoveFlavorText,), "move_flavor_text.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        _move_effect = None
        try:
            _move_effect = (
                MoveEffect.objects.get(pk=int(info[6])) if info[6] != "" else None
            )
        except:
            pass

        yield MoveChange(
            move_id=int(info[0]),
            version_group_id=int(info[1]),
            type_id=int(info[2]) if info[2] != "" else None,
            power=int(info[3]) if info[3] != "" else None,
            pp=int(info[4]) if info[4] != "" else None,
            accuracy=int(info[5]) if info[5] != "" else None,
            move_effect_id=_move_effect.pk if _move_effect else None,
            move_effect_chance=int(info[7]) if info[7] != "" else None,
        )

    build_generic((MoveChange,), "move_changelog.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield MoveBattleStyle(id=int(info[0]), name=info[1])

    build_generic((MoveBattleStyle,), "move_battle_styles.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield MoveBattleStyleName(
            move_battle_style_id=int(info[0]), language_id=int(info[1]), name=info[2]
        )

    build_generic(
        (MoveBattleStyleName,), "move_battle_style_prose.csv", csv_record_to_objects
    )

    def csv_record_to_objects(info):
        yield MoveAttribute(id=int(info[0]), name=info[1])

    build_generic((MoveAttribute,), "move_flags.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield MoveAttributeMap(move_id=int(info[0]), move_attribute_id=int(info[1]))

    build_generic((MoveAttributeMap,), "move_flag_map.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield MoveAttributeName(
            move_attribute_id=int(info[0]), language_id=int(info[1]), name=info[2]
        )
        yield MoveAttributeDescription(
            move_attribute_id=int(info[0]),
            language_id=int(info[1]),
            description=scrub_str(info[3]),
        )

    build_generic(
        (MoveAttributeName, MoveAttributeDescription),
        "move_flag_prose.csv",
        csv_record_to_objects,
    )

    def csv_record_to_objects(info):
        yield MoveMetaAilment(id=int(info[0]), name=info[1])

    build_generic((MoveMetaAilment,), "move_meta_ailments.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield MoveMetaAilmentName(
            move_meta_ailment_id=int(info[0]), language_id=int(info[1]), name=info[2]
        )

    build_generic(
        (MoveMetaAilmentName,), "move_meta_ailment_names.csv", csv_record_to_objects
    )

    def csv_record_to_objects(info):
        yield MoveMetaCategory(id=int(info[0]), name=info[1])

    build_generic(
        (MoveMetaCategory,), "move_meta_categories.csv", csv_record_to_objects
    )

    def csv_record_to_objects(info):
        yield MoveMetaCategoryDescription(
            move_meta_category_id=int(info[0]),
            language_id=int(info[1]),
            description=info[2],
        )

    build_generic(
        (MoveMetaCategoryDescription,),
        "move_meta_category_prose.csv",
        csv_record_to_objects,
    )

    def csv_record_to_objects(info):
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

    build_generic((MoveMeta,), "move_meta.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield MoveMetaStatChange(
            move_id=int(info[0]), stat_id=int(info[1]), change=int(info[2])
        )

    build_generic(
        (MoveMetaStatChange,), "move_meta_stat_changes.csv", csv_record_to_objects
    )

    def csv_record_to_objects(info):
        yield ContestCombo(first_move_id=int(info[0]), second_move_id=int(info[1]))

    build_generic((ContestCombo,), "contest_combos.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield SuperContestCombo(first_move_id=int(info[0]), second_move_id=int(info[1]))

    build_generic(
        (SuperContestCombo,), "super_contest_combos.csv", csv_record_to_objects
    )


#############
#  BERRIES  #
#############


def _build_berries():
    def csv_record_to_objects(info):
        yield BerryFirmness(id=int(info[0]), name=info[1])

    build_generic((BerryFirmness,), "berry_firmness.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield BerryFirmnessName(
            berry_firmness_id=int(info[0]), language_id=int(info[1]), name=info[2]
        )

    build_generic(
        (BerryFirmnessName,), "berry_firmness_names.csv", csv_record_to_objects
    )

    def csv_record_to_objects(info):
        item = Item.objects.get(pk=int(info[1]))
        yield Berry(
            id=int(info[0]),
            item_id=int(info[1]),
            name=item.name[: item.name.index("-")],
            berry_firmness_id=int(info[2]),
            natural_gift_power=int(info[3]),
            natural_gift_type_id=int(info[4]),
            size=int(info[5]),
            max_harvest=int(info[6]),
            growth_time=int(info[7]),
            soil_dryness=int(info[8]),
            smoothness=int(info[9]),
        )

    build_generic((Berry,), "berries.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        # Get the english name for this contest type
        contest_type_name = ContestTypeName.objects.get(
            contest_type_id=int(info[0]), language_id=9
        )
        yield BerryFlavor(
            id=int(info[0]),
            name=contest_type_name.flavor.lower(),
            contest_type=ContestType.objects.get(pk=int(info[0])),
        )

    # This is not an error
    build_generic((BerryFlavor,), "contest_types.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield BerryFlavorName(
            berry_flavor_id=int(info[0]), language_id=int(info[1]), name=info[3]
        )

    # This is not an error
    build_generic((BerryFlavorName,), "contest_type_names.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield BerryFlavorMap(
            berry_id=int(info[0]), berry_flavor_id=int(info[1]), potency=int(info[2])
        )

    # This is not an error
    build_generic((BerryFlavorMap,), "berry_flavors.csv", csv_record_to_objects)


############
#  NATURE  #
############


def _build_natures():
    def csv_record_to_objects(info):
        decreased_stat = None
        increased_stat = None
        hates_flavor = None
        likes_flavor = None

        if info[2] != info[3]:
            decreased_stat = Stat.objects.get(pk=int(info[2]))
            increased_stat = Stat.objects.get(pk=int(info[3]))

        if info[4] != info[5]:
            hates_flavor = BerryFlavor.objects.get(pk=int(info[4]))
            likes_flavor = BerryFlavor.objects.get(pk=int(info[5]))

        yield Nature(
            id=int(info[0]),
            name=info[1],
            decreased_stat=decreased_stat,
            increased_stat=increased_stat,
            hates_flavor=hates_flavor,
            likes_flavor=likes_flavor,
            game_index=info[6],
        )

    build_generic((Nature,), "natures.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield NatureName(nature_id=int(info[0]), language_id=int(info[1]), name=info[2])

    build_generic((NatureName,), "nature_names.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield NaturePokeathlonStat(
            nature_id=(info[0]), pokeathlon_stat_id=(info[1]), max_change=info[2]
        )

    build_generic(
        (NaturePokeathlonStat,), "nature_pokeathlon_stats.csv", csv_record_to_objects
    )

    def csv_record_to_objects(info):
        yield NatureBattleStylePreference(
            nature_id=int(info[0]),
            move_battle_style_id=int(info[1]),
            low_hp_preference=info[2],
            high_hp_preference=info[3],
        )

    build_generic(
        (NatureBattleStylePreference,),
        "nature_battle_style_preferences.csv",
        csv_record_to_objects,
    )


###########
# GENDER  #
###########


def _build_genders():
    def csv_record_to_objects(info):
        yield Gender(id=int(info[0]), name=info[1])

    build_generic((Gender,), "genders.csv", csv_record_to_objects)


################
#  EXPERIENCE  #
################


def _build_experiences():
    def csv_record_to_objects(info):
        yield Experience(
            growth_rate_id=int(info[0]), level=int(info[1]), experience=int(info[2])
        )

    build_generic((Experience,), "experience.csv", csv_record_to_objects)


##############
#  MACHINES  #
##############


def _build_machines():
    def csv_record_to_objects(info):
        yield Machine(
            machine_number=int(info[0]),
            version_group_id=int(info[1]),
            item_id=int(info[2]),
            move_id=int(info[3]),
        )

    build_generic((Machine,), "machines.csv", csv_record_to_objects)


###############
#  EVOLUTION  #
###############


def _build_evolutions():
    def csv_record_to_objects(info):
        yield EvolutionChain(
            id=int(info[0]),
            baby_trigger_item_id=int(info[1]) if info[1] != "" else None,
        )

    build_generic((EvolutionChain,), "evolution_chains.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield EvolutionTrigger(id=int(info[0]), name=info[1])

    build_generic((EvolutionTrigger,), "evolution_triggers.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield EvolutionTriggerName(
            evolution_trigger_id=int(info[0]), language_id=int(info[1]), name=info[2]
        )

    build_generic(
        (EvolutionTriggerName,), "evolution_trigger_prose.csv", csv_record_to_objects
    )


#############
#  POKEDEX  #
#############


def _build_pokedexes():
    def csv_record_to_objects(info):
        yield Pokedex(
            id=int(info[0]),
            region_id=int(info[1]) if info[1] != "" else None,
            name=info[2],
            is_main_series=bool(int(info[3])),
        )

    build_generic((Pokedex,), "pokedexes.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield PokedexName(
            pokedex_id=int(info[0]), language_id=int(info[1]), name=info[2]
        )
        yield PokedexDescription(
            pokedex_id=int(info[0]), language_id=int(info[1]), description=info[3]
        )

    build_generic(
        (PokedexName, PokedexDescription), "pokedex_prose.csv", csv_record_to_objects
    )

    def csv_record_to_objects(info):
        yield PokedexVersionGroup(
            pokedex_id=int(info[0]), version_group_id=int(info[1])
        )

    build_generic(
        (PokedexVersionGroup,), "pokedex_version_groups.csv", csv_record_to_objects
    )


##############
#  LOCATION  #
##############


def _build_locations():
    def csv_record_to_objects(info):
        yield Location(
            id=int(info[0]),
            region_id=int(info[1]) if info[1] != "" else None,
            name=info[2],
        )

    build_generic((Location,), "locations.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield LocationName(
            location_id=int(info[0]), language_id=int(info[1]), name=info[2]
        )

    build_generic((LocationName,), "location_names.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield LocationGameIndex(
            location_id=int(info[0]),
            generation_id=int(info[1]),
            game_index=int(info[2]),
        )

    build_generic(
        (LocationGameIndex,), "location_game_indices.csv", csv_record_to_objects
    )

    def csv_record_to_objects(info):
        location = Location.objects.get(pk=int(info[1]))
        yield LocationArea(
            id=int(info[0]),
            location_id=int(info[1]),
            game_index=int(info[2]),
            name="{}-{}".format(location.name, info[3])
            if info[3]
            else "{}-{}".format(location.name, "area"),
        )

    build_generic((LocationArea,), "location_areas.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield LocationAreaName(
            location_area_id=int(info[0]), language_id=int(info[1]), name=info[2]
        )

    build_generic((LocationAreaName,), "location_area_prose.csv", csv_record_to_objects)


#############
#  POKEMON  #
#############


def _build_pokemons():
    def csv_record_to_objects(info):
        yield PokemonColor(id=int(info[0]), name=info[1])

    build_generic((PokemonColor,), "pokemon_colors.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield PokemonColorName(
            pokemon_color_id=int(info[0]), language_id=int(info[1]), name=info[2]
        )

    build_generic((PokemonColorName,), "pokemon_color_names.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield PokemonShape(id=int(info[0]), name=info[1])

    build_generic((PokemonShape,), "pokemon_shapes.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield PokemonShapeName(
            pokemon_shape_id=int(info[0]),
            language_id=int(info[1]),
            name=info[2],
            awesome_name=info[3],
        )

    build_generic((PokemonShapeName,), "pokemon_shape_prose.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield PokemonHabitat(id=int(info[0]), name=info[1])

    build_generic((PokemonHabitat,), "pokemon_habitats.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
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

    build_generic((PokemonSpecies,), "pokemon_species.csv", csv_record_to_objects)

    # PokemonSpecies.evolves_from_species can't be set until all the species are created
    data = load_data("pokemon_species.csv")
    for index, info in enumerate(data):
        if index > 0:
            evolves = (
                PokemonSpecies.objects.get(pk=int(info[3])) if info[3] != "" else None
            )
            if evolves:
                species = PokemonSpecies.objects.get(pk=int(info[0]))
                species.evolves_from_species = evolves
                species.save()

    def csv_record_to_objects(info):
        yield PokemonSpeciesName(
            pokemon_species_id=int(info[0]),
            language_id=int(info[1]),
            name=info[2],
            genus=info[3],
        )

    build_generic(
        (PokemonSpeciesName,), "pokemon_species_names.csv", csv_record_to_objects
    )

    def csv_record_to_objects(info):
        yield PokemonSpeciesDescription(
            pokemon_species_id=int(info[0]),
            language_id=int(info[1]),
            description=scrub_str(info[2]),
        )

    build_generic(
        (PokemonSpeciesDescription,), "pokemon_species_prose.csv", csv_record_to_objects
    )

    def csv_record_to_objects(info):
        yield PokemonSpeciesFlavorText(
            pokemon_species_id=int(info[0]),
            version_id=int(info[1]),
            language_id=int(info[2]),
            flavor_text=info[3],
        )

    build_generic(
        (PokemonSpeciesFlavorText,),
        "pokemon_species_flavor_text.csv",
        csv_record_to_objects,
    )

    def csv_record_to_objects(info):
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

    build_generic((Pokemon,), "pokemon.csv", csv_record_to_objects)

    def try_image_names(path, info, extension):
        # poke_sprites = "pokemon/{0}"
        pokemon_id = info[0]
        identifier = info[1]
        species_id = info[2]
        if "-" in identifier:
            form_file_name = "%s.%s" % (
                species_id + "-" + identifier.split("-", 1)[1],
                extension,
            )
            id_file_name = "%s.%s" % (pokemon_id, extension)
            file_name = (
                id_file_name
                if file_path_or_none(path + id_file_name)
                else form_file_name
            )
        else:
            file_name = "%s.%s" % (info[0], extension)
        return file_path_or_none(path + file_name)

    def csv_record_to_objects(info):
        poke_sprites = "pokemon/"
        dream_world = "other/dream-world/"
        home = "other/home/"
        official_art = "other/official-artwork/"
        showdown = "other/showdown/"
        gen_i = "versions/generation-i/"
        gen_ii = "versions/generation-ii/"
        gen_iii = "versions/generation-iii/"
        gen_iv = "versions/generation-iv/"
        gen_v = "versions/generation-v/"
        gen_vi = "versions/generation-vi/"
        gen_vii = "versions/generation-vii/"
        gen_viii = "versions/generation-viii/"
        sprites = {
            "front_default": try_image_names(poke_sprites, info, "png"),
            "front_female": try_image_names(poke_sprites + "female/", info, "png"),
            "front_shiny": try_image_names(poke_sprites + "shiny/", info, "png"),
            "front_shiny_female": try_image_names(
                poke_sprites + "shiny/female/", info, "png"
            ),
            "back_default": try_image_names(poke_sprites + "back/", info, "png"),
            "back_female": try_image_names(poke_sprites + "back/female/", info, "png"),
            "back_shiny": try_image_names(poke_sprites + "back/shiny/", info, "png"),
            "back_shiny_female": try_image_names(
                poke_sprites + "back/shiny/female/", info, "png"
            ),
            "other": {
                "dream_world": {
                    "front_default": try_image_names(
                        poke_sprites + dream_world, info, "svg"
                    ),
                    "front_female": try_image_names(
                        poke_sprites + dream_world + "female/", info, "svg"
                    ),
                },
                "home": {
                    "front_default": try_image_names(poke_sprites + home, info, "png"),
                    "front_female": try_image_names(
                        poke_sprites + home + "female/", info, "png"
                    ),
                    "front_shiny": try_image_names(
                        poke_sprites + home + "shiny/", info, "png"
                    ),
                    "front_shiny_female": try_image_names(
                        poke_sprites + home + "shiny/female/", info, "png"
                    ),
                },
                "official-artwork": {
                    "front_default": try_image_names(
                        poke_sprites + official_art, info, "png"
                    ),
                    "front_shiny": try_image_names(
                        poke_sprites + official_art + "shiny/", info, "png"
                    ),
                },
                "showdown": {
                    "front_default": try_image_names(
                        poke_sprites + showdown, info, "gif"
                    ),
                    "front_shiny": try_image_names(
                        poke_sprites + showdown + "shiny/", info, "gif"
                    ),
                    "front_female": try_image_names(
                        poke_sprites + showdown + "female/", info, "gif"
                    ),
                    "front_shiny_female": try_image_names(
                        poke_sprites + showdown + "shiny/female/", info, "gif"
                    ),
                    "back_default": try_image_names(
                        poke_sprites + showdown + "back/", info, "gif"
                    ),
                    "back_shiny": try_image_names(
                        poke_sprites + showdown + "back/shiny/", info, "gif"
                    ),
                    "back_female": try_image_names(
                        poke_sprites + showdown + "back/female/", info, "gif"
                    ),
                    "back_shiny_female": try_image_names(
                        poke_sprites + showdown + "back/shiny/female", info, "gif"
                    ),
                },
            },
            "versions": {
                "generation-i": {
                    "red-blue": {
                        "front_default": try_image_names(
                            poke_sprites + gen_i + "red-blue/", info, "png"
                        ),
                        "front_gray": try_image_names(
                            poke_sprites + gen_i + "red-blue/gray/", info, "png"
                        ),
                        "back_default": try_image_names(
                            poke_sprites + gen_i + "red-blue/back/", info, "png"
                        ),
                        "back_gray": try_image_names(
                            poke_sprites + gen_i + "red-blue/back/gray/", info, "png"
                        ),
                        "front_transparent": try_image_names(
                            poke_sprites + gen_i + "red-blue/transparent/", info, "png"
                        ),
                        "back_transparent": try_image_names(
                            poke_sprites + gen_i + "red-blue/transparent/back/",
                            info,
                            "png",
                        ),
                    },
                    "yellow": {
                        "front_default": try_image_names(
                            poke_sprites + gen_i + "yellow/", info, "png"
                        ),
                        "front_gray": try_image_names(
                            poke_sprites + gen_i + "yellow/gray/", info, "png"
                        ),
                        "back_default": try_image_names(
                            poke_sprites + gen_i + "yellow/back/", info, "png"
                        ),
                        "back_gray": try_image_names(
                            poke_sprites + gen_i + "yellow/back/gray/", info, "png"
                        ),
                        "front_transparent": try_image_names(
                            poke_sprites + gen_i + "yellow/transparent/", info, "png"
                        ),
                        "back_transparent": try_image_names(
                            poke_sprites + gen_i + "yellow/transparent/back/",
                            info,
                            "png",
                        ),
                    },
                },
                "generation-ii": {
                    "crystal": {
                        "front_default": try_image_names(
                            poke_sprites + gen_ii + "crystal/", info, "png"
                        ),
                        "front_shiny": try_image_names(
                            poke_sprites + gen_ii + "crystal/shiny/", info, "png"
                        ),
                        "back_default": try_image_names(
                            poke_sprites + gen_ii + "crystal/back/", info, "png"
                        ),
                        "back_shiny": try_image_names(
                            poke_sprites + gen_ii + "crystal/back/shiny/", info, "png"
                        ),
                        "front_transparent": try_image_names(
                            poke_sprites + gen_ii + "crystal/transparent/", info, "png"
                        ),
                        "front_shiny_transparent": try_image_names(
                            poke_sprites + gen_ii + "crystal/transparent/shiny/",
                            info,
                            "png",
                        ),
                        "back_transparent": try_image_names(
                            poke_sprites + gen_ii + "crystal/transparent/back/",
                            info,
                            "png",
                        ),
                        "back_shiny_transparent": try_image_names(
                            poke_sprites + gen_ii + "crystal/transparent/back/shiny/",
                            info,
                            "png",
                        ),
                    },
                    "gold": {
                        "front_default": try_image_names(
                            poke_sprites + gen_ii + "gold/", info, "png"
                        ),
                        "front_shiny": try_image_names(
                            poke_sprites + gen_ii + "gold/shiny/", info, "png"
                        ),
                        "back_default": try_image_names(
                            poke_sprites + gen_ii + "gold/back/", info, "png"
                        ),
                        "back_shiny": try_image_names(
                            poke_sprites + gen_ii + "gold/back/shiny/", info, "png"
                        ),
                        "front_transparent": try_image_names(
                            poke_sprites + gen_ii + "gold/transparent/", info, "png"
                        ),
                    },
                    "silver": {
                        "front_default": try_image_names(
                            poke_sprites + gen_ii + "silver/", info, "png"
                        ),
                        "front_shiny": try_image_names(
                            poke_sprites + gen_ii + "silver/shiny/", info, "png"
                        ),
                        "back_default": try_image_names(
                            poke_sprites + gen_ii + "silver/back/", info, "png"
                        ),
                        "back_shiny": try_image_names(
                            poke_sprites + gen_ii + "silver/back/shiny/", info, "png"
                        ),
                        "front_transparent": try_image_names(
                            poke_sprites + gen_ii + "silver/transparent/", info, "png"
                        ),
                    },
                },
                "generation-iii": {
                    "emerald": {
                        "front_default": try_image_names(
                            poke_sprites + gen_iii + "emerald/", info, "png"
                        ),
                        "front_shiny": try_image_names(
                            poke_sprites + gen_iii + "emerald/shiny/", info, "png"
                        ),
                    },
                    "firered-leafgreen": {
                        "front_default": try_image_names(
                            poke_sprites + gen_iii + "firered-leafgreen/", info, "png"
                        ),
                        "front_shiny": try_image_names(
                            poke_sprites + gen_iii + "firered-leafgreen/shiny/",
                            info,
                            "png",
                        ),
                        "back_default": try_image_names(
                            poke_sprites + gen_iii + "firered-leafgreen/back/",
                            info,
                            "png",
                        ),
                        "back_shiny": try_image_names(
                            poke_sprites + gen_iii + "firered-leafgreen/back/shiny/",
                            info,
                            "png",
                        ),
                    },
                    "ruby-sapphire": {
                        "front_default": try_image_names(
                            poke_sprites + gen_iii + "ruby-sapphire/", info, "png"
                        ),
                        "front_shiny": try_image_names(
                            poke_sprites + gen_iii + "ruby-sapphire/shiny/",
                            info,
                            "png",
                        ),
                        "back_default": try_image_names(
                            poke_sprites + gen_iii + "ruby-sapphire/back/",
                            info,
                            "png",
                        ),
                        "back_shiny": try_image_names(
                            poke_sprites + gen_iii + "ruby-sapphire/back/shiny/",
                            info,
                            "png",
                        ),
                    },
                },
                "generation-iv": {
                    "diamond-pearl": {
                        "front_default": try_image_names(
                            poke_sprites + gen_iv + "diamond-pearl/", info, "png"
                        ),
                        "front_female": try_image_names(
                            poke_sprites + gen_iv + "diamond-pearl/female/",
                            info,
                            "png",
                        ),
                        "front_shiny": try_image_names(
                            poke_sprites + gen_iv + "diamond-pearl/shiny/",
                            info,
                            "png",
                        ),
                        "front_shiny_female": try_image_names(
                            poke_sprites + gen_iv + "diamond-pearl/shiny/female/",
                            info,
                            "png",
                        ),
                        "back_default": try_image_names(
                            poke_sprites + gen_iv + "diamond-pearl/back/", info, "png"
                        ),
                        "back_female": try_image_names(
                            poke_sprites + gen_iv + "diamond-pearl/back/female/",
                            info,
                            "png",
                        ),
                        "back_shiny": try_image_names(
                            poke_sprites + gen_iv + "diamond-pearl/back/shiny/",
                            info,
                            "png",
                        ),
                        "back_shiny_female": try_image_names(
                            poke_sprites + gen_iv + "diamond-pearl/back/shiny/female/",
                            info,
                            "png",
                        ),
                    },
                    "heartgold-soulsilver": {
                        "front_default": try_image_names(
                            poke_sprites + gen_iv + "heartgold-soulsilver/",
                            info,
                            "png",
                        ),
                        "front_female": try_image_names(
                            poke_sprites + gen_iv + "heartgold-soulsilver/female/",
                            info,
                            "png",
                        ),
                        "front_shiny": try_image_names(
                            poke_sprites + gen_iv + "heartgold-soulsilver/shiny/",
                            info,
                            "png",
                        ),
                        "front_shiny_female": try_image_names(
                            poke_sprites
                            + gen_iv
                            + "heartgold-soulsilver/shiny/female/",
                            info,
                            "png",
                        ),
                        "back_default": try_image_names(
                            poke_sprites + gen_iv + "heartgold-soulsilver/back/",
                            info,
                            "png",
                        ),
                        "back_female": try_image_names(
                            poke_sprites + gen_iv + "heartgold-soulsilver/back/female/",
                            info,
                            "png",
                        ),
                        "back_shiny": try_image_names(
                            poke_sprites + gen_iv + "heartgold-soulsilver/back/shiny/",
                            info,
                            "png",
                        ),
                        "back_shiny_female": try_image_names(
                            poke_sprites
                            + gen_iv
                            + "heartgold-soulsilver/back/shiny/female/",
                            info,
                            "png",
                        ),
                    },
                    "platinum": {
                        "front_default": try_image_names(
                            poke_sprites + gen_iv + "platinum/", info, "png"
                        ),
                        "front_female": try_image_names(
                            poke_sprites + gen_iv + "platinum/female/", info, "png"
                        ),
                        "front_shiny": try_image_names(
                            poke_sprites + gen_iv + "platinum/shiny/", info, "png"
                        ),
                        "front_shiny_female": try_image_names(
                            poke_sprites + gen_iv + "platinum/shiny/female/",
                            info,
                            "png",
                        ),
                        "back_default": try_image_names(
                            poke_sprites + gen_iv + "platinum/back/", info, "png"
                        ),
                        "back_female": try_image_names(
                            poke_sprites + gen_iv + "platinum/back/female/",
                            info,
                            "png",
                        ),
                        "back_shiny": try_image_names(
                            poke_sprites + gen_iv + "platinum/back/shiny/",
                            info,
                            "png",
                        ),
                        "back_shiny_female": try_image_names(
                            poke_sprites + gen_iv + "platinum/back/shiny/female/",
                            info,
                            "png",
                        ),
                    },
                },
                "generation-v": {
                    "black-white": {
                        "front_default": try_image_names(
                            poke_sprites + gen_v + "black-white/", info, "png"
                        ),
                        "front_female": try_image_names(
                            poke_sprites + gen_v + "black-white/female/", info, "png"
                        ),
                        "front_shiny": try_image_names(
                            poke_sprites + gen_v + "black-white/shiny/", info, "png"
                        ),
                        "front_shiny_female": try_image_names(
                            poke_sprites + gen_v + "black-white/shiny/female/",
                            info,
                            "png",
                        ),
                        "back_default": try_image_names(
                            poke_sprites + gen_v + "black-white/back/", info, "png"
                        ),
                        "back_female": try_image_names(
                            poke_sprites + gen_v + "black-white/back/female/",
                            info,
                            "png",
                        ),
                        "back_shiny": try_image_names(
                            poke_sprites + gen_v + "black-white/back/shiny/",
                            info,
                            "png",
                        ),
                        "back_shiny_female": try_image_names(
                            poke_sprites + gen_v + "black-white/back/shiny/female/",
                            info,
                            "png",
                        ),
                        "animated": {
                            "front_default": try_image_names(
                                poke_sprites + gen_v + "black-white/animated/",
                                info,
                                "gif",
                            ),
                            "front_female": try_image_names(
                                poke_sprites + gen_v + "black-white/animated/female/",
                                info,
                                "gif",
                            ),
                            "front_shiny": try_image_names(
                                poke_sprites + gen_v + "black-white/animated/shiny/",
                                info,
                                "gif",
                            ),
                            "front_shiny_female": try_image_names(
                                poke_sprites
                                + gen_v
                                + "black-white/animated/shiny/female/",
                                info,
                                "gif",
                            ),
                            "back_default": try_image_names(
                                poke_sprites + gen_v + "black-white/animated/back/",
                                info,
                                "gif",
                            ),
                            "back_female": try_image_names(
                                poke_sprites
                                + gen_v
                                + "black-white/animated/back/female/",
                                info,
                                "gif",
                            ),
                            "back_shiny": try_image_names(
                                poke_sprites
                                + gen_v
                                + "black-white/animated/back/shiny/",
                                info,
                                "gif",
                            ),
                            "back_shiny_female": try_image_names(
                                poke_sprites
                                + gen_v
                                + "black-white/animated/back/shiny/female/",
                                info,
                                "gif",
                            ),
                        },
                    }
                },
                "generation-vi": {
                    "omegaruby-alphasapphire": {
                        "front_default": try_image_names(
                            poke_sprites + gen_vi + "omegaruby-alphasapphire/",
                            info,
                            "png",
                        ),
                        "front_female": try_image_names(
                            poke_sprites + gen_vi + "omegaruby-alphasapphire/female/",
                            info,
                            "png",
                        ),
                        "front_shiny": try_image_names(
                            poke_sprites + gen_vi + "omegaruby-alphasapphire/shiny/",
                            info,
                            "png",
                        ),
                        "front_shiny_female": try_image_names(
                            poke_sprites
                            + gen_vi
                            + "omegaruby-alphasapphire/shiny/female/",
                            info,
                            "png",
                        ),
                    },
                    "x-y": {
                        "front_default": try_image_names(
                            poke_sprites + gen_vi + "x-y/", info, "png"
                        ),
                        "front_female": try_image_names(
                            poke_sprites + gen_vi + "x-y/female/", info, "png"
                        ),
                        "front_shiny": try_image_names(
                            poke_sprites + gen_vi + "x-y/shiny/", info, "png"
                        ),
                        "front_shiny_female": try_image_names(
                            poke_sprites + gen_vi + "x-y/shiny/female/", info, "png"
                        ),
                    },
                },
                "generation-vii": {
                    "ultra-sun-ultra-moon": {
                        "front_default": try_image_names(
                            poke_sprites + gen_vii + "ultra-sun-ultra-moon/",
                            info,
                            "png",
                        ),
                        "front_female": try_image_names(
                            poke_sprites + gen_vii + "ultra-sun-ultra-moon/female/",
                            info,
                            "png",
                        ),
                        "front_shiny": try_image_names(
                            poke_sprites + gen_vii + "ultra-sun-ultra-moon/shiny/",
                            info,
                            "png",
                        ),
                        "front_shiny_female": try_image_names(
                            poke_sprites
                            + gen_vii
                            + "ultra-sun-ultra-moon/shiny/female/",
                            info,
                            "png",
                        ),
                    },
                    "icons": {
                        "front_default": try_image_names(
                            poke_sprites + gen_vii + "icons/", info, "png"
                        ),
                        "front_female": try_image_names(
                            poke_sprites + gen_vii + "icons/female/", info, "png"
                        ),
                    },
                },
                "generation-viii": {
                    "icons": {
                        "front_default": try_image_names(
                            poke_sprites + gen_viii + "icons/", info, "png"
                        ),
                        "front_female": try_image_names(
                            poke_sprites + gen_viii + "icons/female/", info, "png"
                        ),
                    },
                },
            },
        }
        yield PokemonSprites(
            id=int(info[0]),
            pokemon=Pokemon.objects.get(pk=int(info[0])),
            sprites=sprites,
        )

    build_generic((PokemonSprites,), "pokemon.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield PokemonAbility(
            pokemon_id=int(info[0]),
            ability_id=int(info[1]),
            is_hidden=bool(int(info[2])),
            slot=int(info[3]),
        )

    build_generic((PokemonAbility,), "pokemon_abilities.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield PokemonAbilityPast(
            pokemon_id=int(info[0]),
            generation_id=int(info[1]),
            ability_id=int(info[2]),
            is_hidden=bool(int(info[3])),
            slot=int(info[4]),
        )

    build_generic(
        (PokemonAbilityPast,), "pokemon_abilities_past.csv", csv_record_to_objects
    )

    def csv_record_to_objects(info):
        yield PokemonDexNumber(
            pokemon_species_id=int(info[0]),
            pokedex_id=int(info[1]),
            pokedex_number=int(info[2]),
        )

    build_generic((PokemonDexNumber,), "pokemon_dex_numbers.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield PokemonEggGroup(
            pokemon_species_id=int(info[0]), egg_group_id=int(info[1])
        )

    build_generic((PokemonEggGroup,), "pokemon_egg_groups.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield PokemonEvolution(
            id=int(info[0]),
            evolved_species_id=int(info[1]),
            evolution_trigger_id=int(info[2]),
            evolution_item_id=int(info[3]) if info[3] != "" else None,
            min_level=int(info[4]) if info[4] != "" else None,
            gender_id=int(info[5]) if info[5] != "" else None,
            location_id=int(info[6]) if info[6] != "" else None,
            held_item_id=int(info[7]) if info[7] != "" else None,
            time_of_day=info[8],
            known_move_id=int(info[9]) if info[9] != "" else None,
            known_move_type_id=int(info[10]) if info[10] != "" else None,
            min_happiness=int(info[11]) if info[11] != "" else None,
            min_beauty=int(info[12]) if info[12] != "" else None,
            min_affection=int(info[13]) if info[13] != "" else None,
            relative_physical_stats=int(info[14]) if info[14] != "" else None,
            party_species_id=int(info[15]) if info[15] != "" else None,
            party_type_id=int(info[16]) if info[16] != "" else None,
            trade_species_id=int(info[17]) if info[17] != "" else None,
            needs_overworld_rain=bool(int(info[18])),
            turn_upside_down=bool(int(info[19])),
        )

    build_generic((PokemonEvolution,), "pokemon_evolution.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
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

    build_generic((PokemonForm,), "pokemon_forms.csv", csv_record_to_objects)

    def try_image_names(path, info, extension):
        form_identifier = info[2]
        pokemon_id = info[3]
        pokemon = Pokemon.objects.get(pk=int(pokemon_id))
        species_id = getattr(pokemon, "pokemon_species_id")
        is_default = int(info[5])
        if form_identifier:
            form_file_name = "%s-%s.%s" % (species_id, form_identifier, extension)
            id_file_name = "%s.%s" % (pokemon_id, extension)
            file_name = (
                id_file_name
                if file_path_or_none(path + id_file_name)
                else form_file_name
            )
            if id_file_name and form_file_name and (not is_default):
                file_name = form_file_name
        else:
            file_name = "%s.%s" % (species_id, extension)
        return file_path_or_none(path + file_name)

    def csv_record_to_objects(info):
        poke_sprites = "pokemon/"
        sprites = {
            "front_default": try_image_names(poke_sprites, info, "png"),
            "front_shiny": try_image_names(poke_sprites + "shiny/", info, "png"),
            "back_default": try_image_names(poke_sprites + "back/", info, "png"),
            "back_shiny": try_image_names(poke_sprites + "back/shiny/", info, "png"),
            "front_female": try_image_names(poke_sprites + "female/", info, "png"),
            "front_shiny_female": try_image_names(
                poke_sprites + "shiny/female/", info, "png"
            ),
            "back_female": try_image_names(poke_sprites + "back/female/", info, "png"),
            "back_shiny_female": try_image_names(
                poke_sprites + "back/shiny/female/", info, "png"
            ),
        }
        yield PokemonFormSprites(
            id=int(info[0]), pokemon_form_id=int(info[0]), sprites=sprites
        )

    build_generic((PokemonFormSprites,), "pokemon_forms.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield PokemonFormName(
            pokemon_form=PokemonForm.objects.get(pk=int(info[0])),
            language=Language.objects.get(pk=int(info[1])),
            name=info[2],
            pokemon_name=info[3],
        )

    build_generic((PokemonFormName,), "pokemon_form_names.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield PokemonFormGeneration(
            pokemon_form_id=int(info[0]),
            generation_id=int(info[1]),
            game_index=int(info[2]),
        )

    build_generic(
        (PokemonFormGeneration,), "pokemon_form_generations.csv", csv_record_to_objects
    )

    def csv_record_to_objects(info):
        yield PokemonFormType(
            pokemon_form_id=int(info[0]), type_id=int(info[1]), slot=int(info[2])
        )

    build_generic((PokemonFormType,), "pokemon_form_types.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield PokemonGameIndex(
            pokemon_id=int(info[0]), version_id=int(info[1]), game_index=int(info[2])
        )

    build_generic(
        (PokemonGameIndex,), "pokemon_game_indices.csv", csv_record_to_objects
    )

    def csv_record_to_objects(info):
        yield PokemonHabitatName(
            pokemon_habitat_id=int(info[0]), language_id=int(info[1]), name=info[2]
        )

    build_generic(
        (PokemonHabitatName,), "pokemon_habitat_names.csv", csv_record_to_objects
    )

    def csv_record_to_objects(info):
        yield PokemonItem(
            pokemon_id=int(info[0]),
            version_id=int(info[1]),
            item_id=int(info[2]),
            rarity=int(info[3]),
        )

    build_generic((PokemonItem,), "pokemon_items.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield PokemonMove(
            pokemon_id=int(info[0]),
            version_group_id=int(info[1]),
            move_id=int(info[2]),
            move_learn_method_id=int(info[3]),
            level=int(info[4]),
            order=int(info[5]) if info[5] != "" else None,
        )

    build_generic((PokemonMove,), "pokemon_moves.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield PokemonStat(
            pokemon_id=int(info[0]),
            stat_id=int(info[1]),
            base_stat=int(info[2]),
            effort=int(info[3]),
        )

    build_generic((PokemonStat,), "pokemon_stats.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield PokemonType(
            pokemon_id=int(info[0]), type_id=int(info[1]), slot=int(info[2])
        )

    build_generic((PokemonType,), "pokemon_types.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield PokemonTypePast(
            pokemon_id=int(info[0]),
            generation_id=int(info[1]),
            type_id=int(info[2]),
            slot=int(info[3]),
        )

    build_generic((PokemonTypePast,), "pokemon_types_past.csv", csv_record_to_objects)


###############
#  ENCOUNTER  #
###############


def _build_encounters():
    def csv_record_to_objects(info):
        yield EncounterMethod(id=int(info[0]), name=info[1], order=int(info[2]))

    build_generic((EncounterMethod,), "encounter_methods.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield LocationAreaEncounterRate(
            location_area_id=int(info[0]),
            encounter_method_id=int(info[1]),
            version_id=int(info[2]),
            rate=int(info[3]),
        )

    build_generic(
        (LocationAreaEncounterRate,),
        "location_area_encounter_rates.csv",
        csv_record_to_objects,
    )

    def csv_record_to_objects(info):
        yield EncounterMethodName(
            encounter_method_id=int(info[0]), language_id=int(info[1]), name=info[2]
        )

    build_generic(
        (EncounterMethodName,), "encounter_method_prose.csv", csv_record_to_objects
    )

    def csv_record_to_objects(info):
        yield EncounterCondition(id=int(info[0]), name=info[1])

    build_generic(
        (EncounterCondition,), "encounter_conditions.csv", csv_record_to_objects
    )

    def csv_record_to_objects(info):
        yield EncounterConditionName(
            encounter_condition_id=int(info[0]), language_id=int(info[1]), name=info[2]
        )

    build_generic(
        (EncounterConditionName,),
        "encounter_condition_prose.csv",
        csv_record_to_objects,
    )

    def csv_record_to_objects(info):
        yield EncounterSlot(
            id=int(info[0]),
            version_group_id=int(info[1]),
            encounter_method_id=int(info[2]),
            slot=int(info[3]) if info[3] != "" else None,
            rarity=int(info[4]),
        )

    build_generic((EncounterSlot,), "encounter_slots.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield Encounter(
            id=int(info[0]),
            version_id=int(info[1]),
            location_area_id=int(info[2]),
            encounter_slot_id=int(info[3]),
            pokemon_id=int(info[4]),
            min_level=int(info[5]),
            max_level=int(info[6]),
        )

    build_generic((Encounter,), "encounters.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield EncounterConditionValue(
            id=int(info[0]),
            encounter_condition_id=int(info[1]),
            name=info[2],
            is_default=bool(int(info[3])),
        )

    build_generic(
        (EncounterConditionValue,),
        "encounter_condition_values.csv",
        csv_record_to_objects,
    )

    def csv_record_to_objects(info):
        yield EncounterConditionValueName(
            encounter_condition_value_id=int(info[0]),
            language_id=int(info[1]),
            name=info[2],
        )

    build_generic(
        (EncounterConditionValueName,),
        "encounter_condition_value_prose.csv",
        csv_record_to_objects,
    )

    def csv_record_to_objects(info):
        yield EncounterConditionValueMap(
            encounter_id=int(info[0]), encounter_condition_value_id=int(info[1])
        )

    build_generic(
        (EncounterConditionValueMap,),
        "encounter_condition_value_map.csv",
        csv_record_to_objects,
    )


##############
#  PAL PARK  #
##############


def _build_pal_parks():
    def csv_record_to_objects(info):
        yield PalParkArea(id=int(info[0]), name=info[1])

    build_generic((PalParkArea,), "pal_park_areas.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield PalParkAreaName(
            pal_park_area_id=int(info[0]), language_id=int(info[1]), name=info[2]
        )

    build_generic((PalParkAreaName,), "pal_park_area_names.csv", csv_record_to_objects)

    def csv_record_to_objects(info):
        yield PalPark(
            pokemon_species_id=int(info[0]),
            pal_park_area_id=int(info[1]),
            base_score=int(info[2]),
            rate=int(info[3]),
        )

    build_generic((PalPark,), "pal_park.csv", csv_record_to_objects)


def build_all():
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
