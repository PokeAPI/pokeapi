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
        models[model_class] = [] # one list per model class

    data = load_data(file_name)
    next(data, None)  # skip header

    for record in data:
        for model in data_to_models(record):
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

    def data_to_model(info):
        yield Language(
            id=int(info[0]),
            iso639=info[1],
            iso3166=info[2],
            name=info[3],
            official=bool(int(info[4])),
            order=info[5],
        )
    build_generic((Language,), 'languages.csv', data_to_model)

    def data_to_model(info):
        yield LanguageName(
            language_id=int(info[0]),
            local_language_id=int(info[1]),
            name=info[2]
        )
    build_generic((LanguageName,), 'language_names.csv', data_to_model)



############
#  REGION  #
############

def _build_regions():

    def data_to_model(info):
        yield Region(
            id=int(info[0]),
            name=info[1]
        )
    build_generic((Region,), 'regions.csv', data_to_model)

    def data_to_model(info):
        yield RegionName(
            region_id = int(info[0]),
            language_id = int(info[1]),
            name = info[2]
        )
    build_generic((RegionName,), 'region_names.csv', data_to_model)



################
#  GENERATION  #
################

def _build_generations():
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

def _build_versions():

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

def _build_damage_classes():

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

def _build_stats():

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

def _build_abilities():

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

def _build_characteristics():

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

def _build_egg_groups():

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

def _build_growth_rates():

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

def _build_items():

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

def _build_types():

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

def _build_contests():

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

def _build_moves():

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

def _build_berries():

    def data_to_model(info):
        yield BerryFirmness(
            id = int(info[0]),
            name = info[1]
        )
    build_generic((BerryFirmness,), 'berry_firmness.csv', data_to_model)

    def data_to_model(info):
        yield BerryFirmnessName(
            berry_firmness_id = int(info[0]),
            language_id = int(info[1]),
            name = info[2]
        )
    build_generic((BerryFirmnessName,), 'berry_firmness_names.csv', data_to_model)

    def data_to_model(info):
        item = Item.objects.get(pk = int(info[1]))
        yield Berry(
            id = int(info[0]),
            item_id = int(info[1]),
            name = item.name[:item.name.index('-')],
            berry_firmness_id = int(info[2]),
            natural_gift_power = int(info[3]),
            natural_gift_type_id = int(info[4]),
            size = int(info[5]),
            max_harvest = int(info[6]),
            growth_time = int(info[7]),
            soil_dryness = int(info[8]),
            smoothness = int(info[9])
        )
    build_generic((Berry,), 'berries.csv', data_to_model)

    def data_to_model(info):
        # Get the english name for this contest type
        contest_type_name = ContestTypeName.objects.get(contest_type_id=int(info[0]), language_id=9)
        yield BerryFlavor(
            id = int(info[0]),
            name = contest_type_name.flavor.lower(),
            contest_type = ContestType.objects.get(pk = int(info[0]))
        )
    build_generic((BerryFlavor,), 'contest_types.csv', data_to_model) # This is not an error

    def data_to_model(info):
        yield BerryFlavorName(
            berry_flavor_id = int(info[0]),
            language_id = int(info[1]),
            name = info[3]
        )
    build_generic((BerryFlavorName,), 'contest_type_names.csv', data_to_model) # This is not an error

    def data_to_model(info):
        yield BerryFlavorMap(
            berry_id = int(info[0]),
            berry_flavor_id = int(info[1]),
            potency = int(info[2])
        )
    build_generic((BerryFlavorMap,), 'berry_flavors.csv', data_to_model) # This is not an error



############
#  NATURE  #
############

def _build_natures():

    def data_to_model(info):
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

        yield Nature(
            id = int(info[0]),
            name = info[1],
            decreased_stat = decreased_stat,
            increased_stat = increased_stat,
            hates_flavor = hates_flavor,
            likes_flavor = likes_flavor,
            game_index = info[6]
        )
    build_generic((Nature,), 'natures.csv', data_to_model)

    def data_to_model(info):
        yield NatureName(
            nature_id = int(info[0]),
            language_id = int(info[1]),
            name = info[2]
        )
    build_generic((NatureName,), 'nature_names.csv', data_to_model)

    def data_to_model(info):
        yield NaturePokeathlonStat(
            nature_id = (info[0]),
            pokeathlon_stat_id = (info[1]),
            max_change = info[2]
        )
    build_generic((NaturePokeathlonStat,), 'nature_pokeathlon_stats.csv', data_to_model)

    def data_to_model(info):
        yield NatureBattleStylePreference(
            nature_id = int(info[0]),
            move_battle_style_id = int(info[1]),
            low_hp_preference = info[2],
            high_hp_preference = info[3]
        )
    build_generic((NatureBattleStylePreference,), 'nature_battle_style_preferences.csv', data_to_model)



###########
# GENDER  #
###########

def _build_genders():

    def data_to_model(info):
        yield Gender(
            id = int(info[0]),
            name = info[1]
        )
    build_generic((Gender,), 'genders.csv', data_to_model)



################
#  EXPERIENCE  #
################

def _build_experiences():

    def data_to_model(info):
        yield Experience(
            growth_rate_id = int(info[0]),
            level = int(info[1]),
            experience = int(info[2])
        )
    build_generic((Experience,), 'experience.csv', data_to_model)



##############
#  MACHINES  #
##############

def _build_machines():

    def data_to_model(info):
        yield Machine(
            machine_number = int(info[0]),
            version_group_id = int(info[1]),
            item_id = int(info[2]),
            move_id = int(info[3]),
        )
    build_generic((Machine,), 'machines.csv', data_to_model)



###############
#  EVOLUTION  #
###############

def _build_evolutions():

    def data_to_model(info):
        yield EvolutionChain(
            id = int(info[0]),
            baby_trigger_item_id = int(info[1]) if info[1] != '' else None,
        )
    build_generic((EvolutionChain,), 'evolution_chains.csv', data_to_model)

    def data_to_model(info):
        yield EvolutionTrigger(
            id = int(info[0]),
            name = info[1]
        )
    build_generic((EvolutionTrigger,), 'evolution_triggers.csv', data_to_model)

    def data_to_model(info):
        yield EvolutionTriggerName(
            evolution_trigger_id = int(info[0]),
            language_id = int(info[1]),
            name = info[2]
        )
    build_generic((EvolutionTriggerName,), 'evolution_trigger_prose.csv', data_to_model)



#############
#  POKEDEX  #
#############

def _build_pokedexes():

    def data_to_model(info):
        yield Pokedex(
            id = int(info[0]),
            region_id = int(info[1]) if info[1] != '' else None,
            name = info[2],
            is_main_series = bool(int(info[3]))
        )
    build_generic((Pokedex,), 'pokedexes.csv', data_to_model)

    def data_to_model(info):
        yield PokedexName(
            pokedex_id = int(info[0]),
            language_id = int(info[1]),
            name = info[2],
        )
        yield PokedexDescription(
            pokedex_id = int(info[0]),
            language_id = int(info[1]),
            description = info[3]
        )
    build_generic((PokedexName, PokedexDescription), 'pokedex_prose.csv', data_to_model)

    def data_to_model(info):
        yield PokedexVersionGroup(
            pokedex_id = int(info[0]),
            version_group_id = int(info[1])
        )
    build_generic((PokedexVersionGroup,), 'pokedex_version_groups.csv', data_to_model)



##############
#  LOCATION  #
##############

def _build_locations():

    def data_to_model(info):
        yield Location(
            id = int(info[0]),
            region_id = int(info[1]) if info[1] != '' else None,
            name = info[2]
        )
    build_generic((Location,), 'locations.csv', data_to_model)

    def data_to_model(info):
        yield LocationName(
            location_id = int(info[0]),
            language_id = int(info[1]),
            name = info[2]
        )
    build_generic((LocationName,), 'location_names.csv', data_to_model)

    def data_to_model(info):
        yield LocationGameIndex(
            location_id = int(info[0]),
            generation_id = int(info[1]),
            game_index = int(info[2])
        )
    build_generic((LocationGameIndex,), 'location_game_indices.csv', data_to_model)

    def data_to_model(info):
        location = Location.objects.get(pk = int(info[1]))
        yield LocationArea(
            id = int(info[0]),
            location_id = int(info[1]),
            game_index = int(info[2]),
            name = '{}-{}'.format(location.name, info[3]) if info[3] else '{}-{}'.format(location.name, 'area')
        )
    build_generic((LocationArea,), 'location_areas.csv', data_to_model)

    def data_to_model(info):
        yield LocationAreaName(
            location_area_id = int(info[0]),
            language_id = int(info[1]),
            name = info[2]
        )
    build_generic((LocationAreaName,), 'location_area_prose.csv', data_to_model)



#############
#  POKEMON  #
#############

def _build_pokemons():

    def data_to_model(info):
        yield PokemonColor(
            id = int(info[0]),
            name = info[1]
        )
    build_generic((PokemonColor,), 'pokemon_colors.csv', data_to_model)

    def data_to_model(info):
        yield PokemonColorName(
            pokemon_color_id = int(info[0]),
            language_id = int(info[1]),
            name = info[2]
        )
    build_generic((PokemonColorName,), 'pokemon_color_names.csv', data_to_model)

    def data_to_model(info):
        yield PokemonShape(
            id = int(info[0]),
            name = info[1]
        )
    build_generic((PokemonShape,), 'pokemon_shapes.csv', data_to_model)

    def data_to_model(info):
        yield PokemonShapeName(
            pokemon_shape_id = int(info[0]),
            language_id = int(info[1]),
            name = info[2],
            awesome_name = info[3]
        )
    build_generic((PokemonShapeName,), 'pokemon_shape_prose.csv', data_to_model)

    def data_to_model(info):
        yield PokemonHabitat(
            id = int(info[0]),
            name = info[1]
        )
    build_generic((PokemonHabitat,), 'pokemon_habitats.csv', data_to_model)

    def data_to_model(info):
        yield PokemonSpecies(
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
        )
    build_generic((PokemonSpecies,), 'pokemon_species.csv', data_to_model)

    # PokemonSpecies.evolves_from_species can't be set until all the species are created
    data = load_data('pokemon_species.csv')
    for index, info in enumerate(data):
        if index > 0:
            evolves = PokemonSpecies.objects.get(pk = int(info[3])) if info[3] != '' else None
            if evolves:
                species = PokemonSpecies.objects.get(pk = int(info[0]))
                species.evolves_from_species = evolves
                species.save()

    def data_to_model(info):
        yield PokemonSpeciesName(
            pokemon_species_id = int(info[0]),
            language_id = int(info[1]),
            name = info[2],
            genus = info[3]
        )
    build_generic((PokemonSpeciesName,), 'pokemon_species_names.csv', data_to_model)

    def data_to_model(info):
        yield PokemonSpeciesDescription(
            pokemon_species_id = int(info[0]),
            language_id = int(info[1]),
            description = scrubStr(info[2])
        )
    build_generic((PokemonSpeciesDescription,), 'pokemon_species_prose.csv', data_to_model)

    def data_to_model(info):
        yield PokemonSpeciesFlavorText(
            pokemon_species_id = int(info[0]),
            version_id = int(info[1]),
            language_id = int(info[2]),
            flavor_text = info[3]
        )
    build_generic((PokemonSpeciesFlavorText,), 'pokemon_species_flavor_text.csv', data_to_model)

    def data_to_model(info):
        yield Pokemon(
            id = int(info[0]),
            name = info[1],
            pokemon_species_id = int(info[2]),
            height = int(info[3]),
            weight = int(info[4]),
            base_experience = int(info[5]),
            order = int(info[6]),
            is_default = bool(int(info[7]))
        )
    build_generic((Pokemon,), 'pokemon.csv', data_to_model)

    def data_to_model(info):
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
        yield PokemonSprites(
            id = int(info[0]),
            pokemon = Pokemon.objects.get(pk=int(info[0])),
            sprites = json.dumps(sprites)
        )
    build_generic((PokemonSprites,), 'pokemon.csv', data_to_model)

    def data_to_model(info):
        yield PokemonAbility(
            pokemon_id = int(info[0]),
            ability_id = int(info[1]),
            is_hidden = bool(int(info[2])),
            slot = int(info[3])
        )
    build_generic((PokemonAbility,), 'pokemon_abilities.csv', data_to_model)

    def data_to_model(info):
        yield PokemonDexNumber(
            pokemon_species_id = int(info[0]),
            pokedex_id = int(info[1]),
            pokedex_number = int(info[2])
        )
    build_generic((PokemonDexNumber,), 'pokemon_dex_numbers.csv', data_to_model)

    def data_to_model(info):
        yield PokemonEggGroup(
            pokemon_species_id = int(info[0]),
            egg_group_id = int(info[1])
        )
    build_generic((PokemonEggGroup,), 'pokemon_egg_groups.csv', data_to_model)

    def data_to_model(info):
        yield PokemonEvolution(
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
        )
    build_generic((PokemonEvolution,), 'pokemon_evolution.csv', data_to_model)

    def data_to_model(info):
        yield PokemonForm(
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
        )
    build_generic((PokemonForm,), 'pokemon_forms.csv', data_to_model)

    def data_to_model(info):
        pokemon = Pokemon.objects.get(pk = int(info[3]))
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
        yield PokemonFormSprites(
            id = int(info[0]),
            pokemon_form_id = int(info[0]),
            sprites = json.dumps(sprites)
        )
    build_generic((PokemonFormSprites,), 'pokemon_forms.csv', data_to_model)

    def data_to_model(info):
        yield PokemonFormName(
            pokemon_form = PokemonForm.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            name = info[2],
            pokemon_name = info[3]
        )
    build_generic((PokemonFormName,), 'pokemon_form_names.csv', data_to_model)

    def data_to_model(info):
        yield PokemonFormGeneration(
            pokemon_form_id = int(info[0]),
            generation_id = int(info[1]),
            game_index = int(info[2])
        )
    build_generic((PokemonFormGeneration,), 'pokemon_form_generations.csv', data_to_model)

    def data_to_model(info):
        yield PokemonGameIndex(
            pokemon_id = int(info[0]),
            version_id = int(info[1]),
            game_index = int(info[2])
        )
    build_generic((PokemonGameIndex,), 'pokemon_game_indices.csv', data_to_model)

    def data_to_model(info):
        yield PokemonHabitatName(
            pokemon_habitat_id = int(info[0]),
            language_id = int(info[1]),
            name = info[2]
        )
    build_generic((PokemonHabitatName,), 'pokemon_habitat_names.csv', data_to_model)

    def data_to_model(info):
        yield PokemonItem(
            pokemon_id = int(info[0]),
            version_id = int(info[1]),
            item_id = int(info[2]),
            rarity = int(info[3])
        )
    build_generic((PokemonItem,), 'pokemon_items.csv', data_to_model)

    def data_to_model(info):
        yield PokemonMove(
            pokemon_id = int(info[0]),
            version_group_id = int(info[1]),
            move_id = int(info[2]),
            move_learn_method_id = int(info[3]),
            level = int(info[4]),
            order = int(info[5]) if info[5] != '' else None,
        )
    build_generic((PokemonMove,), 'pokemon_moves.csv', data_to_model)

    def data_to_model(info):
        yield PokemonStat(
            pokemon_id = int(info[0]),
            stat_id = int(info[1]),
            base_stat = int(info[2]),
            effort = int(info[3])
        )
    build_generic((PokemonStat,), 'pokemon_stats.csv', data_to_model)

    def data_to_model(info):
        yield PokemonType(
            pokemon_id = int(info[0]),
            type_id = int(info[1]),
            slot = int(info[2])
        )
    build_generic((PokemonType,), 'pokemon_types.csv', data_to_model)



###############
#  ENCOUNTER  #
###############

def _build_encounters():

    def data_to_model(info):
        yield EncounterMethod(
            id = int(info[0]),
            name = info[1],
            order = int(info[2])
        )
    build_generic((EncounterMethod,), 'encounter_methods.csv', data_to_model)

    def data_to_model(info):
        yield LocationAreaEncounterRate(
            location_area_id = int(info[0]),
            encounter_method_id = int(info[1]),
            version_id = int(info[2]),
            rate = int(info[3])
        )
    build_generic((LocationAreaEncounterRate,), 'location_area_encounter_rates.csv', data_to_model)

    def data_to_model(info):
        yield EncounterMethodName(
            encounter_method_id = int(info[0]),
            language_id = int(info[1]),
            name = info[2]
        )
    build_generic((EncounterMethodName,), 'encounter_method_prose.csv', data_to_model)

    def data_to_model(info):
        yield EncounterCondition(
            id = int(info[0]),
            name = info[1]
        )
    build_generic((EncounterCondition,), 'encounter_conditions.csv', data_to_model)

    def data_to_model(info):
        yield EncounterConditionName(
            encounter_condition_id = int(info[0]),
            language_id = int(info[1]),
            name = info[2]
        )
    build_generic((EncounterConditionName,), 'encounter_condition_prose.csv', data_to_model)

    def data_to_model(info):
        yield EncounterSlot(
            id = int(info[0]),
            version_group_id = int(info[1]),
            encounter_method_id = int(info[2]),
            slot = int(info[3]) if info[3] != '' else None,
            rarity = int(info[4])
        )
    build_generic((EncounterSlot,), 'encounter_slots.csv', data_to_model)

    def data_to_model(info):
        yield Encounter(
            id = int(info[0]),
            version_id = int(info[1]),
            location_area_id = int(info[2]),
            encounter_slot_id = int(info[3]),
            pokemon_id = int(info[4]),
            min_level = int(info[5]),
            max_level = int(info[6])
        )
    build_generic((Encounter,), 'encounters.csv', data_to_model)

    def data_to_model(info):
        yield EncounterConditionValue(
            id = int(info[0]),
            encounter_condition_id = int(info[1]),
            name = info[2],
            is_default = bool(int(info[3]))
        )
    build_generic((EncounterConditionValue,), 'encounter_condition_values.csv', data_to_model)

    def data_to_model(info):
        yield EncounterConditionValueName(
            encounter_condition_value_id = int(info[0]),
            language_id = int(info[1]),
            name = info[2],
        )
    build_generic((EncounterConditionValueName,), 'encounter_condition_value_prose.csv', data_to_model)

    def data_to_model(info):
        yield EncounterConditionValueMap(
            encounter_id = int(info[0]),
            encounter_condition_value_id = int(info[1])
        )
    build_generic((EncounterConditionValueMap,), 'encounter_condition_value_map.csv', data_to_model)



##############
#  PAL PARK  #
##############

def _build_pal_parks():

    def data_to_model(info):
        yield PalParkArea(
            id = int(info[0]),
            name = info[1]
        )
    build_generic((PalParkArea,), 'pal_park_areas.csv', data_to_model)

    def data_to_model(info):
        yield PalParkAreaName(
            pal_park_area_id = int(info[0]),
            language_id = int(info[1]),
            name = info[2]
        )
    build_generic((PalParkAreaName,), 'pal_park_area_names.csv', data_to_model)

    def data_to_model(info):
        yield PalPark(
            pokemon_species_id = int(info[0]),
            pal_park_area_id = int(info[1]),
            base_score = int(info[2]),
            rate = int(info[3])
        )
    build_generic((PalPark,), 'pal_park.csv', data_to_model)


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

if __name__ == '__main__':
    build_all()
