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
    print('building ' + table_name)
    # Reset DB auto increments to start at 1
    if DB_VENDOR == 'sqlite':
        db_cursor.execute("DELETE FROM sqlite_sequence WHERE name = " + "'" + table_name + "'")
    else:
        db_cursor.execute(
            "SELECT setval(pg_get_serial_sequence(" + "'" + table_name + "'" + ",'id'), 1, false);")


def process_csv(file_name, data_to_models):
    daten = load_data(file_name)
    next(daten, None)  # skip header
    for data in daten:
        for model in data_to_models(data):
            model.save()


def build_generic(model_classes, file_name, data_to_models):
    for model_class in model_classes:
        clear_table(model_class)
    process_csv(file_name, data_to_models)


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


def build_languages():
    _build_languages()

    clear_table(LanguageName)
    data = load_data('language_names.csv')

    for index, info in enumerate(data):
        if index > 0:

            languageName = LanguageName(
                language=Language.objects.get(pk=int(info[0])),
                local_language=Language.objects.get(pk=int(info[1])),
                name=info[2]
            )

            languageName.save()

############
#  REGION  #
############


def build_regions():
    clear_table(Region)
    data = load_data('regions.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = Region(
                id=int(info[0]),
                name=info[1]
            )
            model.save()

    clear_table(RegionName)
    data = load_data('region_names.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = RegionName (
                region = Region.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                name = info[2]
            )
            model.save()



################
#  GENERATION  #
################

def build_generations():
    clear_table(Generation)
    data = load_data('generations.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = Generation (
                id = int(info[0]),
                region = Region.objects.get(pk = int(info[1])),
                name = info[2]
            )
            model.save()

    clear_table(GenerationName)
    data = load_data('generation_names.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = GenerationName (
                generation = Generation.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                name = info[2]
            )
            model.save()



#############
#  VERSION  #
#############

def build_versions():
    clear_table(VersionGroup)
    data = load_data('version_groups.csv')

    for index, info in enumerate(data):
        if index > 0:

            versionGroup = VersionGroup (
                id = int(info[0]),
                name = info[1],
                generation = Generation.objects.get(pk = int(info[2])),
                order = int(info[3])
            )
            versionGroup.save()


    clear_table(VersionGroupRegion)
    data = load_data('version_group_regions.csv')

    for index, info in enumerate(data):
        if index > 0:

            versionGroupRegion = VersionGroupRegion (
                version_group = VersionGroup.objects.get(pk = int(info[0])),
                region = Region.objects.get(pk = int(info[1])),
            )
            versionGroupRegion.save()


    clear_table(Version)
    data = load_data('versions.csv')

    for index, info in enumerate(data):
        if index > 0:

            version = Version (
                id = int(info[0]),
                version_group = VersionGroup.objects.get(pk = int(info[1])),
                name = info[2]
            )
            version.save()


    clear_table(VersionName)
    data = load_data('version_names.csv')

    for index, info in enumerate(data):
        if index > 0:

            versionName = VersionName (
                version = Version.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                name = info[2]
            )
            versionName.save()



##################
#  DAMAGE CLASS  #
##################

def build_damage_classes():
    clear_table(MoveDamageClass)
    data = load_data('move_damage_classes.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = MoveDamageClass (
                id = int(info[0]),
                name = info[1]
            )
            model.save()


    clear_table(MoveDamageClassName)
    clear_table(MoveDamageClassDescription)
    data = load_data('move_damage_class_prose.csv')

    for index, info in enumerate(data):
        if index > 0:

            model_name = MoveDamageClassName (
                move_damage_class = MoveDamageClass.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                name = info[2]
            )
            model_name.save()

            model_description = MoveDamageClassDescription (
                move_damage_class = MoveDamageClass.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                description = info[3]
            )
            model_description.save()


###########
#  STATS  #
###########

def build_stats():
    clear_table(Stat)
    data = load_data('stats.csv')

    for index, info in enumerate(data):
        if index > 0:

            stat = Stat (
                id = int(info[0]),
                move_damage_class = MoveDamageClass.objects.get(pk = int(info[1])) if info[1] != '' else None,
                name = info[2],
                is_battle_only = bool(int(info[3])),
                game_index = int(info[4]) if info[4] else 0,
            )
            stat.save()


    clear_table(StatName)
    data = load_data('stat_names.csv')

    for index, info in enumerate(data):
        if index > 0:

            statName = StatName (
                stat = Stat.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                name = info[2]
            )
            statName.save()


    clear_table(PokeathlonStat)
    data = load_data('pokeathlon_stats.csv')

    for index, info in enumerate(data):
        if index > 0:

            stat = PokeathlonStat (
                id = int(info[0]),
                name = info[1],
            )
            stat.save()


    clear_table(PokeathlonStatName)
    data = load_data('pokeathlon_stat_names.csv')

    for index, info in enumerate(data):
        if index > 0:

            statName = PokeathlonStatName (
                pokeathlon_stat = PokeathlonStat.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                name = info[2]
            )
            statName.save()



# ###############
# #  ABILITIES  #
# ###############

def build_abilities():
    clear_table(Ability)
    data = load_data('abilities.csv')

    for index, info in enumerate(data):
        if index > 0:

            ability = Ability (
                id = int(info[0]),
                name = info[1],
                generation = Generation.objects.get(pk = int(info[2])),
                is_main_series = bool(int(info[3]))
            )
            ability.save()


    clear_table(AbilityName)
    data = load_data('ability_names.csv')

    for index, info in enumerate(data):
        if index > 0:

            abilityName = AbilityName (
                ability = Ability.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                name = info[2]
            )
            abilityName.save()


    clear_table(AbilityChange)
    data = load_data('ability_changelog.csv')

    for index, info in enumerate(data):
        if index > 0:

            abilityName = AbilityChange (
                id = int(info[0]),
                ability = Ability.objects.get(pk = int(info[1])),
                version_group = VersionGroup.objects.get(pk = int(info[2]))
            )
            abilityName.save()


    clear_table(AbilityEffectText)
    data = load_data('ability_prose.csv')

    for index, info in enumerate(data):
        if index > 0:

            abilityDesc = AbilityEffectText (
                ability = Ability.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                short_effect = scrubStr(info[2]),
                effect = scrubStr(info[3])
            )
            abilityDesc.save()


    clear_table(AbilityChangeEffectText)
    data = load_data('ability_changelog_prose.csv')

    for index, info in enumerate(data):
        if index > 0:

            abilityChangeEffectText = AbilityChangeEffectText (
                ability_change = AbilityChange.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                effect = scrubStr(info[2])
            )
            abilityChangeEffectText.save()


    clear_table(AbilityFlavorText)
    data = load_data('ability_flavor_text.csv')

    for index, info in enumerate(data):
        if index > 0:

            abilityFlavorText = AbilityFlavorText (
                ability = Ability.objects.get(pk = int(info[0])),
                version_group = VersionGroup.objects.get(pk = int(info[1])),
                language = Language.objects.get(pk = int(info[2])),
                flavor_text = info[3]
            )
            abilityFlavorText.save()



####################
#  CHARACTERISTIC  #
####################

def build_characteristics():
    clear_table(Characteristic)
    data = load_data('characteristics.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = Characteristic (
                id = int(info[0]),
                stat = Stat.objects.get(pk = int(info[1])),
                gene_mod_5 = int(info[2])
            )
            model.save()


    clear_table(CharacteristicDescription)
    data = load_data('characteristic_text.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = CharacteristicDescription (
                characteristic = Characteristic.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                description = info[2]
            )
            model.save()



###############
#  EGG GROUP  #
###############

def build_egg_groups():
    clear_table(EggGroup)
    data = load_data('egg_groups.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = EggGroup (
                id = int(info[0]),
                name = info[1]
            )
            model.save()


    clear_table(EggGroupName)
    data = load_data('egg_group_prose.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = EggGroupName (
                egg_group = EggGroup.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                name = info[2]
            )
            model.save()



#################
#  GROWTH RATE  #
#################

def build_growth_rates():
    clear_table(GrowthRate)
    data = load_data('growth_rates.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = GrowthRate (
                id = int(info[0]),
                name = info[1],
                formula = info[2]
            )
            model.save()


    clear_table(GrowthRateDescription)
    data = load_data('growth_rate_prose.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = GrowthRateDescription (
                growth_rate = GrowthRate.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                description = info[2]
            )
            model.save()


# ###########
# #  ITEMS  #
# ###########

def build_items():
    clear_table(ItemPocket)
    data = load_data('item_pockets.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = ItemPocket (
                id = int(info[0]),
                name = info[1]
            )
            model.save()


    clear_table(ItemPocketName)
    data = load_data('item_pocket_names.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = ItemPocketName (
                item_pocket = ItemPocket.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                name = info[2]
            )
            model.save()


    clear_table(ItemFlingEffect)
    data = load_data('item_fling_effects.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = ItemFlingEffect (
                id = int(info[0]),
                name = info[1]
            )
            model.save()


    clear_table(ItemFlingEffectEffectText)
    data = load_data('item_fling_effect_prose.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = ItemFlingEffectEffectText (
                item_fling_effect = ItemFlingEffect.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                effect = scrubStr(info[2])
            )
            model.save()


    clear_table(ItemCategory)
    data = load_data('item_categories.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = ItemCategory (
                id = int(info[0]),
                item_pocket = ItemPocket.objects.get(pk = int(info[1])),
                name = info[2]
            )
            model.save()


    clear_table(ItemCategoryName)
    data = load_data('item_category_prose.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = ItemCategoryName (
                item_category = ItemCategory.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                name = info[2]
            )
            model.save()


    clear_table(Item)
    clear_table(ItemSprites)
    data = load_data('items.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = Item (
                id = int(info[0]),
                name = info[1],
                item_category = ItemCategory.objects.get(pk = int(info[2])),
                cost = int(info[3]),
                fling_power = int(info[4]) if info[4] != '' else None,
                item_fling_effect = ItemFlingEffect.objects.get(pk = int(info[5])) if info[5] != '' else None
            )
            model.save()

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

            imageModel = ItemSprites (
                id = index,
                item = Item.objects.get(pk=int(info[0])),
                sprites = json.dumps(sprites)
            )
            imageModel.save()


    clear_table(ItemName)
    data = load_data('item_names.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = ItemName (
                item = Item.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                name = info[2]
            )
            model.save()


    clear_table(ItemEffectText)
    data = load_data('item_prose.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = ItemEffectText (
                item = Item.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                short_effect = scrubStr(info[2]),
                effect = scrubStr(info[3])
            )
            model.save()


    clear_table(ItemGameIndex)
    data = load_data('item_game_indices.csv')

    for index, info in enumerate(data):
        if index > 0:
            model = ItemGameIndex (
                item = Item.objects.get(pk = int(info[0])),
                generation = Generation.objects.get(pk = int(info[1])),
                game_index = int(info[2])
            )
            model.save()


    clear_table(ItemFlavorText)
    data = load_data('item_flavor_text.csv')

    for index, info in enumerate(data):
        if index > 0:
            model = ItemFlavorText (
                item = Item.objects.get(pk = int(info[0])),
                version_group = VersionGroup.objects.get(pk = int(info[1])),
                language = Language.objects.get(pk = int(info[2])),
                flavor_text = info[3]
            )
            model.save()


    clear_table(ItemAttribute)
    data = load_data('item_flags.csv')

    for index, info in enumerate(data):
        if index > 0:
            model = ItemAttribute (
                id = int(info[0]),
                name = info[1]
            )
            model.save()


    clear_table(ItemAttributeName)
    clear_table(ItemAttributeDescription)
    data = load_data('item_flag_prose.csv')

    for index, info in enumerate(data):
        if index > 0:
            model_name = ItemAttributeName (
                item_attribute = ItemAttribute.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                name = info[2]
            )
            model_name.save()
            model_description = ItemAttributeDescription (
                item_attribute = ItemAttribute.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                description = info[3]
            )
            model_description.save()


    clear_table(ItemAttributeMap)
    data = load_data('item_flag_map.csv')

    for index, info in enumerate(data):
        if index > 0:
            model = ItemAttributeMap (
                item = Item.objects.get(pk = int(info[0])),
                item_attribute = ItemAttribute.objects.get(pk = int(info[1]))
            )
            model.save()



###########
#  TYPES  #
###########

def build_types():
    clear_table(Type)
    data = load_data('types.csv')

    for index, info in enumerate(data):
        if index > 0:

            type = Type (
                id = int(info[0]),
                name = info[1],
                generation = Generation.objects.get(pk = int(info[2])),
                move_damage_class = MoveDamageClass.objects.get(pk = int(info[3])) if info[3] != '' else None
            )
            type.save()


    clear_table(TypeName)
    data = load_data('type_names.csv')

    for index, info in enumerate(data):
        if index > 0:

            typeName = TypeName (
                type = Type.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                name = info[2]
            )
            typeName.save()


    clear_table(TypeGameIndex)
    data = load_data('type_game_indices.csv')

    for index, info in enumerate(data):
        if index > 0:

            typeGameIndex = TypeGameIndex (
                type = Type.objects.get(pk = int(info[0])),
                generation = Generation.objects.get(pk = int(info[1])),
                game_index = int(info[2])
            )
            typeGameIndex.save()


    clear_table(TypeEfficacy)
    data = load_data('type_efficacy.csv')

    for index, info in enumerate(data):
        if index > 0:

            typeEfficacy = TypeEfficacy (
                damage_type = Type.objects.get(pk = int(info[0])),
                target_type = Type.objects.get(pk = int(info[1])),
                damage_factor = int(info[2])
            )
            typeEfficacy.save()



#############
#  CONTEST  #
#############

def build_contests():
    clear_table(ContestType)
    data = load_data('contest_types.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = ContestType (
                id = int(info[0]),
                name = info[1]
            )
            model.save()


    clear_table(ContestTypeName)
    data = load_data('contest_type_names.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = ContestTypeName (
                contest_type = ContestType.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                name = info[2],
                flavor = info[3],
                color = info[4]
            )
            model.save()


    clear_table(ContestEffect)
    data = load_data('contest_effects.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = ContestEffect (
                id = int(info[0]),
                appeal = int(info[1]),
                jam = int(info[2])
            )
            model.save()


    clear_table(ContestEffectEffectText)
    data = load_data('contest_effect_prose.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = ContestEffectEffectText (
                contest_effect = ContestEffect.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                effect = info[3]
            )
            model.save()

            model = ContestEffectFlavorText (
                contest_effect = ContestEffect.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                flavor_text = info[2]
            )
            model.save()


    clear_table(SuperContestEffect)
    data = load_data('super_contest_effects.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = SuperContestEffect (
                id = int(info[0]),
                appeal = int(info[1])
            )
            model.save()


    clear_table(SuperContestEffectFlavorText)
    data = load_data('super_contest_effect_prose.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = SuperContestEffectFlavorText (
                super_contest_effect = SuperContestEffect.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                flavor_text = info[2]
            )
            model.save()



###########
#  MOVES  #
###########

def build_moves():
    clear_table(MoveEffect)
    data = load_data('move_effects.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = MoveEffect (
                id = int(info[0])
            )
            model.save()


    clear_table(MoveEffectEffectText)
    data = load_data('move_effect_prose.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = MoveEffectEffectText (
                move_effect = MoveEffect.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                short_effect = scrubStr(info[2]),
                effect = scrubStr(info[3])
            )
            model.save()


    clear_table(MoveEffectChange)
    data = load_data('move_effect_changelog.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = MoveEffectChange (
                id = int(info[0]),
                move_effect = MoveEffect.objects.get(pk = int(info[1])),
                version_group = VersionGroup.objects.get(pk = int(info[2]))
            )
            model.save()


    clear_table(MoveEffectChangeEffectText)
    data = load_data('move_effect_changelog_prose.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = MoveEffectChangeEffectText (
                move_effect_change = MoveEffectChange.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                effect = scrubStr(info[2])
            )
            model.save()


    clear_table(MoveLearnMethod)
    data = load_data('pokemon_move_methods.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = MoveLearnMethod (
                id = int(info[0]),
                name = info[1]
            )
            model.save()


    clear_table(VersionGroupMoveLearnMethod)
    data = load_data('version_group_pokemon_move_methods.csv')

    for index, info in enumerate(data):
        if index > 0:

            versionGroupMoveLearnMethod = VersionGroupMoveLearnMethod (
                version_group = VersionGroup.objects.get(pk = int(info[0])),
                move_learn_method = MoveLearnMethod.objects.get(pk = int(info[1])),
            )
            versionGroupMoveLearnMethod.save()


    clear_table(MoveLearnMethodName)
    clear_table(MoveLearnMethodDescription)
    data = load_data('pokemon_move_method_prose.csv')

    for index, info in enumerate(data):
        if index > 0:

            model_name = MoveLearnMethodName (
                move_learn_method = MoveLearnMethod.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                name = info[2]
            )
            model_name.save()

            model_description = MoveLearnMethodDescription (
                move_learn_method = MoveLearnMethod.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                description = info[3]
            )
            model_description.save()


    clear_table(MoveTarget)
    data = load_data('move_targets.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = MoveTarget (
                id = int(info[0]),
                name = info[1]
            )
            model.save()


    clear_table(MoveTargetName)
    clear_table(MoveTargetDescription)
    data = load_data('move_target_prose.csv')

    for index, info in enumerate(data):
        if index > 0:

            model_name = MoveTargetName (
                move_target = MoveTarget.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                name = info[2]
            )
            model_name.save()

            model_description = MoveTargetDescription (
                move_target = MoveTarget.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                description = info[3]
            )
            model_description.save()


    clear_table(Move)
    data = load_data('moves.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = Move (
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
            model.save()


    clear_table(MoveName)
    data = load_data('move_names.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = MoveName (
                move = Move.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                name = info[2]
            )
            model.save()


    clear_table(MoveFlavorText)
    data = load_data('move_flavor_text.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = MoveFlavorText (
                move = Move.objects.get(pk = int(info[0])),
                version_group = VersionGroup.objects.get(pk = int(info[1])),
                language = Language.objects.get(pk = int(info[2])),
                flavor_text = info[3]
            )
            model.save()


    clear_table(MoveChange)
    data = load_data('move_changelog.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = MoveChange (
                move = Move.objects.get(pk = int(info[0])),
                version_group = VersionGroup.objects.get(pk = int(info[1])),

                type = Type.objects.get(pk = int(info[2])) if info[2] != '' else None,

                power = int(info[3]) if info[3] != '' else None,

                pp = int(info[4]) if info[4] != '' else None,

                accuracy = int(info[5]) if info[5] != '' else None,

                move_effect = MoveEffect.objects.get(pk = int(info[6])) if info[6] != '' else None,

                move_effect_chance = int(info[7]) if info[7] != '' else None
            )
            model.save()


    clear_table(MoveBattleStyle)
    data = load_data('move_battle_styles.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = MoveBattleStyle (
                id = int(info[0]),
                name = info[1]
            )
            model.save()


    clear_table(MoveBattleStyleName)
    data = load_data('move_battle_style_prose.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = MoveBattleStyleName (
                move_battle_style = MoveBattleStyle.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                name = info[2]
            )
            model.save()


    clear_table(MoveAttribute)
    data = load_data('move_flags.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = MoveAttribute (
                id = int(info[0]),
                name = info[1]
            )
            model.save()


    clear_table(MoveAttributeMap)
    data = load_data('move_flag_map.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = MoveAttributeMap (
                move = Move.objects.get(pk = int(info[0])),
                move_attribute = MoveAttribute.objects.get(pk = int(info[1])),
            )
            model.save()


    clear_table(MoveAttributeName)
    clear_table(MoveAttributeDescription)
    data = load_data('move_flag_prose.csv')

    for index, info in enumerate(data):
        if index > 0:

            name_model = MoveAttributeName (
                move_attribute = MoveAttribute.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                name = info[2]
            )
            name_model.save()

            description_model = MoveAttributeDescription (
                move_attribute = MoveAttribute.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                description = scrubStr(info[3])
            )
            description_model.save()


    clear_table(MoveMetaAilment)
    data = load_data('move_meta_ailments.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = MoveMetaAilment (
                id = int(info[0]),
                name = info[1]
            )
            model.save()


    clear_table(MoveMetaAilmentName)
    data = load_data('move_meta_ailment_names.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = MoveMetaAilmentName (
                move_meta_ailment = MoveMetaAilment.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                name = info[2]
            )
            model.save()


    clear_table(MoveMetaCategory)
    data = load_data('move_meta_categories.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = MoveMetaCategory (
                id = int(info[0]),
                name = info[1]
            )
            model.save()


    clear_table(MoveMetaCategoryDescription)
    data = load_data('move_meta_category_prose.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = MoveMetaCategoryDescription (
                move_meta_category = MoveMetaCategory.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                description = info[2]
            )
            model.save()


    clear_table(MoveMeta)
    data = load_data('move_meta.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = MoveMeta (
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
            model.save()


    clear_table(MoveMetaStatChange)
    data = load_data('move_meta_stat_changes.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = MoveMetaStatChange (
                move = Move.objects.get(pk = int(info[0])),
                stat = Stat.objects.get(pk = int(info[1])),
                change = int(info[2])
            )
            model.save()


    clear_table(ContestCombo)
    data = load_data('contest_combos.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = ContestCombo (
                first_move = Move.objects.get(pk = int(info[0])),
                second_move = Move.objects.get(pk = int(info[1]))
            )
            model.save()


    clear_table(SuperContestCombo)
    data = load_data('super_contest_combos.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = SuperContestCombo (
                first_move = Move.objects.get(pk = int(info[0])),
                second_move = Move.objects.get(pk = int(info[1]))
            )
            model.save()



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

    for index, info in enumerate(data):
        if index > 0:

            model = PokemonSpecies (
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
            model.save()

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

    for index, info in enumerate(data):
        if index > 0:

            model = PokemonSpeciesName (
                pokemon_species = PokemonSpecies.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                name = info[2],
                genus = info[3]
            )
            model.save()


    clear_table(PokemonSpeciesDescription)
    data = load_data('pokemon_species_prose.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = PokemonSpeciesDescription (
                pokemon_species = PokemonSpecies.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                description = scrubStr(info[2])
            )
            model.save()


    clear_table(PokemonSpeciesFlavorText)
    data = load_data('pokemon_species_flavor_text.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = PokemonSpeciesFlavorText (
                pokemon_species = PokemonSpecies.objects.get(pk = int(info[0])),
                version = Version.objects.get(pk = int(info[1])),
                language = Language.objects.get(pk = int(info[2])),
                flavor_text = info[3]
            )
            model.save()


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

    for index, info in enumerate(data):
        if index > 0:

            model = PokemonAbility (
                pokemon = Pokemon.objects.get(pk = int(info[0])),
                ability = Ability.objects.get(pk = int(info[1])),
                is_hidden = bool(int(info[2])),
                slot = int(info[3])
            )
            model.save()


    clear_table(PokemonDexNumber)
    data = load_data('pokemon_dex_numbers.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = PokemonDexNumber (
                pokemon_species = PokemonSpecies.objects.get(pk = int(info[0])),
                pokedex = Pokedex.objects.get(pk = int(info[1])),
                pokedex_number = int(info[2])
            )
            model.save()


    clear_table(PokemonEggGroup)
    data = load_data('pokemon_egg_groups.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = PokemonEggGroup (
                pokemon_species = PokemonSpecies.objects.get(pk = int(info[0])),
                egg_group = EggGroup.objects.get(pk = int(info[1]))
            )
            model.save()


    clear_table(PokemonEvolution)
    data = load_data('pokemon_evolution.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = PokemonEvolution (
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
            model.save()


    clear_table(PokemonForm)
    clear_table(PokemonFormSprites)
    data = load_data('pokemon_forms.csv')

    for index, info in enumerate(data):
        if index > 0:

            pokemon = Pokemon.objects.get(pk = int(info[3]))

            model = PokemonForm (
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
            model.save()

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

            imageModel = PokemonFormSprites (
                id = index,
                pokemon_form = PokemonForm.objects.get(pk=int(info[0])),
                sprites = json.dumps(sprites)
            )
            imageModel.save()


    clear_table(PokemonFormName)
    data = load_data('pokemon_form_names.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = PokemonFormName (
                pokemon_form = PokemonForm.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                name = info[2],
                pokemon_name = info[3]
            )
            model.save()


    clear_table(PokemonFormGeneration)
    data = load_data('pokemon_form_generations.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = PokemonFormGeneration (
                pokemon_form = PokemonForm.objects.get(pk = int(info[0])),
                generation = Generation.objects.get(pk = int(info[1])),
                game_index = int(info[2])
            )
            model.save()


    clear_table(PokemonGameIndex)
    data = load_data('pokemon_game_indices.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = PokemonGameIndex (
                pokemon = Pokemon.objects.get(pk = int(info[0])),
                version = Version.objects.get(pk = int(info[1])),
                game_index = int(info[2])
            )
            model.save()


    clear_table(PokemonHabitatName)
    data = load_data('pokemon_habitat_names.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = PokemonHabitatName (
                pokemon_habitat = PokemonHabitat.objects.get(pk = int(info[0])),
                language = Language.objects.get(pk = int(info[1])),
                name = info[2]
            )
            model.save()


    clear_table(PokemonItem)
    data = load_data('pokemon_items.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = PokemonItem (
                pokemon = Pokemon.objects.get(pk = int(info[0])),
                version = Version.objects.get(pk = int(info[1])),
                item = Item.objects.get(pk = int(info[2])),
                rarity = int(info[3])
            )
            model.save()


    clear_table(PokemonMove)
    data = load_data('pokemon_moves.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = PokemonMove (
                pokemon = Pokemon.objects.get(pk = int(info[0])),
                version_group = VersionGroup.objects.get(pk = int(info[1])),
                move = Move.objects.get(pk = int(info[2])),
                move_learn_method = MoveLearnMethod.objects.get(pk = int(info[3])),
                level = int(info[4]),
                order = int(info[5]) if info[5] != '' else None,
            )
            model.save()


    clear_table(PokemonStat)
    data = load_data('pokemon_stats.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = PokemonStat (
                pokemon = Pokemon.objects.get(pk = int(info[0])),
                stat = Stat.objects.get(pk = int(info[1])),
                base_stat = int(info[2]),
                effort = int(info[3])
            )
            model.save()


    clear_table(PokemonType)
    data = load_data('pokemon_types.csv')

    for index, info in enumerate(data):
        if index > 0:

            model = PokemonType (
                pokemon = Pokemon.objects.get(pk = int(info[0])),
                type = Type.objects.get(pk = int(info[1])),
                slot = int(info[2])
            )
            model.save()



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
