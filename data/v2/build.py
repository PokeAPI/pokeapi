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
#  If you don't need all of the data just go into data/v2/build.py and
#  just call one of the build functions found in this script


# support python3
from __future__ import print_function

import csv
import os
import os.path
import re
import json
from django.db import connection
from pokemon_v2.models import *  # NOQA


# why this way? how about use `__file__`
DATA_LOCATION = 'data/v2/csv/'
DATA_LOCATION2 = os.path.join(os.path.dirname(__file__), 'csv')
GROUP_RGX = r"\[(.*?)\]\{(.*?)\}"
SUB_RGX = r"\[.*?\]\{.*?\}"

db_cursor = connection.cursor()
DB_VENDOR = connection.vendor


imageDir = os.getcwd() + '/data/v2/sprites/'
resourceImages = []
for root, dirs, files in os.walk(imageDir):
    for file in files:
        image_path = os.path.join(root.replace(imageDir, ""), file)
        image_path = image_path.replace("\\", "/") # convert Windows-style path to Unix
        resourceImages.append(image_path)


mediaDir = '/media/sprites/{0}'


def filePathOrNone(fileName):
    return mediaDir.format(fileName) if fileName in resourceImages else None


def with_iter(context, iterable=None):
    if iterable is None:
        iterable = context
    with context:
        for value in iterable:
            yield value


def load_data(fileName):
    # with_iter closes the file when it has finished
    return csv.reader(with_iter(open(DATA_LOCATION + fileName, 'rt')), delimiter=',')


def clear_table(model):
    table_name = model._meta.db_table
    model.objects.all().delete()
    print('building ' + table_name)
    # Reset DB auto increments to start at 1
    if DB_VENDOR == 'sqlite':
        db_cursor.execute("DELETE FROM sqlite_sequence WHERE name = " + "'" + table_name + "'")
    else:
        db_cursor.execute(
            "SELECT setval(pg_get_serial_sequence(" + "'" + table_name + "'" + ",'id'), 1, false);")


def build_generic(model_classes, file_name, data_to_models):
    models = {}
    for model_class in model_classes:
        clear_table(model_class)
        models[model_class] = []

    daten = load_data(file_name)
    next(daten, None)  # skip header

    for data in daten:
        for model in data_to_models(data):
            models[type(model)].append(model)

            # Limit the batch size
            if len(models[type(model)]) > 200:
                type(model).objects.bulk_create(models[type(model)])
                models[type(model)] = []

    for model_class, models_list in models.iteritems():
        model_class.objects.bulk_create(models_list)


def scrubStr(str):
    """
    The purpose of this function is to scrub the weird template mark-up out of strings
    that Veekun is using for their pokedex.
    Example:
        []{move:dragon-tail} will effect the opponents [HP]{mechanic:hp}.
    Becomes:
        dragon tail will effect the opponents HP.

    If you find this results in weird strings please take a stab at improving or re-writing.
    """
    groups = re.findall(GROUP_RGX, str)
    for group in groups:
        if group[0]:
            sub = group[0]
        else:
            sub = group[1].split(":")[1]
            sub = sub.replace("-", " ")
        str = re.sub(SUB_RGX, sub, str, 1)
    return str


##############
#  LANGUAGE  #
##############

def _build_languages():
    def data_to_language(info):
        yield Language(
            id=int(info[0]),
            iso639=info[1],
            iso3166=info[2],
            name=info[3],
            official=bool(int(info[4])),
            order=info[5],
        )
    build_generic((Language,), 'languages.csv', data_to_language)

def _build_language_names():
    def data_to_language_name(info):
        yield LanguageName(
            language_id=int(info[0]),
            local_language_id=int(info[1]),
            name=info[2]
        )
    build_generic((LanguageName,), 'language_names.csv', data_to_language_name)

def build_languages():
    _build_languages()
    _build_language_names()


############
#  REGION  #
############


def _build_regions():
    def data_to_region(info):
        yield Region(
            id=int(info[0]),
            name=info[1]
        )
    build_generic((Region,), 'regions.csv', data_to_region)

def _build_region_names():
    def data_to_region_name(info):
        yield RegionName(
            region_id = int(info[0]),
            language_id = int(info[1]),
            name = info[2]
        )
    build_generic((RegionName,), 'region_names.csv', data_to_region_name)

def build_regions():
    _build_regions()
    _build_region_names()



################
#  GENERATION  #
################

def build_generations():
    def data_to_model(info):
        yield Generation(
            id = int(info[0]),
            region_id = int(info[1]),
            name = info[2]
        )
    build_generic((Generation,), 'generations.csv', data_to_model)

    def data_to_model(info):
        yield GenerationName(
            generation_id = int(info[0]),
            language_id = int(info[1]),
            name = info[2]
        )
    build_generic((GenerationName,), 'generation_names.csv', data_to_model)



#############
#  VERSION  #
#############

def build_versions():

    def data_to_model(info):
        yield VersionGroup(
            id = int(info[0]),
            name = info[1],
            generation_id = int(info[2]),
            order = int(info[3])
        )
    build_generic((VersionGroup,), 'version_groups.csv', data_to_model)

    def data_to_model(info):
        yield VersionGroupRegion(
            version_group_id = int(info[0]),
            region_id = int(info[1]),
        )
    build_generic((VersionGroupRegion,), 'version_group_regions.csv', data_to_model)

    def data_to_model(info):
        yield Version(
            id = int(info[0]),
            version_group_id = int(info[1]),
            name = info[2]
        )
    build_generic((Version,), 'versions.csv', data_to_model)

    def data_to_model(info):
        yield VersionName(
            version_id = int(info[0]),
            language_id = int(info[1]),
            name = info[2]
        )
    build_generic((VersionName,), 'version_names.csv', data_to_model)



##################
#  DAMAGE CLASS  #
##################

def build_damage_classes():

    def data_to_model(info):
        yield MoveDamageClass(
            id = int(info[0]),
            name = info[1]
        )
    build_generic((MoveDamageClass,), 'move_damage_classes.csv', data_to_model)

    def data_to_model(info):
        yield MoveDamageClassName(
            move_damage_class_id = int(info[0]),
            language_id = int(info[1]),
            name = info[2]
        )
        yield MoveDamageClassDescription(
            move_damage_class_id = int(info[0]),
            language_id = int(info[1]),
            description = info[3]
        )
    build_generic(
        (MoveDamageClassName, MoveDamageClassDescription),
        'move_damage_class_prose.csv',
        data_to_model
    )



###########
#  STATS  #
###########

def build_stats():

    def data_to_model(info):
        yield Stat(
            id = int(info[0]),
            move_damage_class_id = int(info[1]) if info[1] != '' else None,
            name = info[2],
            is_battle_only = bool(int(info[3])),
            game_index = int(info[4]) if info[4] else 0,
        )
    build_generic((Stat,), 'stats.csv', data_to_model)

    def data_to_model(info):
        yield StatName(
            stat_id = int(info[0]),
            language_id = int(info[1]),
            name = info[2]
        )
    build_generic((StatName,), 'stat_names.csv', data_to_model)

    def data_to_model(info):
        yield PokeathlonStat(
            id = int(info[0]),
            name = info[1],
        )
    build_generic((PokeathlonStat,), 'pokeathlon_stats.csv', data_to_model)

    def data_to_model(info):
        yield PokeathlonStatName(
            pokeathlon_stat_id = int(info[0]),
            language_id = int(info[1]),
            name = info[2]
        )
    build_generic((PokeathlonStatName,), 'pokeathlon_stat_names.csv', data_to_model)



# ###############
# #  ABILITIES  #
# ###############

def build_abilities():

    def data_to_model(info):
        yield Ability(
            id = int(info[0]),
            name = info[1],
            generation_id = int(info[2]),
            is_main_series = bool(int(info[3]))
        )
    build_generic((Ability,), 'abilities.csv', data_to_model)

    def data_to_model(info):
        yield AbilityName(
            ability_id = int(info[0]),
            language_id = int(info[1]),
            name = info[2]
        )
    build_generic((AbilityName,), 'ability_names.csv', data_to_model)

    def data_to_model(info):
        yield AbilityChange(
            id = int(info[0]),
            ability_id = int(info[1]),
            version_group_id = int(info[2])
        )
    build_generic((AbilityChange,), 'ability_changelog.csv', data_to_model)

    def data_to_model(info):
        yield AbilityEffectText(
            ability_id = int(info[0]),
            language_id = int(info[1]),
            short_effect = scrubStr(info[2]),
            effect = scrubStr(info[3])
        )
    build_generic((AbilityEffectText,), 'ability_prose.csv', data_to_model)

    def data_to_model(info):
        yield AbilityChangeEffectText(
            ability_change_id = int(info[0]),
            language_id = int(info[1]),
            effect = scrubStr(info[2])
        )
    build_generic((AbilityChangeEffectText,), 'ability_changelog_prose.csv', data_to_model)

    def data_to_model(info):
        yield AbilityFlavorText(
            ability_id = int(info[0]),
            version_group_id = int(info[1]),
            language_id = int(info[2]),
            flavor_text = info[3]
        )
    build_generic((AbilityFlavorText,), 'ability_flavor_text.csv', data_to_model)



####################
#  CHARACTERISTIC  #
####################

def build_characteristics():

    def data_to_model(info):
        yield Characteristic(
            id = int(info[0]),
            stat_id = int(info[1]),
            gene_mod_5 = int(info[2])
        )
    build_generic((Characteristic,), 'characteristics.csv', data_to_model)

    def data_to_model(info):
        yield CharacteristicDescription(
            characteristic_id = int(info[0]),
            language_id = int(info[1]),
            description = info[2]
        )
    build_generic((CharacteristicDescription,), 'characteristic_text.csv', data_to_model)



###############
#  EGG GROUP  #
###############

def build_egg_groups():

    def data_to_model(info):
        yield EggGroup(
            id = int(info[0]),
            name = info[1]
        )
    build_generic((EggGroup,), 'egg_groups.csv', data_to_model)

    def data_to_model(info):
        yield EggGroupName(
            egg_group_id = int(info[0]),
            language_id = int(info[1]),
            name = info[2]
        )
    build_generic((EggGroupName,), 'egg_group_prose.csv', data_to_model)



#################
#  GROWTH RATE  #
#################

def build_growth_rates():

    def data_to_model(info):
        yield GrowthRate(
            id = int(info[0]),
            name = info[1],
            formula = info[2]
        )
    build_generic((GrowthRate,), 'growth_rates.csv', data_to_model)

    def data_to_model(info):
        yield GrowthRateDescription(
            growth_rate_id = int(info[0]),
            language_id = int(info[1]),
            description = info[2]
        )
    build_generic((GrowthRateDescription,), 'growth_rate_prose.csv', data_to_model)



# ###########
# #  ITEMS  #
# ###########

def build_items():

    def data_to_model(info):
        yield ItemPocket(
            id = int(info[0]),
            name = info[1]
        )
    build_generic((ItemPocket,), 'item_pockets.csv', data_to_model)

    def data_to_model(info):
        yield ItemPocketName(
            item_pocket_id = int(info[0]),
            language_id = int(info[1]),
            name = info[2]
        )
    build_generic((ItemPocketName,), 'item_pocket_names.csv', data_to_model)

    def data_to_model(info):
        yield ItemFlingEffect(
            id = int(info[0]),
            name = info[1]
        )
    build_generic((ItemFlingEffect,), 'item_fling_effects.csv', data_to_model)

    def data_to_model(info):
        yield ItemFlingEffectEffectText(
            item_fling_effect_id = int(info[0]),
            language_id = int(info[1]),
            effect = scrubStr(info[2])
        )
    build_generic((ItemFlingEffectEffectText,), 'item_fling_effect_prose.csv', data_to_model)

    def data_to_model(info):
        yield ItemCategory(
            id = int(info[0]),
            item_pocket_id = int(info[1]),
            name = info[2]
        )
    build_generic((ItemCategory,), 'item_categories.csv', data_to_model)

    def data_to_model(info):
        yield ItemCategoryName(
            item_category_id = int(info[0]),
            language_id = int(info[1]),
            name = info[2]
        )
    build_generic((ItemCategoryName,), 'item_category_prose.csv', data_to_model)

    def data_to_model(info):
        yield Item(
            id = int(info[0]),
            name = info[1],
            item_category_id = int(info[2]),
            cost = int(info[3]),
            fling_power = int(info[4]) if info[4] != '' else None,
            item_fling_effect_id = int(info[5]) if info[5] != '' else None
        )
    build_generic((Item,), 'items.csv', data_to_model)

    def data_to_model(info):
        if re.search(r"^data-card", info[1]):
            fileName = 'data-card.png'
        elif re.search(r"^tm[0-9]", info[1]):
            fileName = 'tm-normal.png'
        elif re.search(r"^hm[0-9]", info[1]):
            fileName = 'hm-normal.png'
        else:
            fileName = '%s.png' % info[1]

        itemSprites = 'items/{0}';
        sprites = {
            'default': filePathOrNone(itemSprites.format(fileName)),
        }
        yield ItemSprites(
            id = int(info[0]),
            item_id = int(info[0]),
            sprites = json.dumps(sprites)
        )
    build_generic((ItemSprites,), 'items.csv', data_to_model)

    def data_to_model(info):
        yield ItemName(
            item_id = int(info[0]),
            language_id = int(info[1]),
            name = info[2]
        )
    build_generic((ItemName,), 'item_names.csv', data_to_model)

    def data_to_model(info):
        yield ItemEffectText(
            item_id = int(info[0]),
            language_id = int(info[1]),
            short_effect = scrubStr(info[2]),
            effect = scrubStr(info[3])
        )
    build_generic((ItemEffectText,), 'item_prose.csv', data_to_model)

    def data_to_model(info):
        yield ItemGameIndex(
            item_id = int(info[0]),
            generation_id = int(info[1]),
            game_index = int(info[2])
        )
    build_generic((ItemGameIndex,), 'item_game_indices.csv', data_to_model)

    def data_to_model(info):
        yield ItemFlavorText(
            item_id = int(info[0]),
            version_group_id = int(info[1]),
            language_id = int(info[2]),
            flavor_text = info[3]
        )
    build_generic((ItemFlavorText,), 'item_flavor_text.csv', data_to_model)

    def data_to_model(info):
        yield ItemAttribute(
            id = int(info[0]),
            name = info[1]
        )
    build_generic((ItemAttribute,), 'item_flags.csv', data_to_model)

    def data_to_model(info):
        yield ItemAttributeName(
            item_attribute_id = int(info[0]),
            language_id = int(info[1]),
            name = info[2]
        )
        yield ItemAttributeDescription(
            item_attribute_id = int(info[0]),
            language_id = int(info[1]),
            description = info[3]
        )
    build_generic(
        (ItemAttributeName, ItemAttributeDescription),
        'item_flag_prose.csv',
        data_to_model
    )

    def data_to_model(info):
        yield ItemAttributeMap(
            item_id = int(info[0]),
            item_attribute_id = int(info[1])
        )
    build_generic((ItemAttributeMap,), 'item_flag_map.csv', data_to_model)



###########
#  TYPES  #
###########

def build_types():

    def data_to_model(info):
        yield Type(
            id = int(info[0]),
            name = info[1],
            generation_id = int(info[2]),
            move_damage_class_id = int(info[3]) if info[3] != '' else None
        )
    build_generic((Type,), 'types.csv', data_to_model)

    def data_to_model(info):
        yield TypeName(
            type_id = int(info[0]),
            language_id = int(info[1]),
            name = info[2]
        )
    build_generic((TypeName,), 'type_names.csv', data_to_model)

    def data_to_model(info):
        yield TypeGameIndex(
            type_id = int(info[0]),
            generation_id = int(info[1]),
            game_index = int(info[2])
        )
    build_generic((TypeGameIndex,), 'type_game_indices.csv', data_to_model)

    def data_to_model(info):
        yield TypeEfficacy(
            damage_type_id = int(info[0]),
            target_type_id = int(info[1]),
            damage_factor = int(info[2])
        )
    build_generic((TypeEfficacy,), 'type_efficacy.csv', data_to_model)



#############
#  CONTEST  #
#############

def build_contests():

    def data_to_model(info):
        yield ContestType(
            id = int(info[0]),
            name = info[1]
        )
    build_generic((ContestType,), 'contest_types.csv', data_to_model)

    def data_to_model(info):
        yield ContestTypeName(
            contest_type_id = int(info[0]),
            language_id = int(info[1]),
            name = info[2],
            flavor = info[3],
            color = info[4]
        )
    build_generic((ContestTypeName,), 'contest_type_names.csv', data_to_model)

    def data_to_model(info):
        yield ContestEffect(
            id = int(info[0]),
            appeal = int(info[1]),
            jam = int(info[2])
        )
    build_generic((ContestEffect,), 'contest_effects.csv', data_to_model)

    def data_to_model(info):
        yield ContestEffectEffectText(
            contest_effect_id = int(info[0]),
            language_id = int(info[1]),
            effect = info[3]
        )
        yield ContestEffectFlavorText(
            contest_effect_id = int(info[0]),
            language_id = int(info[1]),
            flavor_text = info[2]
        )
    build_generic(
        (ContestEffectEffectText, ContestEffectFlavorText),
        'contest_effect_prose.csv',
        data_to_model
    )

    def data_to_model(info):
        yield SuperContestEffect(
            id = int(info[0]),
            appeal = int(info[1])
        )
    build_generic((SuperContestEffect,), 'super_contest_effects.csv', data_to_model)

    def data_to_model(info):
        yield SuperContestEffectFlavorText(
            super_contest_effect_id = int(info[0]),
            language_id = int(info[1]),
            flavor_text = info[2]
        )
    build_generic((SuperContestEffectFlavorText,), 'super_contest_effect_prose.csv', data_to_model)



###########
#  MOVES  #
###########

def build_moves():

    def data_to_model(info):
        yield MoveEffect(
            id = int(info[0])
        )
    build_generic((MoveEffect,), 'move_effects.csv', data_to_model)

    def data_to_model(info):
        yield MoveEffectEffectText(
            move_effect_id = int(info[0]),
            language_id = int(info[1]),
            short_effect = scrubStr(info[2]),
            effect = scrubStr(info[3])
        )
    build_generic((MoveEffectEffectText,), 'move_effect_prose.csv', data_to_model)

    def data_to_model(info):
        yield MoveEffectChange(
            id = int(info[0]),
            move_effect_id = int(info[1]),
            version_group_id = int(info[2])
        )
    build_generic((MoveEffectChange,), 'move_effect_changelog.csv', data_to_model)

    def data_to_model(info):
        yield MoveEffectChangeEffectText(
            move_effect_change_id = int(info[0]),
            language_id = int(info[1]),
            effect = scrubStr(info[2])
        )
    build_generic((MoveEffectChangeEffectText,), 'move_effect_changelog_prose.csv', data_to_model)

    def data_to_model(info):
        yield MoveLearnMethod(
            id = int(info[0]),
            name = info[1]
        )
    build_generic((MoveLearnMethod,), 'pokemon_move_methods.csv', data_to_model)

    def data_to_model(info):
        yield VersionGroupMoveLearnMethod(
            version_group_id = int(info[0]),
            move_learn_method_id = int(info[1]),
        )
    build_generic(
        (VersionGroupMoveLearnMethod,), 'version_group_pokemon_move_methods.csv', data_to_model
    )

    def data_to_model(info):
        yield MoveLearnMethodName(
            move_learn_method_id = int(info[0]),
            language_id = int(info[1]),
            name = info[2]
        )
        yield MoveLearnMethodDescription(
            move_learn_method_id = int(info[0]),
            language_id = int(info[1]),
            description = info[3]
        )
    build_generic(
        (MoveLearnMethodName, MoveLearnMethodDescription),
        'pokemon_move_method_prose.csv',
        data_to_model
    )

    def data_to_model(info):
        yield MoveTarget(
            id = int(info[0]),
            name = info[1]
        )
    build_generic((MoveTarget,), 'move_targets.csv', data_to_model)

    def data_to_model(info):
        yield MoveTargetName(
            move_target_id = int(info[0]),
            language_id = int(info[1]),
            name = info[2]
        )
        yield MoveTargetDescription(
            move_target_id = int(info[0]),
            language_id = int(info[1]),
            description = info[3]
        )
    build_generic((MoveTargetName, MoveTargetDescription), 'move_target_prose.csv', data_to_model)

    def data_to_model(info):
        yield Move(
            id = int(info[0]),
            name = info[1],
            generation_id = int(info[2]),
            type_id = int(info[3]),
            power = int(info[4]) if info[4] != '' else None,
            pp = int(info[5]) if info[5] != '' else None,
            accuracy = int(info[6]) if info[6] != '' else None,
            priority = int(info[7]) if info[7] != '' else None,
            move_target_id = int(info[8]),
            move_damage_class_id = int(info[9]),
            move_effect_id = int(info[10]),
            move_effect_chance = int(info[11]) if info[11] != '' else None,
            contest_type_id = int(info[12]) if info[12] != '' else None,
            contest_effect_id = int(info[13]) if info[13] != '' else None,
            super_contest_effect_id = int(info[14]) if info[14] != '' else None
        )
    build_generic((Move,), 'moves.csv', data_to_model)

    def data_to_model(info):
        yield MoveName(
            move_id = int(info[0]),
            language_id = int(info[1]),
            name = info[2]
        )
    build_generic((MoveName,), 'move_names.csv', data_to_model)

    def data_to_model(info):
        yield MoveFlavorText(
            move_id = int(info[0]),
            version_group_id = int(info[1]),
            language_id = int(info[2]),
            flavor_text = info[3]
        )
    build_generic((MoveFlavorText,), 'move_flavor_text.csv', data_to_model)

    def data_to_model(info):
        _move_effect = None
        try:
            _move_effect = MoveEffect.objects.get(pk = int(info[6])) if info[6] != '' else None
        except:
            pass

        yield MoveChange(
            move_id = int(info[0]),
            version_group_id = int(info[1]),
            type_id = int(info[2]) if info[2] != '' else None,
            power = int(info[3]) if info[3] != '' else None,
            pp = int(info[4]) if info[4] != '' else None,
            accuracy = int(info[5]) if info[5] != '' else None,
            move_effect_id =  _move_effect.pk if _move_effect else None,
            move_effect_chance = int(info[7]) if info[7] != '' else None
        )
    build_generic((MoveChange,), 'move_changelog.csv', data_to_model)

    def data_to_model(info):
        yield MoveBattleStyle(
            id = int(info[0]),
            name = info[1]
        )
    build_generic((MoveBattleStyle,), 'move_battle_styles.csv', data_to_model)

    def data_to_model(info):
        yield MoveBattleStyleName(
            move_battle_style_id = int(info[0]),
            language_id = int(info[1]),
            name = info[2]
        )
    build_generic((MoveBattleStyleName,), 'move_battle_style_prose.csv', data_to_model)

    def data_to_model(info):
        yield MoveAttribute(
            id = int(info[0]),
            name = info[1]
        )
    build_generic((MoveAttribute,), 'move_flags.csv', data_to_model)

    def data_to_model(info):
        yield MoveAttributeMap(
            move_id = int(info[0]),
            move_attribute_id = int(info[1]),
        )
    build_generic((MoveAttributeMap,), 'move_flag_map.csv', data_to_model)

    def data_to_model(info):
        yield MoveAttributeName(
            move_attribute_id = int(info[0]),
            language_id = int(info[1]),
            name = info[2]
        )
        yield MoveAttributeDescription(
            move_attribute_id = int(info[0]),
            language_id = int(info[1]),
            description = scrubStr(info[3])
        )
    build_generic(
        (MoveAttributeName, MoveAttributeDescription), 'move_flag_prose.csv', data_to_model
    )

    def data_to_model(info):
        yield MoveMetaAilment(
            id = int(info[0]),
            name = info[1]
        )
    build_generic((MoveMetaAilment,), 'move_meta_ailments.csv', data_to_model)

    def data_to_model(info):
        yield MoveMetaAilmentName(
            move_meta_ailment_id = int(info[0]),
            language_id = int(info[1]),
            name = info[2]
        )
    build_generic((MoveMetaAilmentName,), 'move_meta_ailment_names.csv', data_to_model)

    def data_to_model(info):
        yield MoveMetaCategory(
            id = int(info[0]),
            name = info[1]
        )
    build_generic((MoveMetaCategory,), 'move_meta_categories.csv', data_to_model)

    def data_to_model(info):
        yield MoveMetaCategoryDescription(
            move_meta_category_id =  int(info[0]),
            language_id =  int(info[1]),
            description = info[2]
        )
    build_generic((MoveMetaCategoryDescription,), 'move_meta_category_prose.csv', data_to_model)

    def data_to_model(info):
        yield MoveMeta(
            move_id = int(info[0]),
            move_meta_category_id = int(info[1]),
            move_meta_ailment_id = int(info[2]),
            min_hits = int(info[3]) if info[3] != '' else None,
            max_hits = int(info[4]) if info[4] != '' else None,
            min_turns = int(info[5]) if info[5] != '' else None,
            max_turns = int(info[6]) if info[6] != '' else None,
            drain = int(info[7]) if info[7] != '' else None,
            healing = int(info[8]) if info[8] != '' else None,
            crit_rate = int(info[9]) if info[9] != '' else None,
            ailment_chance = int(info[10]) if info[10] != '' else None,
            flinch_chance = int(info[11]) if info[11] != '' else None,
            stat_chance = int(info[12]) if info[12] != '' else None
        )
    build_generic((MoveMeta,), 'move_meta.csv', data_to_model)

    def data_to_model(info):
        yield MoveMetaStatChange(
            move_id = int(info[0]),
            stat_id = int(info[1]),
            change = int(info[2])
        )
    build_generic((MoveMetaStatChange,), 'move_meta_stat_changes.csv', data_to_model)

    def data_to_model(info):
        yield ContestCombo(
            first_move_id = int(info[0]),
            second_move_id = int(info[1])
        )
    build_generic((ContestCombo,), 'contest_combos.csv', data_to_model)

    def data_to_model(info):
        yield SuperContestCombo(
            first_move_id = int(info[0]),
            second_move_id = int(info[1])
        )
    build_generic((SuperContestCombo,), 'super_contest_combos.csv', data_to_model)



#############
#  BERRIES  #
#############

def build_berries():
    clear_table(BerryFirmness)
    data = load_data('berry_firmness.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = BerryFirmness (
                id = int(info[0]),
                name = info[1]
            )
            model.save()


    clear_table(BerryFirmnessName)
    data = load_data('berry_firmness_names.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = BerryFirmnessName (
                berry_firmness = BerryFirmness.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                name = info[2]
            )
            model.save()


    clear_table(Berry)
    data = load_data('berries.csv')

    for index, info in enumerate(data):
        if index > 0:
            item = Item.objects.get(pk = int(info[1]))
            model = Berry (
                id = int(info[0]),
                item = item,
                name = item.name[:item.name.index('-')],
                berry_firmness = BerryFirmness.objects.get(pk = int(info[2])),
                natural_gift_power = int(info[3]),
                natural_gift_type = Type.objects.get(pk = int(info[4])),
                size = int(info[5]),
                max_harvest = int(info[6]),
                growth_time = int(info[7]),
                soil_dryness = int(info[8]),
                smoothness = int(info[9])
            )
            model.save()


    clear_table(BerryFlavor)
    data = load_data('contest_types.csv') #this is not an error

    for index, info in enumerate(data):
        if index > 0:
            # get the english name for this contest type
            contest_type_name = ContestTypeName.objects.get(contest_type_id=int(info[0]), language_id=9)

            model = BerryFlavor (

                id = int(info[0]),
                name = contest_type_name.flavor.lower(),
                contest_type = ContestType.objects.get(pk = int(info[0]))
            )
            model.save()


    clear_table(BerryFlavorName)
    data = load_data('contest_type_names.csv') #this is not an error

    for index, info in enumerate(data):
        if index > 0:

            model = BerryFlavorName (
                berry_flavor = BerryFlavor.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                name = info[3]
            )
            model.save()


    clear_table(BerryFlavorMap)
    data = load_data('berry_flavors.csv') #this is not an error

    for index, info in enumerate(data):
        if index > 0:

            model = BerryFlavorMap (
                berry = Berry.objects.get(pk = int(info[0])),
                berry_flavor = BerryFlavor.objects.get(pk = int(info[1])),
                potency = int(info[2])
            )
            model.save()


############
#  NATURE  #
############

def build_natures():
    clear_table(Nature)
    data = load_data('natures.csv')

    for index, info in enumerate(data):
        if index > 0:

            decreased_stat = None
            increased_stat = None
            hates_flavor = None
            likes_flavor = None

            if (info[2] != info[3]):
                decreased_stat = Stat.objects.get(pk = int(info[2]))
                increased_stat = Stat.objects.get(pk = int(info[3]))

            if (info[4] != info[5]):
                hates_flavor = BerryFlavor.objects.get(pk = int(info[4]))
                likes_flavor = BerryFlavor.objects.get(pk = int(info[5]))

            nature = Nature (
                id = int(info[0]),
                name = info[1],
                decreased_stat = decreased_stat,
                increased_stat = increased_stat,
                hates_flavor = hates_flavor,
                likes_flavor = likes_flavor,
                game_index = info[6]
              )
            nature.save()


    clear_table(NatureName)
    data = load_data('nature_names.csv')

    for index, info in enumerate(data):
        if index > 0:

            natureName = NatureName (
                nature = Nature.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                name = info[2]
              )
            natureName.save()


    clear_table(NaturePokeathlonStat)
    data = load_data('nature_pokeathlon_stats.csv')

    for index, info in enumerate(data):
        if index > 0:

            naturePokeathlonStat = NaturePokeathlonStat (
                nature = Nature.objects.get(pk = int(info[0])),
                pokeathlon_stat = PokeathlonStat.objects.get(pk = int(info[1])),
                max_change = info[2]
              )
            naturePokeathlonStat.save()


    clear_table(NatureBattleStylePreference)
    data = load_data('nature_battle_style_preferences.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = NatureBattleStylePreference (
                nature = Nature.objects.get(pk = int(info[0])),
                move_battle_style = MoveBattleStyle.objects.get(pk = int(info[1])),
                low_hp_preference = info[2],
                high_hp_preference = info[3]
              )
            model.save()



###########
# GENDER  #
###########

def build_genders():
    clear_table(Gender)
    data = load_data('genders.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = Gender (
                id = int(info[0]),
                name = info[1]
              )
            model.save()



################
#  EXPERIENCE  #
################

def build_experiences():
    clear_table(Experience)
    data = load_data('experience.csv')

    for index, info in enumerate(data):
      if index > 0:

        model = Experience (
            growth_rate = GrowthRate.objects.get(pk = int(info[0])),
            level = int(info[1]),
            experience = int(info[2])
          )
        model.save()



##############
#  MACHINES  #
##############

def build_machines():
    clear_table(Machine)
    data = load_data('machines.csv')

    for index, info in enumerate(data):
      if index > 0:

        model = Machine (
            machine_number = int(info[0]),
            version_group = VersionGroup.objects.get(pk = int(info[1])),
            item = Item.objects.get(pk = int(info[2])),
            move = Move.objects.get(pk = int(info[3])),
          )
        model.save()



###############
#  EVOLUTION  #
###############

def build_evolutions():
    clear_table(EvolutionChain)
    data = load_data('evolution_chains.csv')

    for index, info in enumerate(data):
      if index > 0:

        model = EvolutionChain (
            id = int(info[0]),
            baby_trigger_item = Item.objects.get(pk = int(info[1])) if info[1] != '' else None,
          )
        model.save()


    clear_table(EvolutionTrigger)
    data = load_data('evolution_triggers.csv')

    for index, info in enumerate(data):
      if index > 0:

        model = EvolutionTrigger (
            id = int(info[0]),
            name = info[1]
          )
        model.save()


    clear_table(EvolutionTriggerName)
    data = load_data('evolution_trigger_prose.csv')

    for index, info in enumerate(data):
      if index > 0:

        model = EvolutionTriggerName (
            evolution_trigger = EvolutionTrigger.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            name = info[2]
          )
        model.save()



#############
#  POKEDEX  #
#############

def build_pokedexes():
    clear_table(Pokedex)
    data = load_data('pokedexes.csv')

    for index, info in enumerate(data):
      if index > 0:

        model = Pokedex (
            id = int(info[0]),
            region = Region.objects.get(pk = int(info[1])) if info[1] != '' else None,
            name = info[2],
            is_main_series = bool(int(info[3]))
          )
        model.save()


    clear_table(PokedexName)
    clear_table(PokedexDescription)
    data = load_data('pokedex_prose.csv')

    for index, info in enumerate(data):
      if index > 0:

        name_model = PokedexName (
            pokedex = Pokedex.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            name = info[2],
          )
        name_model.save()

        description_model = PokedexDescription (
            pokedex = Pokedex.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            description = info[3]
          )
        description_model.save()


    clear_table(PokedexVersionGroup)
    data = load_data('pokedex_version_groups.csv')

    for index, info in enumerate(data):
      if index > 0:

        model = PokedexVersionGroup (
            pokedex = Pokedex.objects.get(pk = int(info[0])),
            version_group = VersionGroup.objects.get(pk = int(info[1]))
          )
        model.save()


##############
#  LOCATION  #
##############

def build_locations():
    clear_table(Location)
    data = load_data('locations.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = Location (
                id = int(info[0]),
                region = Region.objects.get(pk = int(info[1])) if info[1] != '' else None,
                name = info[2]
              )
            model.save()


    clear_table(LocationName)
    data = load_data('location_names.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = LocationName (
                location = Location.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                name = info[2]
              )
            model.save()


    clear_table(LocationGameIndex)
    data = load_data('location_game_indices.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = LocationGameIndex (
                location = Location.objects.get(pk = int(info[0])),
                generation = Generation.objects.get(pk = int(info[1])),
                game_index = int(info[2])
              )
            model.save()


    clear_table(LocationArea)
    data = load_data('location_areas.csv')

    for index, info in enumerate(data):
        if index > 0:

            location = Location.objects.get(pk = int(info[1]))

            model = LocationArea (
              id = int(info[0]),
              location = location,
              game_index = int(info[2]),
              name = '{}-{}'.format(location.name, info[3]) if info[3] else '{}-{}'.format(location.name, 'area')
            )
            model.save()


    clear_table(LocationAreaName)
    data = load_data('location_area_prose.csv')

    for index, info in enumerate(data):
      if index > 0:

        model = LocationAreaName (
            location_area = LocationArea.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            name = info[2]
          )
        model.save()



#############
#  POKEMON  #
#############

def build_pokemons():

    clear_table(PokemonColor)
    data = load_data('pokemon_colors.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = PokemonColor (
                id = int(info[0]),
                name = info[1]
            )
            model.save()


    clear_table(PokemonColorName)
    data = load_data('pokemon_color_names.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = PokemonColorName (
                pokemon_color = PokemonColor.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                name = info[2]
            )
            model.save()


    clear_table(PokemonShape)
    data = load_data('pokemon_shapes.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = PokemonShape (
                id = int(info[0]),
                name = info[1]
            )
            model.save()


    clear_table(PokemonShapeName)
    data = load_data('pokemon_shape_prose.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = PokemonShapeName (
                pokemon_shape = PokemonShape.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                name = info[2],
                awesome_name = info[3]
            )
            model.save()


    clear_table(PokemonHabitat)
    data = load_data('pokemon_habitats.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = PokemonHabitat (
                id = int(info[0]),
                name = info[1]
            )
            model.save()


    clear_table(PokemonSpecies)
    data = load_data('pokemon_species.csv')
    models = []
    for index, info in enumerate(data):
        if index > 0:
            models.append(PokemonSpecies (
                id = int(info[0]),
                name = info[1],
                generation_id = int(info[2]),
                evolves_from_species = None,
                evolution_chain_id = int(info[4]),
                pokemon_color_id = int(info[5]),
                pokemon_shape_id = int(info[6]),
                pokemon_habitat_id = int(info[7]) if info[7] != '' else None,
                gender_rate = int(info[8]),
                capture_rate = int(info[9]),
                base_happiness = int(info[10]),
                is_baby = bool(int(info[11])),
                hatch_counter = int(info[12]),
                has_gender_differences = bool(int(info[13])),
                growth_rate_id = int(info[14]),
                forms_switchable = bool(int(info[15])),
                order = int(info[16])
            ))
            if len(models) > 200:
                PokemonSpecies.objects.bulk_create(models)
                models = []

    PokemonSpecies.objects.bulk_create(models)

    data = load_data('pokemon_species.csv')

    for index, info in enumerate(data):
        if index > 0:

            evolves = PokemonSpecies.objects.get(pk = int(info[3])) if info[3] != '' else None

            if evolves:
                species = PokemonSpecies.objects.get(pk = int(info[0]))
                species.evolves_from_species = evolves
                species.save()


    clear_table(PokemonSpeciesName)
    data = load_data('pokemon_species_names.csv')
    models = []
    for index, info in enumerate(data):
        if index > 0:
            models.append(PokemonSpeciesName (
                pokemon_species_id = int(info[0]),
                language_id = int(info[1]),
                name = info[2],
                genus = info[3]
            ))
            if len(models) > 200:
                PokemonSpeciesName.objects.bulk_create(models)
                models = []

    PokemonSpeciesName.objects.bulk_create(models)


    clear_table(PokemonSpeciesDescription)
    data = load_data('pokemon_species_prose.csv')
    models = []
    for index, info in enumerate(data):
        if index > 0:
            models.append(PokemonSpeciesDescription (
                pokemon_species_id = int(info[0]),
                language_id = int(info[1]),
                description = scrubStr(info[2])
            ))
            if len(models) > 200:
                PokemonSpeciesDescription.objects.bulk_create(models)
                models = []

    PokemonSpeciesDescription.objects.bulk_create(models)


    clear_table(PokemonSpeciesFlavorText)
    data = load_data('pokemon_species_flavor_text.csv')
    models = []
    for index, info in enumerate(data):
        if index > 0:
            models.append(PokemonSpeciesFlavorText (
                pokemon_species_id = int(info[0]),
                version_id = int(info[1]),
                language_id = int(info[2]),
                flavor_text = info[3]
            ))
            if len(models) > 200:
                PokemonSpeciesFlavorText.objects.bulk_create(models)
                models = []

    PokemonSpeciesFlavorText.objects.bulk_create(models)


    clear_table(Pokemon)
    clear_table(PokemonSprites)
    data = load_data('pokemon.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = Pokemon (
                id = int(info[0]),
                name = info[1],
                pokemon_species = PokemonSpecies.objects.get(pk = int(info[2])),
                height = int(info[3]),
                weight = int(info[4]),
                base_experience = int(info[5]),
                order = int(info[6]),
                is_default = bool(int(info[7]))
            )
            model.save()

            fileName = '%s.png' % info[0]
            pokeSprites = 'pokemon/{0}';

            sprites = {
                'front_default'      : filePathOrNone(pokeSprites.format(fileName)),
                'front_female'       : filePathOrNone(pokeSprites.format('female/'+fileName)),
                'front_shiny'        : filePathOrNone(pokeSprites.format('shiny/'+fileName)),
                'front_shiny_female' : filePathOrNone(pokeSprites.format('shiny/female/'+fileName)),
                'back_default'       : filePathOrNone(pokeSprites.format('back/'+fileName)),
                'back_female'        : filePathOrNone(pokeSprites.format('back/female/'+fileName)),
                'back_shiny'         : filePathOrNone(pokeSprites.format('back/shiny/'+fileName)),
                'back_shiny_female'  : filePathOrNone(pokeSprites.format('back/shiny/female/'+fileName)),
            }

            imageModel = PokemonSprites (
                id = index,
                pokemon = Pokemon.objects.get(pk=int(info[0])),
                sprites = json.dumps(sprites)
            )
            imageModel.save()

    clear_table(PokemonAbility)
    data = load_data('pokemon_abilities.csv')
    models = []
    for index, info in enumerate(data):
        if index > 0:
            models.append(PokemonAbility (
                pokemon_id = int(info[0]),
                ability_id = int(info[1]),
                is_hidden = bool(int(info[2])),
                slot = int(info[3])
            ))
            if len(models) > 200:
                PokemonAbility.objects.bulk_create(models)
                models = []

    PokemonAbility.objects.bulk_create(models)


    clear_table(PokemonDexNumber)
    data = load_data('pokemon_dex_numbers.csv')
    models = []
    for index, info in enumerate(data):
        if index > 0:
            models.append(PokemonDexNumber (
                pokemon_species_id = int(info[0]),
                pokedex_id = int(info[1]),
                pokedex_number = int(info[2])
            ))
            if len(models) > 200:
                PokemonDexNumber.objects.bulk_create(models)
                models = []

    PokemonDexNumber.objects.bulk_create(models)


    clear_table(PokemonEggGroup)
    data = load_data('pokemon_egg_groups.csv')
    models = []
    for index, info in enumerate(data):
        if index > 0:
            models.append(PokemonEggGroup (
                pokemon_species_id = int(info[0]),
                egg_group_id = int(info[1])
            ))
            if len(models) > 200:
                PokemonEggGroup.objects.bulk_create(models)
                models = []

    PokemonEggGroup.objects.bulk_create(models)


    clear_table(PokemonEvolution)
    data = load_data('pokemon_evolution.csv')
    models = []
    for index, info in enumerate(data):
        if index > 0:
            models.append(PokemonEvolution (
                id = int(info[0]),
                evolved_species_id = int(info[1]),
                evolution_trigger_id = int(info[2]),
                evolution_item_id = int(info[3]) if info[3] != '' else None,
                min_level = int(info[4]) if info[4] != '' else None,
                gender_id = int(info[5]) if info[5] != '' else None,
                location_id = int(info[6]) if info[6] != '' else None,
                held_item_id = int(info[7]) if info[7] != '' else None,
                time_of_day = info[8],
                known_move_id = int(info[9]) if info[9] != '' else None,
                known_move_type_id = int(info[10]) if info[10] != '' else None,
                min_happiness = int(info[11]) if info[11] != '' else None,
                min_beauty = int(info[12]) if info[12] != '' else None,
                min_affection = int(info[13]) if info[13] != '' else None,
                relative_physical_stats = int(info[14]) if info[14] != '' else None,
                party_species_id = int(info[15]) if info[15] != '' else None,
                party_type_id = int(info[16]) if info[16] != '' else None,
                trade_species_id = int(info[17]) if info[17] != '' else None,
                needs_overworld_rain = bool(int(info[18])),
                turn_upside_down = bool(int(info[19]))
            ))
            if len(models) > 200:
                PokemonEvolution.objects.bulk_create(models)
                models = []

    PokemonEvolution.objects.bulk_create(models)


    clear_table(PokemonForm)
    clear_table(PokemonFormSprites)
    data = load_data('pokemon_forms.csv')
    models = []
    spritesModels = []
    for index, info in enumerate(data):
        if index > 0:

            pokemon = Pokemon.objects.get(pk = int(info[3]))
            models.append(PokemonForm (
                id = int(info[0]),
                name = info[1],
                form_name = info[2],
                pokemon_id = int(info[3]),
                version_group_id = int(info[4]),
                is_default = bool(int(info[5])),
                is_battle_only = bool(int(info[6])),
                is_mega = bool(int(info[7])),
                form_order = int(info[8]),
                order = int(info[9])
            ))
            if len(models) > 200:
                PokemonForm.objects.bulk_create(models)
                models = []

            if info[2]:
                if re.search(r"^mega", info[2]):
                    fileName = '%s.png' % info[3]
                else:
                    fileName = '%s-%s.png' % (getattr(pokemon, 'pokemon_species_id'), info[2])
            else:
                fileName = '%s.png' % getattr(pokemon, 'pokemon_species_id')

            pokeSprites = 'pokemon/{0}'

            sprites = {
                'front_default'      : filePathOrNone(pokeSprites.format(fileName)),
                'front_shiny'        : filePathOrNone(pokeSprites.format('shiny/'+fileName)),
                'back_default'       : filePathOrNone(pokeSprites.format('back/'+fileName)),
                'back_shiny'         : filePathOrNone(pokeSprites.format('back/shiny/'+fileName)),
            }
            spritesModels.append(PokemonFormSprites(
                id = index,
                pokemon_form_id = int(info[0]),
                sprites = json.dumps(sprites)
            ))
            if len(spritesModels) > 200:
                PokemonFormSprites.objects.bulk_create(spritesModels)
                spritesModels = []

    PokemonForm.objects.bulk_create(models)
    PokemonFormSprites.objects.bulk_create(spritesModels)


    clear_table(PokemonFormName)
    data = load_data('pokemon_form_names.csv')
    models = []
    for index, info in enumerate(data):
        if index > 0:
            models.append(PokemonFormName (
                pokemon_form = PokemonForm.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                name = info[2],
                pokemon_name = info[3]
            ))
            if len(models) > 200:
                PokemonFormName.objects.bulk_create(models)
                models = []

    PokemonFormName.objects.bulk_create(models)


    clear_table(PokemonFormGeneration)
    data = load_data('pokemon_form_generations.csv')
    models = []
    for index, info in enumerate(data):
        if index > 0:
            models.append(PokemonFormGeneration (
                pokemon_form_id = int(info[0]),
                generation_id = int(info[1]),
                game_index = int(info[2])
            ))
            if len(models) > 200:
                PokemonFormGeneration.objects.bulk_create(models)
                models = []

    PokemonFormGeneration.objects.bulk_create(models)


    clear_table(PokemonGameIndex)
    data = load_data('pokemon_game_indices.csv')
    models = []
    for index, info in enumerate(data):
        if index > 0:
            models.append(PokemonGameIndex (
                pokemon_id = int(info[0]),
                version_id = int(info[1]),
                game_index = int(info[2])
            ))
            if len(models) > 200:
                PokemonGameIndex.objects.bulk_create(models)
                models = []

    PokemonGameIndex.objects.bulk_create(models)


    clear_table(PokemonHabitatName)
    data = load_data('pokemon_habitat_names.csv')
    models = []
    for index, info in enumerate(data):
        if index > 0:
            models.append(PokemonHabitatName (
                pokemon_habitat_id = int(info[0]),
                language_id = int(info[1]),
                name = info[2]
            ))
            if len(models) > 200:
                PokemonHabitatName.objects.bulk_create(models)
                models = []

    PokemonHabitatName.objects.bulk_create(models)


    clear_table(PokemonItem)
    data = load_data('pokemon_items.csv')
    models = []
    for index, info in enumerate(data):
        if index > 0:
            models.append(PokemonItem (
                pokemon_id = int(info[0]),
                version_id = int(info[1]),
                item_id = int(info[2]),
                rarity = int(info[3])
            ))
            if len(models) > 200:
                PokemonItem.objects.bulk_create(models)
                models = []

    PokemonItem.objects.bulk_create(models)


    clear_table(PokemonMove)
    data = load_data('pokemon_moves.csv')
    models = []

    for index, info in enumerate(data):
        if index > 0:

            models.append(
                PokemonMove(
                    pokemon_id = int(info[0]),
                    version_group_id = int(info[1]),
                    move_id = int(info[2]),
                    move_learn_method_id = int(info[3]),
                    level = int(info[4]),
                    order = int(info[5]) if info[5] != '' else None,
                )
            )

            if len(models) > 200:
                PokemonMove.objects.bulk_create(models)
                models = []

    PokemonMove.objects.bulk_create(models)


    clear_table(PokemonStat)
    data = load_data('pokemon_stats.csv')
    models = []
    for index, info in enumerate(data):
        if index > 0:
            models.append(PokemonStat (
                pokemon_id = int(info[0]),
                stat_id = int(info[1]),
                base_stat = int(info[2]),
                effort = int(info[3])
            ))
            if len(models) > 200:
                PokemonStat.objects.bulk_create(models)
                models = []

    PokemonStat.objects.bulk_create(models)


    clear_table(PokemonType)
    data = load_data('pokemon_types.csv')
    models = []
    for index, info in enumerate(data):
        if index > 0:
            models.append(PokemonType (
                pokemon_id = int(info[0]),
                type_id = int(info[1]),
                slot = int(info[2])
            ))
            if len(models) > 200:
                PokemonType.objects.bulk_create(models)
                models = []

    PokemonType.objects.bulk_create(models)



###############
#  ENCOUNTER  #
###############

def build_encounters():
    clear_table(EncounterMethod)
    data = load_data('encounter_methods.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = EncounterMethod (
                id = int(info[0]),
                name = info[1],
                order = int(info[2])
            )
            model.save()


    # LocationAreaEncounterRate/EncounterMethod associations
    """
    I tried handling this the same way Berry/Natures are handled
    but for some odd reason it resulted in a ton of db table issues.
    It was easy enough to move LocationAreaEncounterRates below
    Encounter population and for some reason things works now.
    """
    clear_table(LocationAreaEncounterRate)
    data = load_data('location_area_encounter_rates.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = LocationAreaEncounterRate (
                location_area = LocationArea.objects.get(pk = int(info[0])),
                encounter_method = EncounterMethod.objects.get(pk=info[1]),
                version = Version.objects.get(pk = int(info[2])),
                rate = int(info[3])
            )
            model.save()


    clear_table(EncounterMethodName)
    data = load_data('encounter_method_prose.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = EncounterMethodName (
                encounter_method = EncounterMethod.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                name = info[2]
            )
            model.save()


    clear_table(EncounterSlot)
    data = load_data('encounter_slots.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = EncounterSlot (
                id = int(info[0]),
                version_group = VersionGroup.objects.get(pk = int(info[1])),
                encounter_method = EncounterMethod.objects.get(pk = int(info[2])),
                slot = int(info[3]) if info[3] != '' else None,
                rarity = int(info[4])
            )
            model.save()


    clear_table(EncounterCondition)
    data = load_data('encounter_conditions.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = EncounterCondition (
                id = int(info[0]),
                name = info[1]
            )
            model.save()


    clear_table(EncounterConditionName)
    data = load_data('encounter_condition_prose.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = EncounterConditionName (
                encounter_condition = EncounterCondition.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                name = info[2]
            )
            model.save()


    clear_table(Encounter)
    data = load_data('encounters.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = Encounter (
                id = int(info[0]),
                version = Version.objects.get(pk = int(info[1])),
                location_area = LocationArea.objects.get(pk = int(info[2])),
                encounter_slot = EncounterSlot.objects.get(pk = int(info[3])),
                pokemon = Pokemon.objects.get(pk = int(info[4])),
                min_level = int(info[5]),
                max_level = int(info[6])
            )
            model.save()


    clear_table(EncounterConditionValue)
    data = load_data('encounter_condition_values.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = EncounterConditionValue (
                id = int(info[0]),
                encounter_condition = EncounterCondition.objects.get(pk = int(info[1])),
                name = info[2],
                is_default = bool(int(info[3]))
            )
            model.save()


    clear_table(EncounterConditionValueName)
    data = load_data('encounter_condition_value_prose.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = EncounterConditionValueName (
                encounter_condition_value = EncounterConditionValue.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                name = info[2],
            )
            model.save()


    clear_table(EncounterConditionValueMap)
    data = load_data('encounter_condition_value_map.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = EncounterConditionValueMap (
                encounter = Encounter.objects.get(pk = int(info[0])),
                encounter_condition_value = EncounterConditionValue.objects.get(pk = int(info[1]))
            )
            model.save()



##############
#  PAL PARK  #
##############

def build_pal_parks():
    clear_table(PalParkArea)
    data = load_data('pal_park_areas.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = PalParkArea (
                id = int(info[0]),
                name = info[1]
            )
            model.save()


    clear_table(PalParkAreaName)
    data = load_data('pal_park_area_names.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = PalParkAreaName (
                pal_park_area = PalParkArea.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                name = info[2]
            )
            model.save()


    clear_table(PalPark)
    data = load_data('pal_park.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = PalPark (
                pokemon_species = PokemonSpecies.objects.get(pk = int(info[0])),
                pal_park_area = PalParkArea.objects.get(pk = int(info[1])),
                base_score = int(info[2]),
                rate = int(info[3])
            )
            model.save()


def build_all():
    build_languages()
    build_regions()
    build_generations()
    build_versions()
    build_damage_classes()
    build_stats()
    build_abilities()
    build_characteristics()
    build_egg_groups()
    build_growth_rates()
    build_items()
    build_types()
    build_contests()
    build_moves()
    build_berries()
    build_natures()
    build_genders()
    build_experiences()
    build_machines()
    build_evolutions()
    build_pokedexes()
    build_locations()
    build_pokemons()
    build_encounters()
    build_pal_parks()

if __name__ == '__main__':
    build_all()
