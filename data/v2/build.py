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
from django.db.models import get_app, get_models    # MJH 4.24.2016
from django.core import serializers                 # MJH 4.24.2016
import itertools

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
        resourceImages.append(os.path.join(root.replace(imageDir, ""), file))


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
    print('building {}'.format(table_name))
    # Reset DB auto increments to start at 1
    if DB_VENDOR == 'sqlite':
        db_cursor.execute("DELETE FROM sqlite_sequence WHERE name = " + "'" + table_name + "'")
    else:
        db_cursor.execute(
            "SELECT setval(pg_get_serial_sequence(" + "'" + table_name + "'" + ",'id'), 1, false);")


def build_generic(model_class, file_name, data_to_model):
    clear_table(model_class)
    daten = load_data(file_name)
    next(daten, None)  # skip header
    models = []
    for data in daten:
        models.append(next(data_to_model(data)))
    model_class.objects.bulk_create(models)

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

def build_languages():
    def data_to_Language(info):
        yield Language(
            id=int(info[0]),
            iso639=info[1],
            iso3166=info[2],
            name=info[3],
            official=bool(int(info[4])),
            order=info[5],
        )
    build_generic(Language, 'languages.csv', data_to_Language)

    def data_to_LanguageName(info):
        yield LanguageName(
            language=Language.objects.get(pk=int(info[0])),
            local_language=Language.objects.get(pk=int(info[1])),
            name=info[2]
        )
    build_generic(LanguageName, 'language_names.csv', data_to_LanguageName)

############
#  REGION  #
############


def build_regions():

    def data_to_Region(info):
        yield Region(
            id=int(info[0]),
            name=info[1]
        )
    build_generic(Region, 'regions.csv', data_to_Region)

    def data_to_RegionName(info):
        yield RegionName (
            region = Region.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            name = info[2]
        )
    build_generic(RegionName, 'region_names.csv', data_to_RegionName)

################
#  GENERATION  #
################

def build_generations():

    def data_to_Generation(info):
        yield Generation (
            id = int(info[0]),
            region = Region.objects.get(pk = int(info[1])),
            name = info[2]
        )
    build_generic(Generation, 'generations.csv', data_to_Generation)

    def data_to_GenerationName(info):
        yield GenerationName (
            generation = Generation.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            name = info[2]
        )
    build_generic(GenerationName, 'generation_names.csv', data_to_GenerationName)

#############
#  VERSION  #
#############

def build_versions():

    def data_to_VersionGroup(info):
        yield VersionGroup (
            id = int(info[0]),
            name = info[1],
            generation = Generation.objects.get(pk = int(info[2])),
            order = int(info[3])
        )
    build_generic(VersionGroup, 'version_groups.csv', data_to_VersionGroup)

    def data_to_VersionGroupRegion(info):
        yield VersionGroupRegion (
            version_group = VersionGroup.objects.get(pk = int(info[0])),
            region = Region.objects.get(pk = int(info[1])),
        )
    build_generic(VersionGroupRegion, 'version_group_regions.csv', data_to_VersionGroupRegion)

    def data_to_Version(info):
        yield Version (
            id = int(info[0]),
            version_group = VersionGroup.objects.get(pk = int(info[1])),
            name = info[2]
        )
    build_generic(Version, 'versions.csv', data_to_Version)

    def data_to_VersionName(info):
        yield VersionName (
            version = Version.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            name = info[2]
        )
    build_generic(VersionName, 'version_names.csv', data_to_VersionName)

##################
#  DAMAGE CLASS  #
##################

def build_damage_classes():

    def data_to_MoveDamageClass(info):
        yield MoveDamageClass (
            id = int(info[0]),
            name = info[1]
        )
    build_generic(MoveDamageClass, 'move_damage_classes.csv', data_to_MoveDamageClass)

    def data_to_MoveDamageClassName(info):
        yield MoveDamageClassName (
            move_damage_class = MoveDamageClass.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            name = info[2]
        )
    build_generic(MoveDamageClassName, 'move_damage_class_prose.csv', data_to_MoveDamageClassName)

    def data_to_MoveDamageClassDescription(info):
        yield MoveDamageClassDescription (
            move_damage_class = MoveDamageClass.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            description = info[3]
        )
    build_generic(MoveDamageClassDescription, 'move_damage_class_prose.csv', data_to_MoveDamageClassDescription)

###########
#  STATS  #
###########

def build_stats():

    def data_to_Stat(info):
        yield Stat (
            id = int(info[0]),
            move_damage_class = MoveDamageClass.objects.get(pk = int(info[1])) if info[1] != '' else None,
            name = info[2],
            is_battle_only = bool(int(info[3])),
            game_index = int(info[4]) if info[4] else 0,
        )
    build_generic(Stat, 'stats.csv', data_to_Stat)

    def data_to_StatName(info):
        yield StatName (
            stat = Stat.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            name = info[2]
        )
    build_generic(StatName, 'stat_names.csv', data_to_StatName)

    def data_to_PokeathlonStat(info):
        yield PokeathlonStat (
            id = int(info[0]),
            name = info[1],
        )
    build_generic(PokeathlonStat, 'pokeathlon_stats.csv', data_to_PokeathlonStat)

    def data_to_PokeathlonStatName(info):
        yield PokeathlonStatName (
            pokeathlon_stat = PokeathlonStat.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            name = info[2]
        )
    build_generic(PokeathlonStatName, 'pokeathlon_stat_names.csv', data_to_PokeathlonStatName)

# ###############
# #  ABILITIES  #
# ###############

def build_abilities():

    def data_to_Ability(info):
        yield Ability (
            id = int(info[0]),
            name = info[1],
            generation = Generation.objects.get(pk = int(info[2])),
            is_main_series = bool(int(info[3]))
        )
    build_generic(Ability, 'abilities.csv', data_to_Ability)

    def data_to_AbilityName(info):
        yield AbilityName (
            ability = Ability.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            name = info[2]
        )
    build_generic(AbilityName, 'ability_names.csv', data_to_AbilityName)

    def data_to_AbilityChange(info):
        yield AbilityChange (
            id = int(info[0]),
            ability = Ability.objects.get(pk = int(info[1])),
            version_group = VersionGroup.objects.get(pk = int(info[2]))
        )
    build_generic(AbilityChange, 'ability_changelog.csv', data_to_AbilityChange)

    def data_to_AbilityEffectText(info):
        yield AbilityEffectText (
            ability = Ability.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            short_effect = scrubStr(info[2]),
            effect = scrubStr(info[3])
        )
    build_generic(AbilityEffectText, 'ability_prose.csv', data_to_AbilityEffectText)

    def data_to_AbilityChangeEffectText(info):
        yield AbilityChangeEffectText (
            ability_change = AbilityChange.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            effect = scrubStr(info[2])
        )
    build_generic(AbilityChangeEffectText, 'ability_changelog_prose.csv', data_to_AbilityChangeEffectText)

    def data_to_AbilityFlavorText(info):
        yield AbilityFlavorText (
            ability = Ability.objects.get(pk = int(info[0])),
            version_group = VersionGroup.objects.get(pk = int(info[1])),
            language = Language.objects.get(pk = int(info[2])),
            flavor_text = info[3]
        )
    build_generic(AbilityFlavorText, 'ability_flavor_text.csv', data_to_AbilityFlavorText)

####################
#  CHARACTERISTIC  #
####################

def build_characteristics():

    def data_to_Characteristic(info):
        yield Characteristic (
            id = int(info[0]),
            stat = Stat.objects.get(pk = int(info[1])),
            gene_mod_5 = int(info[2])
        )
    build_generic(Characteristic, 'characteristics.csv', data_to_Characteristic)

    def data_to_CharacteristicDescription(info):
        yield CharacteristicDescription (
            characteristic = Characteristic.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            description = info[2]
        )
    build_generic(CharacteristicDescription, 'characteristic_text.csv', data_to_CharacteristicDescription)

###############
#  EGG GROUP  #
###############

def build_egg_groups():

    def data_to_EggGroup(info):
        yield EggGroup (
            id = int(info[0]),
            name = info[1]
        )
    build_generic(EggGroup, 'egg_groups.csv', data_to_EggGroup)

    def data_to_EggGroupName(info):
        yield EggGroupName (
            egg_group = EggGroup.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            name = info[2]
        )
    build_generic(EggGroupName, 'egg_group_prose.csv', data_to_EggGroupName)

#################
#  GROWTH RATE  #
#################

def build_growth_rates():

    def data_to_GrowthRate(info):
        yield GrowthRate (
            id = int(info[0]),
            name = info[1],
            formula = info[2]
        )
    build_generic(GrowthRate, 'growth_rates.csv', data_to_GrowthRate)

    def data_to_GrowthRateDescription(info):
        yield GrowthRateDescription (
            growth_rate = GrowthRate.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            description = info[2]
        )
    build_generic(GrowthRateDescription, 'growth_rate_prose.csv', data_to_GrowthRateDescription)

# ###########
# #  ITEMS  #
# ###########

def build_items():

    def data_to_ItemPocket(info):
        yield ItemPocket (
            id = int(info[0]),
            name = info[1]
        )
    build_generic(ItemPocket, 'item_pockets.csv', data_to_ItemPocket)

    def data_to_ItemPocketName(info):
        yield ItemPocketName (
            item_pocket = ItemPocket.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            name = info[2]
        )
    build_generic(ItemPocketName, 'item_pocket_names.csv', data_to_ItemPocketName)

    def data_to_ItemFlingEffect(info):
        yield ItemFlingEffect (
            id = int(info[0]),
            name = info[1]
        )
    build_generic(ItemFlingEffect, 'item_fling_effects.csv', data_to_ItemFlingEffect)

    def data_to_ItemFlingEffectEffectText(info):
        yield ItemFlingEffectEffectText (
            item_fling_effect = ItemFlingEffect.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            effect = scrubStr(info[2])
        )
    build_generic(ItemFlingEffectEffectText, 'item_fling_effect_prose.csv', data_to_ItemFlingEffectEffectText)

    def data_to_ItemCategory(info):
        yield ItemCategory (
            id = int(info[0]),
            item_pocket = ItemPocket.objects.get(pk = int(info[1])),
            name = info[2]
        )
    build_generic(ItemCategory, 'item_categories.csv', data_to_ItemCategory)

    def data_to_ItemCategoryName(info):
        yield ItemCategoryName (
            item_category = ItemCategory.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            name = info[2]
        )
    build_generic(ItemCategoryName, 'item_category_prose.csv', data_to_ItemCategoryName)

    def data_to_Item(info):
        yield Item (
            id = int(info[0]),
            name = info[1],
            item_category = ItemCategory.objects.get(pk = int(info[2])),
            cost = int(info[3]),
            fling_power = int(info[4]) if info[4] != '' else None,
            item_fling_effect = ItemFlingEffect.objects.get(pk = int(info[5])) if info[5] != '' else None
        )
    build_generic(Item, 'items.csv', data_to_Item)

    def data_to_ItemSprites(info):
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
        yield ItemSprites (
            id = info[0],
            item = Item.objects.get(pk=int(info[0])),
            sprites = json.dumps(sprites)
        )
    build_generic(ItemSprites, 'items.csv', data_to_ItemSprites)

    def data_to_ItemName(info):
        yield ItemName (
            item = Item.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            name = info[2]
        )
    build_generic(ItemName, 'item_names.csv', data_to_ItemName)

    def data_to_ItemEffectText(info):
        yield ItemEffectText (
            item = Item.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            short_effect = scrubStr(info[2]),
            effect = scrubStr(info[3])
        )
    build_generic(ItemEffectText, 'item_prose.csv', data_to_ItemEffectText)

    def data_to_ItemGameIndex(info):
        yield ItemGameIndex (
            item = Item.objects.get(pk = int(info[0])),
            generation = Generation.objects.get(pk = int(info[1])),
            game_index = int(info[2])
        )
    build_generic(ItemGameIndex, 'item_game_indices.csv', data_to_ItemGameIndex)

    def data_to_ItemFlavorText(info):
        yield ItemFlavorText (
            item = Item.objects.get(pk = int(info[0])),
            version_group = VersionGroup.objects.get(pk = int(info[1])),
            language = Language.objects.get(pk = int(info[2])),
            flavor_text = info[3]
        )
    build_generic(ItemFlavorText, 'item_flavor_text.csv', data_to_ItemFlavorText)

    def data_to_ItemAttribute(info):
        yield ItemAttribute (
            id = int(info[0]),
            name = info[1]
        )
    build_generic(ItemAttribute, 'item_flags.csv', data_to_ItemAttribute)

    def data_to_ItemAttributeName(info):
        yield ItemAttributeName (
            item_attribute = ItemAttribute.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            name = info[2]
        )
    build_generic(ItemAttributeName, 'item_flag_prose.csv', data_to_ItemAttributeName)

    def data_to_ItemAttributeDescription(info):
        yield ItemAttributeDescription (
            item_attribute = ItemAttribute.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            description = info[3]
        )
    build_generic(ItemAttributeDescription, 'item_flag_prose.csv', data_to_ItemAttributeDescription)

    def data_to_ItemAttributeMap(info):
        yield ItemAttributeMap (
            item = Item.objects.get(pk = int(info[0])),
            item_attribute = ItemAttribute.objects.get(pk = int(info[1]))
        )
    build_generic(ItemAttributeMap, 'item_flag_map.csv', data_to_ItemAttributeMap)

###########
#  TYPES  #
###########

def build_types():

    def data_to_Type(info):
        yield Type (
            id = int(info[0]),
            name = info[1],
            generation = Generation.objects.get(pk = int(info[2])),
            move_damage_class = MoveDamageClass.objects.get(pk = int(info[3])) if info[3] != '' else None
        )
    build_generic(Type, 'types.csv', data_to_Type)

    def data_to_TypeName(info):
        yield TypeName (
            type = Type.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            name = info[2]
        )
    build_generic(TypeName, 'type_names.csv', data_to_TypeName)

    def data_to_TypeGameIndex(info):
        yield TypeGameIndex (
            type = Type.objects.get(pk = int(info[0])),
            generation = Generation.objects.get(pk = int(info[1])),
            game_index = int(info[2])
        )
    build_generic(TypeGameIndex, 'type_game_indices.csv', data_to_TypeGameIndex)

    def data_to_TypeEfficacy(info):
        yield TypeEfficacy (
            damage_type = Type.objects.get(pk = int(info[0])),
            target_type = Type.objects.get(pk = int(info[1])),
            damage_factor = int(info[2])
        )
    build_generic(TypeEfficacy, 'type_efficacy.csv', data_to_TypeEfficacy)

#############
#  CONTEST  #
#############

def build_contests():

    def data_to_ContestType(info):
        yield ContestType (
            id = int(info[0]),
            name = info[1]
        )
    build_generic(ContestType, 'contest_types.csv', data_to_ContestType)

    def data_to_ContestTypeName(info):
        yield ContestTypeName (
            contest_type = ContestType.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            name = info[2],
            flavor = info[3],
            color = info[4]
        )
    build_generic(ContestTypeName, 'contest_type_names.csv', data_to_ContestTypeName)

    def data_to_ContestEffect(info):
        yield ContestEffect (
            id = int(info[0]),
            appeal = int(info[1]),
            jam = int(info[2])
        )
    build_generic(ContestEffect, 'contest_effects.csv', data_to_ContestEffect)

    def data_to_ContestEffectEffectText(info):
        yield ContestEffectEffectText (
            contest_effect = ContestEffect.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            effect = info[3]
        )
    build_generic(ContestEffectEffectText, 'contest_effect_prose.csv', data_to_ContestEffectEffectText)

    def data_to_ContestEffectFlavorText(info):
        yield ContestEffectFlavorText (
            contest_effect = ContestEffect.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            flavor_text = info[2]
        )
    build_generic(ContestEffectFlavorText, 'contest_effect_prose.csv', data_to_ContestEffectFlavorText)

    def data_to_SuperContestEffect(info):
        yield SuperContestEffect (
            id = int(info[0]),
            appeal = int(info[1])
        )
    build_generic(SuperContestEffect, 'super_contest_effects.csv', data_to_SuperContestEffect)

    def data_to_SuperContestEffectFlavorText(info):
        yield SuperContestEffectFlavorText (
            super_contest_effect = SuperContestEffect.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            flavor_text = info[2]
        )
    build_generic(SuperContestEffectFlavorText, 'super_contest_effect_prose.csv', data_to_SuperContestEffectFlavorText)

###########
#  MOVES  #
###########

def build_moves():

    def data_to_MoveEffect(info):
        yield MoveEffect (
            id = int(info[0])
        )
    build_generic(MoveEffect, 'move_effects.csv', data_to_MoveEffect)

    def data_to_MoveEffectEffectText(info):
        yield MoveEffectEffectText (
            move_effect = MoveEffect.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            short_effect = scrubStr(info[2]),
            effect = scrubStr(info[3])
        )
    build_generic(MoveEffectEffectText, 'move_effect_prose.csv', data_to_MoveEffectEffectText)

    def data_to_MoveEffectChange(info):
        yield MoveEffectChange (
            id = int(info[0]),
            move_effect = MoveEffect.objects.get(pk = int(info[1])),
            version_group = VersionGroup.objects.get(pk = int(info[2]))
        )
    build_generic(MoveEffectChange, 'move_effect_changelog.csv', data_to_MoveEffectChange)

    def data_to_MoveEffectChangeEffectText(info):
        yield MoveEffectChangeEffectText (
            move_effect_change = MoveEffectChange.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            effect = scrubStr(info[2])
        )
    build_generic(MoveEffectChangeEffectText, 'move_effect_changelog_prose.csv', data_to_MoveEffectChangeEffectText)

    def data_to_MoveLearnMethod(info):
        yield MoveLearnMethod (
            id = int(info[0]),
            name = info[1]
        )
    build_generic(MoveLearnMethod, 'pokemon_move_methods.csv', data_to_MoveLearnMethod)

    def data_to_VersionGroupMoveLearnMethod(info):
        yield VersionGroupMoveLearnMethod (
            version_group = VersionGroup.objects.get(pk = int(info[0])),
            move_learn_method = MoveLearnMethod.objects.get(pk = int(info[1])),
        )
    build_generic(VersionGroupMoveLearnMethod, 'version_group_pokemon_move_methods.csv', data_to_VersionGroupMoveLearnMethod)

    def data_to_MoveLearnMethodName(info):
        yield MoveLearnMethodName (
            move_learn_method = MoveLearnMethod.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            name = info[2]
        )
    build_generic(MoveLearnMethodName, 'pokemon_move_method_prose.csv', data_to_MoveLearnMethodName)

    def data_to_MoveLearnMethodDescription(info):
        yield MoveLearnMethodDescription (
            move_learn_method = MoveLearnMethod.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            description = info[3]
        )
    build_generic(MoveLearnMethodDescription, 'pokemon_move_method_prose.csv', data_to_MoveLearnMethodDescription)

    def data_to_MoveTarget(info):
        yield MoveTarget (
            id = int(info[0]),
            name = info[1]
        )
    build_generic(MoveTarget, 'move_targets.csv', data_to_MoveTarget)


    def data_to_MoveTargetName(info):
        yield MoveTargetName (
            move_target = MoveTarget.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            name = info[2]
        )
    build_generic(MoveTargetName, 'move_target_prose.csv', data_to_MoveTargetName)

    def data_to_MoveTargetDescription(info):
        yield MoveTargetDescription (
            move_target = MoveTarget.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            description = info[3]
        )
    build_generic(MoveTargetDescription, 'move_target_prose.csv', data_to_MoveTargetDescription)

    def data_to_Move(info):
        yield Move (
            id = int(info[0]),
            name = info[1],
            generation = Generation.objects.get(pk = int(info[2])),
            type = Type.objects.get(pk = int(info[3])),
            power = int(info[4]) if info[4] != '' else None,
            pp = int(info[5]) if info[5] != '' else None,
            accuracy = int(info[6]) if info[6] != '' else None,
            priority = int(info[7]) if info[7] != '' else None,
            move_target = MoveTarget.objects.get(pk = int(info[8])),
            move_damage_class = MoveDamageClass.objects.get(pk = int(info[9])),
            move_effect = MoveEffect.objects.get(pk = int(info[10])),
            move_effect_chance = int(info[11]) if info[11] != '' else None,
            contest_type = ContestType.objects.get(pk = int(info[12])) if info[12] != '' else None,
            contest_effect = ContestEffect.objects.get(pk = int(info[13])) if info[13] != '' else None,
            super_contest_effect = SuperContestEffect.objects.get(pk = int(info[14])) if info[14] != '' else None
        )
    build_generic(Move, 'moves.csv', data_to_Move)

    def data_to_MoveName(info):
        yield MoveName (
            move = Move.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            name = info[2]
        )
    build_generic(MoveName, 'move_names.csv', data_to_MoveName)

    def data_to_MoveFlavorText(info):
        yield MoveFlavorText (
            move = Move.objects.get(pk = int(info[0])),
            version_group = VersionGroup.objects.get(pk = int(info[1])),
            language = Language.objects.get(pk = int(info[2])),
            flavor_text = info[3]
        )
    build_generic(MoveFlavorText, 'move_flavor_text.csv', data_to_MoveFlavorText)

    def data_to_MoveChange(info):
        yield MoveChange (
            move = Move.objects.get(pk = int(info[0])),
            version_group = VersionGroup.objects.get(pk = int(info[1])),
            type = Type.objects.get(pk = int(info[2])) if info[2] != '' else None,
            power = int(info[3]) if info[3] != '' else None,
            pp = int(info[4]) if info[4] != '' else None,
            accuracy = int(info[5]) if info[5] != '' else None,
            move_effect = MoveEffect.objects.get(pk = int(info[6])) if info[6] != '' else None,
            move_effect_chance = int(info[7]) if info[7] != '' else None
        )
    build_generic(MoveChange, 'move_changelog.csv', data_to_MoveChange)

    def data_to_MoveBattleStyle(info):
        yield MoveBattleStyle (
            id = int(info[0]),
            name = info[1]
        )
    build_generic(MoveBattleStyle, 'move_battle_styles.csv', data_to_MoveBattleStyle)

    def data_to_MoveBattleStyleName(info):
        yield MoveBattleStyleName (
            move_battle_style = MoveBattleStyle.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            name = info[2]
        )
    build_generic(MoveBattleStyleName, 'move_battle_style_prose.csv', data_to_MoveBattleStyleName)

    def data_to_MoveAttribute(info):
        yield MoveAttribute (
            id = int(info[0]),
            name = info[1]
        )
    build_generic(MoveAttribute, 'move_flags.csv', data_to_MoveAttribute)

    def data_to_MoveAttributeMap(info):
        yield MoveAttributeMap (
            move = Move.objects.get(pk = int(info[0])),
            move_attribute = MoveAttribute.objects.get(pk = int(info[1])),
        )
    build_generic(MoveAttributeMap, 'move_flag_map.csv', data_to_MoveAttributeMap)

    def data_to_MoveAttributeName(info):
        yield MoveAttributeName (
            move_attribute = MoveAttribute.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            name = info[2]
        )
    build_generic(MoveAttributeName, 'move_flag_prose.csv', data_to_MoveAttributeName)

    def data_to_MoveAttributeDescription(info):
        yield MoveAttributeDescription (
            move_attribute = MoveAttribute.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            description = scrubStr(info[3])
        )
    build_generic(MoveAttributeDescription, 'move_flag_prose.csv', data_to_MoveAttributeDescription)

    def data_to_MoveMetaAilment(info):
        yield MoveMetaAilment (
            id = int(info[0]),
            name = info[1]
        )
    build_generic(MoveMetaAilment, 'move_meta_ailments.csv', data_to_MoveMetaAilment)

    def data_to_MoveMetaAilmentName(info):
        yield MoveMetaAilmentName (
            move_meta_ailment = MoveMetaAilment.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            name = info[2]
        )
    build_generic(MoveMetaAilmentName, 'move_meta_ailment_names.csv', data_to_MoveMetaAilmentName)

    def data_to_MoveMetaCategory(info):
        yield MoveMetaCategory (
            id = int(info[0]),
            name = info[1]
        )
    build_generic(MoveMetaCategory, 'move_meta_categories.csv', data_to_MoveMetaCategory)

    def data_to_MoveMetaCategoryDescription(info):
        yield MoveMetaCategoryDescription (
            move_meta_category = MoveMetaCategory.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            description = info[2]
        )
    build_generic(MoveMetaCategoryDescription, 'move_meta_category_prose.csv', data_to_MoveMetaCategoryDescription)

    def data_to_MoveMeta(info):
        yield MoveMeta (
            move = Move.objects.get(pk = int(info[0])),
            move_meta_category = MoveMetaCategory.objects.get(pk = int(info[1])),
            move_meta_ailment = MoveMetaAilment.objects.get(pk = int(info[2])),
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
    build_generic(MoveMeta, 'move_meta.csv', data_to_MoveMeta)

    def data_to_MoveMetaStatChange(info):
        yield MoveMetaStatChange (
            move = Move.objects.get(pk = int(info[0])),
            stat = Stat.objects.get(pk = int(info[1])),
            change = int(info[2])
        )
    build_generic(MoveMetaStatChange, 'move_meta_stat_changes.csv', data_to_MoveMetaStatChange)

    def data_to_ContestCombo(info):
        yield ContestCombo (
            first_move = Move.objects.get(pk = int(info[0])),
            second_move = Move.objects.get(pk = int(info[1]))
        )
    build_generic(ContestCombo, 'contest_combos.csv', data_to_ContestCombo)

    def data_to_SuperContestCombo(info):
        yield SuperContestCombo (
            first_move = Move.objects.get(pk = int(info[0])),
            second_move = Move.objects.get(pk = int(info[1]))
        )
    build_generic(SuperContestCombo, 'super_contest_combos.csv', data_to_SuperContestCombo)

#############
#  BERRIES  #
#############

def build_berries():

    def data_to_BerryFirmness(info):
        yield BerryFirmness (
            id = int(info[0]),
            name = info[1]
        )
    build_generic(BerryFirmness, 'berry_firmness.csv', data_to_BerryFirmness)

    def data_to_BerryFirmnessName(info):
        yield BerryFirmnessName (
            berry_firmness = BerryFirmness.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            name = info[2]
        )
    build_generic(BerryFirmnessName, 'berry_firmness_names.csv', data_to_BerryFirmnessName)

    def data_to_Berry(info):
        item = Item.objects.get(pk = int(info[1]))
        yield Berry (
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
    build_generic(Berry, 'berries.csv', data_to_Berry)

    def data_to_BerryFlavor(info):
        contest_type_name = ContestTypeName.objects.get(contest_type_id=int(info[0]), language_id=9)
        yield BerryFlavor (
            id = int(info[0]),
            name = contest_type_name.flavor.lower(),
            contest_type = ContestType.objects.get(pk = int(info[0]))
        )
    build_generic(BerryFlavor, 'contest_types.csv', data_to_BerryFlavor)

    def data_to_BerryFlavorName(info):
        yield BerryFlavorName (
            berry_flavor = BerryFlavor.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            name = info[3]
        )
    build_generic(BerryFlavorName, 'contest_type_names.csv', data_to_BerryFlavorName)

    def data_to_BerryFlavorMap(info):
        yield BerryFlavorMap (
            berry = Berry.objects.get(pk = int(info[0])),
            berry_flavor = BerryFlavor.objects.get(pk = int(info[1])),
            potency = int(info[2])
        )
    build_generic(BerryFlavorMap, 'berry_flavors.csv', data_to_BerryFlavorMap)

############
#  NATURE  #
############

def build_natures():

    def data_to_Nature(info):
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

        yield Nature (
            id = int(info[0]),
            name = info[1],
            decreased_stat = decreased_stat,
            increased_stat = increased_stat,
            hates_flavor = hates_flavor,
            likes_flavor = likes_flavor,
            game_index = info[6]
        )
    build_generic(Nature, 'natures.csv', data_to_Nature)

    def data_to_NatureName(info):
        yield NatureName (
            nature = Nature.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            name = info[2]
        )
    build_generic(NatureName, 'nature_names.csv', data_to_NatureName)

    def data_to_NaturePokeathlonStat(info):
        yield NaturePokeathlonStat (
            nature = Nature.objects.get(pk = int(info[0])),
            pokeathlon_stat = PokeathlonStat.objects.get(pk = int(info[1])),
            max_change = info[2]
        )
    build_generic(NaturePokeathlonStat, 'nature_pokeathlon_stats.csv', data_to_NaturePokeathlonStat)

    def data_to_NatureBattleStylePreference(info):
        yield NatureBattleStylePreference (
            nature = Nature.objects.get(pk = int(info[0])),
            move_battle_style = MoveBattleStyle.objects.get(pk = int(info[1])),
            low_hp_preference = info[2],
            high_hp_preference = info[3]
        )
    build_generic(NatureBattleStylePreference, 'nature_battle_style_preferences.csv', data_to_NatureBattleStylePreference)

###########
# GENDER  #
###########

def build_genders():

    def data_to_Gender(info):
        yield Gender (
            id = int(info[0]),
            name = info[1]
        )
    build_generic(Gender, 'genders.csv', data_to_Gender)

################
#  EXPERIENCE  #
################

def build_experiences():

    def data_to_Experience(info):
        yield Experience (
            growth_rate = GrowthRate.objects.get(pk = int(info[0])),
            level = int(info[1]),
            experience = int(info[2])
      )
    build_generic(Experience, 'experience.csv', data_to_Experience)

##############
#  MACHINES  #
##############

def build_machines():

    def data_to_Machine(info):
        yield Machine (
            machine_number = int(info[0]),
            version_group = VersionGroup.objects.get(pk = int(info[1])),
            item = Item.objects.get(pk = int(info[2])),
            move = Move.objects.get(pk = int(info[3])),
      )
    build_generic(Machine, 'machines.csv', data_to_Machine)

###############
#  EVOLUTION  #
###############

def build_evolutions():

    def data_to_EvolutionChain(info):
        yield EvolutionChain (
            id = int(info[0]),
            baby_trigger_item = Item.objects.get(pk = int(info[1])) if info[1] != '' else None,
        )
    build_generic(EvolutionChain, 'evolution_chains.csv', data_to_EvolutionChain)

    def data_to_EvolutionTrigger(info):
        yield EvolutionTrigger (
            id = int(info[0]),
            name = info[1]
        )
    build_generic(EvolutionTrigger, 'evolution_triggers.csv', data_to_EvolutionTrigger)

    def data_to_EvolutionTriggerName(info):
        yield EvolutionTriggerName (
            evolution_trigger = EvolutionTrigger.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            name = info[2]
      )
    build_generic(EvolutionTriggerName, 'evolution_trigger_prose.csv', data_to_EvolutionTriggerName)

#############
#  POKEDEX  #
#############

def build_pokedexes():

    def data_to_Pokedex(info):
        yield Pokedex (
            id = int(info[0]),
            region = Region.objects.get(pk = int(info[1])) if info[1] != '' else None,
            name = info[2],
            is_main_series = bool(int(info[3]))
      )
    build_generic(Pokedex, 'pokedexes.csv', data_to_Pokedex)

    def data_to_PokedexName(info):
        yield PokedexName (
            pokedex = Pokedex.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            name = info[2],
      )
    build_generic(PokedexName, 'pokedex_prose.csv', data_to_PokedexName)

    def data_to_PokedexDescription(info):
        yield PokedexDescription (
            pokedex = Pokedex.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            description = info[3]
        )
    build_generic(PokedexDescription, 'pokedex_prose.csv', data_to_PokedexDescription)

    def data_to_PokedexVersionGroup(info):
        yield PokedexVersionGroup (
            pokedex = Pokedex.objects.get(pk = int(info[0])),
            version_group = VersionGroup.objects.get(pk = int(info[1]))
        )
    build_generic(PokedexVersionGroup, 'pokedex_version_groups.csv', data_to_PokedexVersionGroup)

##############
#  LOCATION  #
##############

def build_locations():

    def data_to_Location(info):
        yield Location (
            id = int(info[0]),
            region = Region.objects.get(pk = int(info[1])) if info[1] != '' else None,
            name = info[2]
          )
    build_generic(Location, 'locations.csv', data_to_Location)

    def data_to_LocationName(info):
        yield LocationName (
            location = Location.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            name = info[2]
          )
    build_generic(LocationName, 'location_names.csv', data_to_LocationName)

    def data_to_LocationGameIndex(info):
        yield LocationGameIndex (
            location = Location.objects.get(pk = int(info[0])),
            generation = Generation.objects.get(pk = int(info[1])),
            game_index = int(info[2])
          )
    build_generic(LocationGameIndex, 'location_game_indices.csv', data_to_LocationGameIndex)

    def data_to_LocationArea(info):
        location = Location.objects.get(pk = int(info[1]))
        yield LocationArea (
            id = int(info[0]),
            location = location,
            game_index = int(info[2]),
            name = '{}-{}'.format(location.name, info[3]) if info[3] else '{}-{}'.format(location.name, 'area')
        )
    build_generic(LocationArea, 'location_areas.csv', data_to_LocationArea)

    def data_to_LocationAreaName(info):
        yield LocationAreaName (
            location_area = LocationArea.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            name = info[2]
      )
    build_generic(LocationAreaName, 'location_area_prose.csv', data_to_LocationAreaName)

#############
#  POKEMON  #
#############

def build_pokemons():

    def data_to_PokemonColor(info):
        yield PokemonColor (
            id = int(info[0]),
            name = info[1]
        )
    build_generic(PokemonColor, 'pokemon_colors.csv', data_to_PokemonColor)

    def data_to_PokemonColorName(info):
        yield PokemonColorName (
            pokemon_color = PokemonColor.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            name = info[2]
        )
    build_generic(PokemonColorName, 'pokemon_color_names.csv', data_to_PokemonColorName)

    def data_to_PokemonShape(info):
        yield PokemonShape (
            id = int(info[0]),
            name = info[1]
        )
    build_generic(PokemonShape, 'pokemon_shapes.csv', data_to_PokemonShape)

    def data_to_PokemonShapeName(info):
        yield PokemonShapeName (
            pokemon_shape = PokemonShape.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            name = info[2],
            awesome_name = info[3]
        )
    build_generic(PokemonShapeName, 'pokemon_shape_prose.csv', data_to_PokemonShapeName)

    def data_to_PokemonHabitat(info):
        yield PokemonHabitat (
            id = int(info[0]),
            name = info[1]
        )
    build_generic(PokemonHabitat, 'pokemon_habitats.csv', data_to_PokemonHabitat)

    def data_to_PokemonSpecies(info):
        yield PokemonSpecies (
            id = int(info[0]),
            name = info[1],
            generation = Generation.objects.get(pk = int(info[2])),
            evolves_from_species = None,
            evolution_chain = EvolutionChain.objects.get(pk = int(info[4])),
            pokemon_color = PokemonColor.objects.get(pk = int(info[5])),
            pokemon_shape = PokemonShape.objects.get(pk = int(info[6])),
            pokemon_habitat = PokemonHabitat.objects.get(pk = int(info[7])) if info[7] != '' else None,
            gender_rate = int(info[8]),
            capture_rate = int(info[9]),
            base_happiness = int(info[10]),
            is_baby = bool(int(info[11])),
            hatch_counter = int(info[12]),
            has_gender_differences = bool(int(info[13])),
            growth_rate = GrowthRate.objects.get(pk = int(info[14])),
            forms_switchable = bool(int(info[15])),
            order = int(info[16])
        )
    build_generic(PokemonSpecies, 'pokemon_species.csv', data_to_PokemonSpecies)

    data = load_data('pokemon_species.csv')
    next(data)
    for info in data:
        evolves = PokemonSpecies.objects.get(pk = int(info[3])) if info[3] != '' else None
        if evolves:
            species = PokemonSpecies.objects.get(pk = int(info[0]))
            species.evolves_from_species = evolves
            species.save()

    def data_to_PokemonSpeciesName(info):
        yield PokemonSpeciesName (
            pokemon_species = PokemonSpecies.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            name = info[2],
            genus = info[3]
        )
    build_generic(PokemonSpeciesName, 'pokemon_species_names.csv', data_to_PokemonSpeciesName)

    def data_to_PokemonSpeciesDescription(info):
        yield PokemonSpeciesDescription (
            pokemon_species = PokemonSpecies.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            description = scrubStr(info[2])
        )
    build_generic(PokemonSpeciesDescription, 'pokemon_species_prose.csv', data_to_PokemonSpeciesDescription)

    def data_to_PokemonSpeciesFlavorText(info):
        yield PokemonSpeciesFlavorText (
            pokemon_species = PokemonSpecies.objects.get(pk = int(info[0])),
            version = Version.objects.get(pk = int(info[1])),
            language = Language.objects.get(pk = int(info[2])),
            flavor_text = info[3]
        )
    build_generic(PokemonSpeciesFlavorText, 'pokemon_species_flavor_text.csv', data_to_PokemonSpeciesFlavorText)

    def data_to_Pokemon(info):
        yield Pokemon (
            id = int(info[0]),
            name = info[1],
            pokemon_species = PokemonSpecies.objects.get(pk = int(info[2])),
            height = int(info[3]),
            weight = int(info[4]),
            base_experience = int(info[5]),
            order = int(info[6]),
            is_default = bool(int(info[7]))
        )
    build_generic(Pokemon, 'pokemon.csv', data_to_Pokemon)

    def data_to_PokemonSprites(info):
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
        yield PokemonSprites (
            id = info[0],
            pokemon = Pokemon.objects.get(pk=int(info[0])),
            sprites = json.dumps(sprites)
        )
    build_generic(PokemonSprites, 'pokemon.csv', data_to_PokemonSprites)

    def data_to_PokemonAbility(info):
        yield PokemonAbility (
            pokemon = Pokemon.objects.get(pk = int(info[0])),
            ability = Ability.objects.get(pk = int(info[1])),
            is_hidden = bool(int(info[2])),
            slot = int(info[3])
        )
    build_generic(PokemonAbility, 'pokemon_abilities.csv', data_to_PokemonAbility)

    def data_to_PokemonDexNumber(info):
        yield PokemonDexNumber (
            pokemon_species = PokemonSpecies.objects.get(pk = int(info[0])),
            pokedex = Pokedex.objects.get(pk = int(info[1])),
            pokedex_number = int(info[2])
        )
    build_generic(PokemonDexNumber, 'pokemon_dex_numbers.csv', data_to_PokemonDexNumber)

    def data_to_PokemonEggGroup(info):
        yield PokemonEggGroup (
            pokemon_species = PokemonSpecies.objects.get(pk = int(info[0])),
            egg_group = EggGroup.objects.get(pk = int(info[1]))
        )
    build_generic(PokemonEggGroup, 'pokemon_egg_groups.csv', data_to_PokemonEggGroup)

    def data_to_PokemonEvolution(info):
        yield PokemonEvolution (
            id = int(info[0]),
            evolved_species = PokemonSpecies.objects.get(pk = int(info[1])),
            evolution_trigger = EvolutionTrigger.objects.get(pk = int(info[2])),
            evolution_item = Item.objects.get(pk = int(info[3])) if info[3] != '' else None,
            min_level = int(info[4]) if info[4] != '' else None,
            gender = Gender.objects.get(pk = int(info[5])) if info[5] != '' else None,
            location = Location.objects.get(pk = int(info[6])) if info[6] != '' else None,
            held_item = Item.objects.get(pk = int(info[7])) if info[7] != '' else None,
            time_of_day = info[8],
            known_move = Move.objects.get(pk = int(info[9])) if info[9] != '' else None,
            known_move_type = Type.objects.get(pk = int(info[10])) if info[10] != '' else None,
            min_happiness = int(info[11]) if info[11] != '' else None,
            min_beauty = int(info[12]) if info[12] != '' else None,
            min_affection = int(info[13]) if info[13] != '' else None,
            relative_physical_stats = int(info[14]) if info[14] != '' else None,
            party_species = PokemonSpecies.objects.get(pk = int(info[15])) if info[15] != '' else None,
            party_type = Type.objects.get(pk = int(info[16])) if info[16] != '' else None,
            trade_species = PokemonSpecies.objects.get(pk = int(info[17])) if info[17] != '' else None,
            needs_overworld_rain = bool(int(info[18])),
            turn_upside_down = bool(int(info[19]))
        )
    build_generic(PokemonEvolution, 'pokemon_evolution.csv', data_to_PokemonEvolution)


    def data_to_PokemonForm(info):
        pokemon = Pokemon.objects.get(pk = int(info[3]))
        yield PokemonForm (
            id = int(info[0]),
            name = info[1],
            form_name = info[2],
            pokemon = pokemon,
            version_group = VersionGroup.objects.get(pk = int(info[4])),
            is_default = bool(int(info[5])),
            is_battle_only = bool(int(info[6])),
            is_mega = bool(int(info[7])),
            form_order = int(info[8]),
            order = int(info[9])
        )
    build_generic(PokemonForm, 'pokemon_forms.csv', data_to_PokemonForm)

    def data_to_PokemonFormSprites(info):
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
        yield PokemonFormSprites (
            id = info[0],
            pokemon_form = PokemonForm.objects.get(pk=int(info[0])),
            sprites = json.dumps(sprites)
        )
    build_generic(PokemonFormSprites, 'pokemon_forms.csv', data_to_PokemonFormSprites)

    def data_to_PokemonFormName(info):
        yield PokemonFormName (
            pokemon_form = PokemonForm.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            name = info[2],
            pokemon_name = info[3]
        )
    build_generic(PokemonFormName, 'pokemon_form_names.csv', data_to_PokemonFormName)

    def data_to_PokemonFormGeneration(info):
        yield PokemonFormGeneration (
            pokemon_form = PokemonForm.objects.get(pk = int(info[0])),
            generation = Generation.objects.get(pk = int(info[1])),
            game_index = int(info[2])
        )
    build_generic(PokemonFormGeneration, 'pokemon_form_generations.csv', data_to_PokemonFormGeneration)

    def data_to_PokemonGameIndex(info):
        yield PokemonGameIndex (
            pokemon = Pokemon.objects.get(pk = int(info[0])),
            version = Version.objects.get(pk = int(info[1])),
            game_index = int(info[2])
        )
    build_generic(PokemonGameIndex, 'pokemon_game_indices.csv', data_to_PokemonGameIndex)

    def data_to_PokemonHabitatName(info):
        yield PokemonHabitatName (
            pokemon_habitat = PokemonHabitat.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            name = info[2]
        )
    build_generic(PokemonHabitatName, 'pokemon_habitat_names.csv', data_to_PokemonHabitatName)

    def data_to_PokemonItem(info):
        yield PokemonItem (
            pokemon = Pokemon.objects.get(pk = int(info[0])),
            version = Version.objects.get(pk = int(info[1])),
            item = Item.objects.get(pk = int(info[2])),
            rarity = int(info[3])
        )
    build_generic(PokemonItem, 'pokemon_items.csv', data_to_PokemonItem)

    def data_to_PokemonMove(info):
        yield PokemonMove (
            pokemon = Pokemon.objects.get(pk = int(info[0])),
            version_group = VersionGroup.objects.get(pk = int(info[1])),
            move = Move.objects.get(pk = int(info[2])),
            move_learn_method = MoveLearnMethod.objects.get(pk = int(info[3])),
            level = int(info[4]),
            order = int(info[5]) if info[5] != '' else None,
        )
    build_generic(PokemonMove, 'pokemon_moves.csv', data_to_PokemonMove)

    def data_to_PokemonStat(info):
        yield PokemonStat (
            pokemon = Pokemon.objects.get(pk = int(info[0])),
            stat = Stat.objects.get(pk = int(info[1])),
            base_stat = int(info[2]),
            effort = int(info[3])
        )
    build_generic(PokemonStat, 'pokemon_stats.csv', data_to_PokemonStat)

    def data_to_PokemonType(info):
        yield PokemonType (
            pokemon = Pokemon.objects.get(pk = int(info[0])),
            type = Type.objects.get(pk = int(info[1])),
            slot = int(info[2])
        )
    build_generic(PokemonType, 'pokemon_types.csv', data_to_PokemonType)

###############
#  ENCOUNTER  #
###############

def build_encounters():

    def data_to_EncounterMethod(info):
        yield EncounterMethod (
            id = int(info[0]),
            name = info[1],
            order = int(info[2])
        )
    build_generic(EncounterMethod, 'encounter_methods.csv', data_to_EncounterMethod)

    # LocationAreaEncounterRate/EncounterMethod associations
    """
    I tried handling this the same way Berry/Natures are handled
    but for some odd reason it resulted in a ton of db table issues.
    It was easy enough to move LocationAreaEncounterRates below
    Encounter population and for some reason things works now.
    """

    def data_to_LocationAreaEncounterRate(info):
        yield LocationAreaEncounterRate (
            location_area = LocationArea.objects.get(pk = int(info[0])),
            encounter_method = EncounterMethod.objects.get(pk=info[1]),
            version = Version.objects.get(pk = int(info[2])),
            rate = int(info[3])
        )
    build_generic(LocationAreaEncounterRate, 'location_area_encounter_rates.csv', data_to_LocationAreaEncounterRate)

    def data_to_EncounterMethodName(info):
        yield EncounterMethodName (
            encounter_method = EncounterMethod.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            name = info[2]
        )
    build_generic(EncounterMethodName, 'encounter_method_prose.csv', data_to_EncounterMethodName)

    def data_to_EncounterSlot(info):
        yield EncounterSlot (
            id = int(info[0]),
            version_group = VersionGroup.objects.get(pk = int(info[1])),
            encounter_method = EncounterMethod.objects.get(pk = int(info[2])),
            slot = int(info[3]) if info[3] != '' else None,
            rarity = int(info[4])
        )
    build_generic(EncounterSlot, 'encounter_slots.csv', data_to_EncounterSlot)

    def data_to_EncounterCondition(info):
        yield EncounterCondition (
            id = int(info[0]),
            name = info[1]
        )
    build_generic(EncounterCondition, 'encounter_conditions.csv', data_to_EncounterCondition)

    def data_to_EncounterConditionName(info):
        yield EncounterConditionName (
            encounter_condition = EncounterCondition.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            name = info[2]
        )
    build_generic(EncounterConditionName, 'encounter_condition_prose.csv', data_to_EncounterConditionName)

    def data_to_Encounter(info):
        yield Encounter (
            id = int(info[0]),
            version = Version.objects.get(pk = int(info[1])),
            location_area = LocationArea.objects.get(pk = int(info[2])),
            encounter_slot = EncounterSlot.objects.get(pk = int(info[3])),
            pokemon = Pokemon.objects.get(pk = int(info[4])),
            min_level = int(info[5]),
            max_level = int(info[6])
        )
    build_generic(Encounter, 'encounters.csv', data_to_Encounter)

    def data_to_EncounterConditionValue(info):
        yield EncounterConditionValue (
            id = int(info[0]),
            encounter_condition = EncounterCondition.objects.get(pk = int(info[1])),
            name = info[2],
            is_default = bool(int(info[3]))
        )
    build_generic(EncounterConditionValue, 'encounter_condition_values.csv', data_to_EncounterConditionValue)

    def data_to_EncounterConditionValueName(info):
        yield EncounterConditionValueName (
            encounter_condition_value = EncounterConditionValue.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            name = info[2],
        )
    build_generic(EncounterConditionValueName, 'encounter_condition_value_prose.csv', data_to_EncounterConditionValueName)

    def data_to_EncounterConditionValueMap(info):
        yield EncounterConditionValueMap (
            encounter = Encounter.objects.get(pk = int(info[0])),
            encounter_condition_value = EncounterConditionValue.objects.get(pk = int(info[1]))
        )
    build_generic(EncounterConditionValueMap, 'encounter_condition_value_map.csv', data_to_EncounterConditionValueMap)

##############
#  PAL PARK  #
##############

def build_pal_parks():

    def data_to_PalParkArea(info):
        yield PalParkArea (
            id = int(info[0]),
            name = info[1]
        )
    build_generic(PalParkArea, 'pal_park_areas.csv', data_to_PalParkArea)

    def data_to_PalParkAreaName(info):
        yield PalParkAreaName (
            pal_park_area = PalParkArea.objects.get(pk = int(info[0])),
            language = Language.objects.get(pk = int(info[1])),
            name = info[2]
        )
    build_generic(PalParkAreaName, 'pal_park_area_names.csv', data_to_PalParkAreaName)

    def data_to_PalPark(info):
        yield PalPark (
            pokemon_species = PokemonSpecies.objects.get(pk = int(info[0])),
            pal_park_area = PalParkArea.objects.get(pk = int(info[1])),
            base_score = int(info[2]),
            rate = int(info[3])
        )
    build_generic(PalPark, 'pal_park.csv', data_to_PalPark)

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

#Courtesy of nimjae
def dump_one():
    with open('dev-data.json', 'w+') as out:
        out.write(serializers.serialize('json',
            itertools.chain.from_iterable(model.objects.all()
                for model in get_models(get_app('pokemon_v2')))))
def dump_all():
    app = get_app('pokemon_v2')
    for model in get_models(app):
        data = serializers.serialize("json", model.objects.all())
        file_name = 'pokemon_v2/fixtures/{}.json'.format(model.__name__)
        #using 'with' will close the file even if there
        #is an exception (/pokeapi/pull/162)
        with open(file_name, 'w+') as out:
            out.write(data)
            out.close()

if __name__ == '__main__':
    build_all()
