#  To build out the data you'll need to jump into the Django shell
#
#     $ python manage.py shell
#
#  and run the build script with
#
#     $ execfile('data/v2/build.py')
#
#  Each time the build script is run it will iterate over each table in the database,
#  wipe it and rewrite each row using the data found in data/v2/csv.
#  If you don't need all of the data just go into data/v2/build.py and
#  comment out everything but what you need to build the tables you're looking for.
#  This might be useful because some of the csv files are massive
#  (pokemon_moves expecially) and it can take about 30 minutes to build everything.

import csv
import os
from django.db import migrations, connection
from pokemon_v2.models import *


data_location = 'data/v2/csv/'
db_cursor = connection.cursor()
db_vendor = connection.vendor


def loadData(fileName):
  return csv.reader(open(data_location + fileName, 'rb'), delimiter=',')


def clearTable(model):

  table_name = model._meta.db_table
  model.objects.all().delete()

  print 'building ' + table_name

  # Reset DB auto increments to start at 1
  if db_vendor == 'sqlite':
    db_cursor.execute("DELETE FROM sqlite_sequence WHERE name = " + "'" + table_name + "'" )
  else:
    db_cursor.execute("SELECT setval(pg_get_serial_sequence(" + "'" + table_name + "'" + ",'id'), 1, false);")



##############
#  LANGUAGE  #
##############

clearTable(Language)
data = loadData('languages.csv')

for index, info in enumerate(data):
  if index > 0:

    language = Language (
        id = int(info[0]),
        iso639 = info[1],
        iso3166 = info[2],
        name = info[3],
        official = bool(info[4]),
        order = info[5],
      )

    language.save()


clearTable(LanguageName)
data = loadData('language_names.csv')

for index, info in enumerate(data):
  if index > 0:

    languageName = LanguageName (
        language = Language.objects.get(pk = int(info[0])),
        local_language_id = int(info[1]),
        name = info[2]
      )

    languageName.save()



############
#  REGION  #
############

clearTable(Region)
data = loadData('regions.csv')

for index, info in enumerate(data):
  if index > 0:

    model = Region (
        id = int(info[0]),
        name = info[1]
      )
    model.save()


clearTable(RegionName)
data = loadData('region_names.csv')

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

clearTable(Generation)
data = loadData('generations.csv')

for index, info in enumerate(data):
  if index > 0:

    model = Generation (
        id = int(info[0]),
        region = Region.objects.get(pk = int(info[1])),
        name = info[2]
      )
    model.save()


clearTable(GenerationName)
data = loadData('generation_names.csv')

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

clearTable(VersionGroup)
data = loadData('version_groups.csv')

for index, info in enumerate(data):
  if index > 0:

    versionGroup = VersionGroup (
        id = int(info[0]),
        name = info[1],
        generation = Generation.objects.get(pk = int(info[2])),
        order = int(info[3])
      )
    versionGroup.save()


clearTable(VersionGroupRegion)
data = loadData('version_group_regions.csv')

for index, info in enumerate(data):
  if index > 0:

    versionGroupRegion = VersionGroupRegion (
        version_group = VersionGroup.objects.get(pk = int(info[0])),
        region = Region.objects.get(pk = int(info[1])),
      )
    versionGroupRegion.save()


clearTable(Version)
data = loadData('versions.csv')

for index, info in enumerate(data):
  if index > 0:

    version = Version (
        id = int(info[0]),
        version_group = VersionGroup.objects.get(pk = int(info[1])),
        name = info[2]
      )
    version.save()


clearTable(VersionName)
data = loadData('version_names.csv')

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

clearTable(MoveDamageClass)
data = loadData('move_damage_classes.csv')

for index, info in enumerate(data):
  if index > 0:

    model = MoveDamageClass (
        id = int(info[0]),
        name = info[1]
      )
    model.save()


clearTable(MoveDamageClassDescription)
data = loadData('move_damage_class_prose.csv')

for index, info in enumerate(data):
  if index > 0:

    model = MoveDamageClassDescription (
        move_damage_class = MoveDamageClass.objects.get(pk = int(info[0])),
        language = Language.objects.get(pk = int(info[1])),
        description = info[2]
      )
    model.save()


###########
#  STATS  #
###########

clearTable(Stat)
data = loadData('stats.csv')

for index, info in enumerate(data):
  if index > 0:

    stat = Stat (
        id = int(info[0]),
        move_damage_class = MoveDamageClass.objects.get(pk = int(info[1])) if info[1] != '' else None,
        name = info[2],
        is_battle_only = bool(info[3]),
        game_index = int(info[4]) if info[4] else 0,
      )
    stat.save()


clearTable(StatName)
data = loadData('stat_names.csv')

for index, info in enumerate(data):
  if index > 0:

    statName = StatName (
        stat = Stat.objects.get(pk = int(info[0])),
        language = Language.objects.get(pk = int(info[1])),
        name = info[2]
      )
    statName.save()


clearTable(PokeathlonStat)
data = loadData('pokeathlon_stats.csv')

for index, info in enumerate(data):
  if index > 0:

    stat = PokeathlonStat (
        id = int(info[0]),
        name = info[1],
      )
    stat.save()


clearTable(PokeathlonStatName)
data = loadData('pokeathlon_stat_names.csv')

for index, info in enumerate(data):
  if index > 0:

    statName = PokeathlonStatName (
        pokeathlon_stat = PokeathlonStat.objects.get(pk = int(info[0])),
        language = Language.objects.get(pk = int(info[1])),
        name = info[2]
      )
    statName.save()




###############
#  ABILITIES  #
###############

clearTable(Ability)
data = loadData('abilities.csv')

for index, info in enumerate(data):
  if index > 0:

    ability = Ability (
        id = int(info[0]),
        name = info[1],
        generation = Generation.objects.get(pk = int(info[2])),
        is_main_series = bool(info[3])
      )
    ability.save()


clearTable(AbilityName)
data = loadData('ability_names.csv')

for index, info in enumerate(data):
  if index > 0:

    abilityName = AbilityName (
        ability = Ability.objects.get(pk = int(info[0])),
        language = Language.objects.get(pk = int(info[1])),
        name = info[2]
      )
    abilityName.save()


clearTable(AbilityDescription)
data = loadData('ability_prose.csv')

for index, info in enumerate(data):
  if index > 0:

    abilityDesc = AbilityDescription (
        ability = Ability.objects.get(pk = int(info[0])),
        language = Language.objects.get(pk = int(info[1])),
        short_effect = info[2],
        effect = info[3]
      )
    abilityDesc.save()


clearTable(AbilityFlavorText)
data = loadData('ability_flavor_text.csv')

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

clearTable(Characteristic)
data = loadData('characteristics.csv')

for index, info in enumerate(data):
  if index > 0:

    model = Characteristic (
        id = int(info[0]),
        stat = Stat.objects.get(pk = int(info[1])),
        gene_mod_5 = int(info[2])
      )
    model.save()


clearTable(CharacteristicDescription)
data = loadData('characteristic_text.csv')

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

clearTable(EggGroup)
data = loadData('egg_groups.csv')

for index, info in enumerate(data):
  if index > 0:

    model = EggGroup (
        id = int(info[0]),
        name = info[1]
      )
    model.save()


clearTable(EggGroupName)
data = loadData('egg_group_prose.csv')

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

clearTable(GrowthRate)
data = loadData('growth_rates.csv')

for index, info in enumerate(data):
  if index > 0:

    model = GrowthRate (
        id = int(info[0]),
        name = info[1],
        formula = info[2]
      )
    model.save()


clearTable(GrowthRateDescription)
data = loadData('growth_rate_prose.csv')

for index, info in enumerate(data):
  if index > 0:

    model = GrowthRateDescription (
        growth_rate = GrowthRate.objects.get(pk = int(info[0])),
        language = Language.objects.get(pk = int(info[1])),
        description = info[2]
      )
    model.save()



clearTable(ItemPocket)
data = loadData('item_pockets.csv')

for index, info in enumerate(data):
  if index > 0:

    model = ItemPocket (
        id = int(info[0]),
        name = info[1]
      )
    model.save()


clearTable(ItemPocketName)
data = loadData('item_pocket_names.csv')

for index, info in enumerate(data):
  if index > 0:

    model = ItemPocketName (
        item_pocket = ItemPocket.objects.get(pk = int(info[0])),
        language = Language.objects.get(pk = int(info[1])),
        name = info[2]
      )
    model.save()


clearTable(ItemFlingEffect)
data = loadData('item_fling_effects.csv')

for index, info in enumerate(data):
  if index > 0:

    model = ItemFlingEffect (
        id = int(info[0])
      )
    model.save()


clearTable(ItemFlingEffectDescription)
data = loadData('item_fling_effect_prose.csv')

for index, info in enumerate(data):
  if index > 0:

    model = ItemFlingEffectDescription (
        item_fling_effect = ItemFlingEffect.objects.get(pk = int(info[0])),
        language = Language.objects.get(pk = int(info[1])),
        effect = info[2]
      )
    model.save()


clearTable(ItemCategory)
data = loadData('item_categories.csv')

for index, info in enumerate(data):
  if index > 0:

    model = ItemCategory (
        id = int(info[0]),
        item_pocket = ItemPocket.objects.get(pk = int(info[1])),
        name = info[2]
      )
    model.save()


clearTable(ItemCategoryName)
data = loadData('item_category_prose.csv')

for index, info in enumerate(data):
  if index > 0:

    model = ItemCategoryName (
        item_category = ItemCategory.objects.get(pk = int(info[0])),
        language = Language.objects.get(pk = int(info[1])),
        name = info[2]
      )
    model.save()


clearTable(Item)
data = loadData('items.csv')

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


clearTable(ItemName)
data = loadData('item_names.csv')

for index, info in enumerate(data):
  if index > 0:

    model = ItemName (
        item = Item.objects.get(pk = int(info[0])),
        language = Language.objects.get(pk = int(info[1])),
        name = info[2]
      )
    model.save()


clearTable(ItemDescription)
data = loadData('item_prose.csv')

for index, info in enumerate(data):
  if index > 0:

    model = ItemDescription (
        item = Item.objects.get(pk = int(info[0])),
        language = Language.objects.get(pk = int(info[1])),
        short_effect = info[2],
        effect = info[3]
      )
    model.save()


clearTable(ItemGameIndex)
data = loadData('item_game_indices.csv')

for index, info in enumerate(data):
  if index > 0:

    model = ItemGameIndex (
        item = Item.objects.get(pk = int(info[0])),
        generation = Generation.objects.get(pk = int(info[1])),
        game_index = int(info[2])
      )
    model.save()


clearTable(ItemFlavorText)
data = loadData('item_flavor_text.csv')

for index, info in enumerate(data):
  if index > 0:

    model = ItemFlavorText (
        item = Item.objects.get(pk = int(info[0])),
        version_group = VersionGroup.objects.get(pk = int(info[1])),
        language = Language.objects.get(pk = int(info[2])),
        flavor_text = info[3]
      )
    model.save()


clearTable(ItemFlag)
data = loadData('item_flags.csv')

for index, info in enumerate(data):
  if index > 0:

    model = ItemFlag (
        id = int(info[0]),
        name = info[1]
      )
    model.save()


clearTable(ItemFlagDescription)
data = loadData('item_flag_prose.csv')

for index, info in enumerate(data):
  if index > 0:

    model = ItemFlagDescription (
        item_flag = ItemFlag.objects.get(pk = int(info[0])),
        language = Language.objects.get(pk = int(info[1])),
        name = info[2],
        description = info[3]
      )
    model.save()


clearTable(ItemFlagMap)
data = loadData('item_flag_map.csv')

for index, info in enumerate(data):
  if index > 0:

    model = ItemFlagMap (
        item = Item.objects.get(pk = int(info[0])),
        item_flag = ItemFlag.objects.get(pk = int(info[1]))
      )
    model.save()


clearTable(ItemFlagDescription)
data = loadData('item_flag_prose.csv')

for index, info in enumerate(data):
  if index > 0:

    model = ItemFlagDescription (
        item_flag = ItemFlag.objects.get(pk = int(info[0])),
        language = Language.objects.get(pk = int(info[1])),
        name = info[2],
        description = info[3]
      )
    model.save()



###########
#  TYPES  #
###########

clearTable(Type)
data = loadData('types.csv')

for index, info in enumerate(data):
  if index > 0:

    type = Type (
        id = int(info[0]),
        name = info[1],
        generation = Generation.objects.get(pk = int(info[2])),
        move_damage_class = MoveDamageClass.objects.get(pk = int(info[3])) if info[3] != '' else None
      )
    type.save()


clearTable(TypeName)
data = loadData('type_names.csv')

for index, info in enumerate(data):
  if index > 0:

    typeName = TypeName (
        type = Type.objects.get(pk = int(info[0])),
        language = Language.objects.get(pk = int(info[1])),
        name = info[2]
      )
    typeName.save()


clearTable(TypeGameIndex)
data = loadData('type_game_indices.csv')

for index, info in enumerate(data):
  if index > 0:

    typeGameIndex = TypeGameIndex (
        type = Type.objects.get(pk = int(info[0])),
        generation = Generation.objects.get(pk = int(info[1])),
        game_index = int(info[2])
      )
    typeGameIndex.save()


clearTable(TypeEfficacy)
data = loadData('type_efficacy.csv')

for index, info in enumerate(data):
  if index > 0:

    typeEfficacy = TypeEfficacy (
        damage_type_id = int(info[0]),
        target_type_id = int(info[1]),
        damage_factor = int(info[2])
      )
    typeEfficacy.save()



###########
#  MOVES  #
###########

clearTable(MoveEffect)
data = loadData('move_effects.csv')

for index, info in enumerate(data):
  if index > 0:

    model = MoveEffect (
        id = int(info[0])
      )
    model.save()


clearTable(MoveEffectDescription)
data = loadData('move_effect_prose.csv')

for index, info in enumerate(data):
  if index > 0:

    model = MoveEffectDescription (
        move_effect = MoveEffect.objects.get(pk = int(info[1])),
        language = Language.objects.get(pk = int(info[1])),
        short_effect = info[2],
        effect = info[3]
      )
    model.save()


clearTable(MoveEffectChange)
data = loadData('move_effect_changelog.csv')

for index, info in enumerate(data):
  if index > 0:

    model = MoveEffectChange (
        id = int(info[0]),
        move_effect = MoveEffect.objects.get(pk = int(info[1])),
        version_group = VersionGroup.objects.get(pk = int(info[2]))
      )
    model.save()


clearTable(MoveEffectChangeDescription)
data = loadData('move_effect_changelog_prose.csv')

for index, info in enumerate(data):
  if index > 0:

    model = MoveEffectChangeDescription (
        move_effect_change = MoveEffectChange.objects.get(pk = int(info[0])),
        language = Language.objects.get(pk = int(info[1])),
        effect = info[2]
      )
    model.save()


clearTable(MoveTarget)
data = loadData('move_targets.csv')

for index, info in enumerate(data):
  if index > 0:

    model = MoveTarget (
        id = int(info[0]),
        name = info[1]
      )
    model.save()


clearTable(MoveTargetDescription)
data = loadData('move_target_prose.csv')

for index, info in enumerate(data):
  if index > 0:

    model = MoveTargetDescription (
        move_target = MoveTarget.objects.get(pk = int(info[0])),
        language = Language.objects.get(pk = int(info[1])),
        name = info[2],
        description = info[3]
      )
    model.save()


clearTable(Move)
data = loadData('moves.csv')

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

        contest_type_id = int(info[12]) if info[12] != '' else None,

        contest_effect_id = int(info[13]) if info[13] != '' else None,

        super_contest_effect_id = int(info[14]) if info[14] != '' else None
      )
    model.save()


clearTable(MoveName)
data = loadData('move_names.csv')

for index, info in enumerate(data):
  if index > 0:

    model = MoveName (
        move = Move.objects.get(pk = int(info[0])),
        language = Language.objects.get(pk = int(info[1])),
        name = info[2]
      )
    model.save()


clearTable(MoveFlavorText)
data = loadData('move_flavor_text.csv')

for index, info in enumerate(data):
  if index > 0:

    model = MoveFlavorText (
        move = Move.objects.get(pk = int(info[0])),
        version_group = VersionGroup.objects.get(pk = int(info[1])),
        language = Language.objects.get(pk = int(info[2])),
        flavor_text = info[3]
      )
    model.save()


clearTable(MoveChange)
data = loadData('move_changelog.csv')

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


clearTable(MoveBattleStyle)
data = loadData('move_battle_styles.csv')

for index, info in enumerate(data):
  if index > 0:

    model = MoveBattleStyle (
        id = int(info[0]),
        name = info[1]
      )
    model.save()


clearTable(MoveBattleStyleName)
data = loadData('move_battle_style_prose.csv')

for index, info in enumerate(data):
  if index > 0:

    model = MoveBattleStyleName (
        move_battle_style = MoveBattleStyle.objects.get(pk = int(info[0])),
        language = Language.objects.get(pk = int(info[1])),
        name = info[2]
      )
    model.save()


clearTable(MoveFlag)
data = loadData('move_flags.csv')

for index, info in enumerate(data):
  if index > 0:

    model = MoveFlag (
        id = int(info[0]),
        name = info[1]
      )
    model.save()


clearTable(MoveFlagMap)
data = loadData('move_flag_map.csv')

for index, info in enumerate(data):
  if index > 0:

    model = MoveFlagMap (
        move = Move.objects.get(pk = int(info[0])),
        move_flag = MoveFlag.objects.get(pk = int(info[1])),
      )
    model.save()


clearTable(MoveFlagDescription)
data = loadData('move_flag_prose.csv')

for index, info in enumerate(data):
  if index > 0:

    model = MoveFlagDescription (
        move_flag = MoveFlag.objects.get(pk = int(info[0])),
        language = Language.objects.get(pk = int(info[1])),
        name = info[2],
        description = info[3]
      )
    model.save()


clearTable(MoveMetaAilment)
data = loadData('move_meta_ailments.csv')

for index, info in enumerate(data):
  if index > 0:

    model = MoveMetaAilment (
        id = int(info[0]),
        name = info[1]
      )
    model.save()


clearTable(MoveMetaAilmentName)
data = loadData('move_meta_ailment_names.csv')

for index, info in enumerate(data):
  if index > 0:

    model = MoveMetaAilmentName (
        move_meta_ailment = MoveMetaAilment.objects.get(pk = int(info[0])),
        language = Language.objects.get(pk = int(info[1])),
        name = info[2]
      )
    model.save()


clearTable(MoveMetaCategory)
data = loadData('move_meta_categories.csv')

for index, info in enumerate(data):
  if index > 0:

    model = MoveMetaCategory (
        id = int(info[0]),
        name = info[1]
      )
    model.save()


clearTable(MoveMetaCategoryDescription)
data = loadData('move_meta_category_prose.csv')

for index, info in enumerate(data):
  if index > 0:

    model = MoveMetaCategoryDescription (
        move_meta_category = MoveMetaCategory.objects.get(pk = int(info[0])),
        language = Language.objects.get(pk = int(info[1])),
        description = info[2]
      )
    model.save()


clearTable(MoveMeta)
data = loadData('move_meta.csv')

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


clearTable(MoveMetaStatChange)
data = loadData('move_meta_stat_changes.csv')

for index, info in enumerate(data):
  if index > 0:

    model = MoveMetaStatChange (
        move = Move.objects.get(pk = int(info[0])),
        stat = Stat.objects.get(pk = int(info[1])),
        change = int(info[2])
      )
    model.save()



#############
#  CONTEST  #
#############

clearTable(ContestType)
data = loadData('contest_types.csv')

for index, info in enumerate(data):
  if index > 0:

    model = ContestType (
        id = int(info[0]),
        name = info[1]
      )
    model.save()


clearTable(ContestTypeName)
data = loadData('contest_type_names.csv')

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


clearTable(ContestEffect)
data = loadData('contest_effects.csv')

for index, info in enumerate(data):
  if index > 0:

    model = ContestEffect (
        id = int(info[0]),
        appeal = int(info[1]),
        jam = int(info[2])
      )
    model.save()


clearTable(ContestEffectDescription)
data = loadData('contest_effect_prose.csv')

for index, info in enumerate(data):
  if index > 0:

    model = ContestEffectDescription (
        contest_effect = ContestEffect.objects.get(pk = int(info[0])),
        language = Language.objects.get(pk = int(info[1])),
        flavor_text = info[2],
        effect = info[3]
      )
    model.save()


clearTable(ContestCombo)
data = loadData('contest_combos.csv')

for index, info in enumerate(data):
  if index > 0:

    model = ContestCombo (
        first_move = Move.objects.get(pk = int(info[0])),
        second_move = Move.objects.get(pk = int(info[1]))
      )
    model.save()


clearTable(SuperContestEffect)
data = loadData('super_contest_effects.csv')

for index, info in enumerate(data):
  if index > 0:

    model = SuperContestEffect (
        id = int(info[0]),
        appeal = int(info[1])
      )
    model.save()


clearTable(SuperContestEffectDescription)
data = loadData('super_contest_effect_prose.csv')

for index, info in enumerate(data):
  if index > 0:

    model = SuperContestEffectDescription (
        super_contest_effect = SuperContestEffect.objects.get(pk = int(info[0])),
        language = Language.objects.get(pk = int(info[1])),
        flavor_text = info[2]
      )
    model.save()


clearTable(SuperContestCombo)
data = loadData('super_contest_combos.csv')

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

clearTable(BerryFirmness)
data = loadData('berry_firmness.csv')

for index, info in enumerate(data):
  if index > 0:

    model = BerryFirmness (
        id = int(info[0]),
        name = info[1]
      )
    model.save()


clearTable(BerryFirmnessName)
data = loadData('berry_firmness_names.csv')

for index, info in enumerate(data):
  if index > 0:

    model = BerryFirmnessName (
        berry_firmness = BerryFirmness.objects.get(pk = int(info[0])),
        language = Language.objects.get(pk = int(info[1])),
        name = info[2]
      )
    model.save()


clearTable(Berry)
data = loadData('berries.csv')

for index, info in enumerate(data):
  if index > 0:

    model = Berry (
        id = int(info[0]),
        item = Item.objects.get(pk = int(info[1])),
        berry_firmness = BerryFirmness.objects.get(pk = int(info[2])),
        natural_gift_power = int(info[3]),
        nature = None,
        size = int(info[5]),
        max_harvest = int(info[6]),
        growth_time = int(info[7]),
        soil_dryness = int(info[8]),
        smoothness = int(info[9])
      )
    model.save()


clearTable(BerryFlavor)
data = loadData('berry_flavors.csv')

for index, info in enumerate(data):
  if index > 0:

    model = BerryFlavor (
        berry = Berry.objects.get(pk = int(info[0])),
        contest_type = ContestType.objects.get(pk = int(info[1])),
        flavor = int(info[2])
      )
    model.save()



############
#  NATURE  #
############

clearTable(Nature)
data = loadData('natures.csv')

for index, info in enumerate(data):
  if index > 0:

    nature = Nature (
        id = int(info[0]),
        name = info[1],
        decreased_stat_id = Stat.objects.get(pk = int(info[2])),
        increased_stat_id = Stat.objects.get(pk = int(info[3])),
        hates_flavor_id = BerryFlavor.objects.get(pk = int(info[4])),
        likes_flavor_id = BerryFlavor.objects.get(pk = int(info[5])),
        game_index = info[6]
      )
    nature.save()


#Berry/Nature associations
data = loadData('berries.csv')

for index, info in enumerate(data):
  if index > 0:

    berry = Berry.objects.get(pk = int(info[0]))
    berry.nature = Nature.objects.get(pk = int(info[4]))
    berry.save()


clearTable(NatureName)
data = loadData('nature_names.csv')

for index, info in enumerate(data):
  if index > 0:

    natureName = NatureName (
        nature = Nature.objects.get(pk = int(info[0])),
        language = Language.objects.get(pk = int(info[1])),
        name = info[2]
      )
    natureName.save()


clearTable(NaturePokeathlonStat)
data = loadData('nature_pokeathlon_stats.csv')

for index, info in enumerate(data):
  if index > 0:

    naturePokeathlonStat = NaturePokeathlonStat (
        nature = Nature.objects.get(pk = int(info[0])),
        pokeathlon_stat = PokeathlonStat.objects.get(pk = int(info[1])),
        max_change = info[2]
      )
    naturePokeathlonStat.save()


clearTable(NatureBattleStylePreference)
data = loadData('nature_battle_style_preferences.csv')

for index, info in enumerate(data):
  if index > 0:

    model = NatureBattleStylePreference (
        nature = Nature.objects.get(pk = int(info[0])),
        move_battle_style_id = int(info[1]),
        low_hp_preference = info[2],
        high_hp_preference = info[3]
      )
    model.save()



############
#  GENDER  #
############

clearTable(Gender)
data = loadData('genders.csv')

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

clearTable(Experience)
data = loadData('experience.csv')

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

clearTable(Machine)
data = loadData('machines.csv')

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

clearTable(EvolutionChain)
data = loadData('evolution_chains.csv')

for index, info in enumerate(data):
  if index > 0:

    model = EvolutionChain (
        id = int(info[0]),
        baby_evolution_item = Item.objects.get(pk = int(info[1])) if info[1] != '' else None,
      )
    model.save()


clearTable(EvolutionTrigger)
data = loadData('evolution_triggers.csv')

for index, info in enumerate(data):
  if index > 0:

    model = EvolutionTrigger (
        id = int(info[0]),
        name = info[1]
      )
    model.save()


clearTable(EvolutionTriggerName)
data = loadData('evolution_trigger_prose.csv')

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

clearTable(Pokedex)
data = loadData('pokedexes.csv')

for index, info in enumerate(data):
  if index > 0:

    model = Pokedex (
        id = int(info[0]),
        region = Region.objects.get(pk = int(info[1])) if info[1] != '' else None,
        name = info[2],
        is_main_series = bool(info[3])
      )
    model.save()


clearTable(PokedexDescription)
data = loadData('pokedex_prose.csv')

for index, info in enumerate(data):
  if index > 0:

    model = PokedexDescription (
        pokedex = Pokedex.objects.get(pk = int(info[0])),
        language = Language.objects.get(pk = int(info[1])),
        name = info[2],
        description = info[3]
      )
    model.save()


clearTable(PokedexVersionGroup)
data = loadData('pokedex_version_groups.csv')

for index, info in enumerate(data):
  if index > 0:

    model = PokedexVersionGroup (
        pokedex = Pokedex.objects.get(pk = int(info[0])),
        version_group = VersionGroup.objects.get(pk = int(info[1]))
      )
    model.save()



#############
#  POKEMON  #
#############

clearTable(PokemonColor)
data = loadData('pokemon_colors.csv')

for index, info in enumerate(data):
  if index > 0:

    model = PokemonColor (
        id = int(info[0]),
        name = info[1]
      )
    model.save()


clearTable(PokemonColorName)
data = loadData('pokemon_color_names.csv')

for index, info in enumerate(data):
  if index > 0:

    model = PokemonColorName (
        pokemon_color = PokemonColor.objects.get(pk = int(info[0])),
        language = Language.objects.get(pk = int(info[1])),
        name = info[2]
      )
    model.save()


clearTable(PokemonShape)
data = loadData('pokemon_shapes.csv')

for index, info in enumerate(data):
  if index > 0:

    model = PokemonShape (
        id = int(info[0]),
        name = info[1]
      )
    model.save()


clearTable(PokemonShapeName)
data = loadData('pokemon_shape_prose.csv')

for index, info in enumerate(data):
  if index > 0:

    model = PokemonShapeName (
        pokemon_shape = PokemonShape.objects.get(pk = int(info[0])),
        language = Language.objects.get(pk = int(info[1])),
        name = info[2],
        awesome_name = info[3]
      )
    model.save()


clearTable(PokemonHabitat)
data = loadData('pokemon_habitats.csv')

for index, info in enumerate(data):
  if index > 0:

    model = PokemonHabitat (
        id = int(info[0]),
        name = info[1]
      )
    model.save()


clearTable(PokemonSpecies)
data = loadData('pokemon_species.csv')

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
        is_baby = bool(info[11]),
        hatch_counter = int(info[12]),
        has_gender_differences = bool(info[13]),
        growth_rate = GrowthRate.objects.get(pk = int(info[14])),
        forms_switchable = bool(info[15]),
        order = int(info[16])
      )
    model.save()

data = loadData('pokemon_species.csv')

for index, info in enumerate(data):
  if index > 0:

    evolves = PokemonSpecies.objects.get(pk = int(info[3])) if info[3] != '' else None

    if evolves:
      species = PokemonSpecies.objects.get(pk = int(info[0]))
      species.evolves_from_species = evolves
      species.save()


clearTable(PokemonSpeciesName)
data = loadData('pokemon_species_names.csv')

for index, info in enumerate(data):
  if index > 0:

    model = PokemonSpeciesName (
        pokemon_species = PokemonSpecies.objects.get(pk = int(info[0])),
        language = Language.objects.get(pk = int(info[1])),
        name = info[2],
        genus = info[3]
      )
    model.save()


clearTable(PokemonSpeciesDescription)
data = loadData('pokemon_species_prose.csv')

for index, info in enumerate(data):
  if index > 0:

    model = PokemonSpeciesDescription (
        pokemon_species = PokemonSpecies.objects.get(pk = int(info[0])),
        language = Language.objects.get(pk = int(info[1])),
        description = info[2]
      )
    model.save()


clearTable(PokemonSpeciesFlavorText)
data = loadData('pokemon_species_flavor_text.csv')

for index, info in enumerate(data):
  if index > 0:

    model = PokemonSpeciesFlavorText (
        pokemon_species = PokemonSpecies.objects.get(pk = int(info[0])),
        version = Version.objects.get(pk = int(info[1])),
        language = Language.objects.get(pk = int(info[2])),
        flavor_text = info[3]
      )
    model.save()


clearTable(Pokemon)
data = loadData('pokemon.csv')

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
        is_default = bool(info[7])
      )
    model.save()


clearTable(PokemonAbility)
data = loadData('pokemon_abilities.csv')

for index, info in enumerate(data):
  if index > 0:

    model = PokemonAbility (
        pokemon = Pokemon.objects.get(pk = int(info[0])),
        ability = Ability.objects.get(pk = int(info[1])),
        is_hidden = bool(info[2]),
        slot = int(info[3])
      )
    model.save()


clearTable(PokemonDexNumber)
data = loadData('pokemon_dex_numbers.csv')

for index, info in enumerate(data):
  if index > 0:

    model = PokemonDexNumber (
        pokemon_species = PokemonSpecies.objects.get(pk = int(info[0])),
        pokedex = Pokedex.objects.get(pk = int(info[1])),
        pokedex_number = int(info[2])
      )
    model.save()


clearTable(PokemonEggGroup)
data = loadData('pokemon_egg_groups.csv')

for index, info in enumerate(data):
  if index > 0:

    model = PokemonEggGroup (
        pokemon_species = PokemonSpecies.objects.get(pk = int(info[0])),
        egg_group = EggGroup.objects.get(pk = int(info[1]))
      )
    model.save()


clearTable(PokemonEvolution)
data = loadData('pokemon_evolution.csv')

for index, info in enumerate(data):
  if index > 0:

    model = PokemonEvolution (
        id = int(info[0]),
        evolved_species = PokemonSpecies.objects.get(pk = int(info[1])),
        evolution_trigger = EvolutionTrigger.objects.get(pk = int(info[2])),
        evolution_item = Item.objects.get(pk = int(info[3])) if info[3] != '' else None,
        min_level = int(info[4]) if info[4] != '' else None,
        gender = Gender.objects.get(pk = int(info[5])) if info[5] != '' else None,
        location_id = int(info[6]) if info[6] != '' else None,
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
        needs_overworld_rain = bool(info[18]),
        turn_upside_down = bool(info[19])
      )
    model.save()


clearTable(PokemonForm)
data = loadData('pokemon_forms.csv')

for index, info in enumerate(data):
  if index > 0:

    model = PokemonForm (
        id = int(info[0]),
        name = info[1],
        form_identifier = info[2],
        pokemon = Pokemon.objects.get(pk = int(info[3])),
        introduced_in_version_group = VersionGroup.objects.get(pk = int(info[4])),
        is_default = bool(info[5]),
        is_battle_only = bool(info[6]),
        is_mega = bool(info[7]),
        form_order = int(info[8]),
        order = int(info[9])
      )
    model.save()


clearTable(PokemonFormName)
data = loadData('pokemon_form_names.csv')

for index, info in enumerate(data):
  if index > 0:

    model = PokemonFormName (
        pokemon_form = PokemonForm.objects.get(pk = int(info[0])),
        language = Language.objects.get(pk = int(info[1])),
        name = info[2],
        pokemon_name = info[3]
      )
    model.save()


clearTable(PokemonFormGeneration)
data = loadData('pokemon_form_generations.csv')

for index, info in enumerate(data):
  if index > 0:

    model = PokemonFormGeneration (
        pokemon_form = PokemonForm.objects.get(pk = int(info[0])),
        generation = Generation.objects.get(pk = int(info[1])),
        game_index = int(info[2])
      )
    model.save()


clearTable(PokemonGameIndex)
data = loadData('pokemon_game_indices.csv')

for index, info in enumerate(data):
  if index > 0:

    model = PokemonGameIndex (
        pokemon = Pokemon.objects.get(pk = int(info[0])),
        version = Version.objects.get(pk = int(info[1])),
        game_index = int(info[2])
      )
    model.save()


clearTable(PokemonGameIndex)
data = loadData('pokemon_game_indices.csv')

for index, info in enumerate(data):
  if index > 0:

    model = PokemonGameIndex (
        pokemon = Pokemon.objects.get(pk = int(info[0])),
        version = Version.objects.get(pk = int(info[1])),
        game_index = int(info[2])
      )
    model.save()


clearTable(PokemonHabitatName)
data = loadData('pokemon_habitat_names.csv')

for index, info in enumerate(data):
  if index > 0:

    model = PokemonHabitatName (
        pokemon_habitat = PokemonHabitat.objects.get(pk = int(info[0])),
        language = Language.objects.get(pk = int(info[1])),
        name = info[2]
      )
    model.save()


clearTable(PokemonItem)
data = loadData('pokemon_items.csv')

for index, info in enumerate(data):
  if index > 0:

    model = PokemonItem (
        pokemon = Pokemon.objects.get(pk = int(info[0])),
        version = Version.objects.get(pk = int(info[1])),
        item = Item.objects.get(pk = int(info[2])),
        rarity = int(info[3])
      )
    model.save()


clearTable(PokemonMoveMethod)
data = loadData('pokemon_move_methods.csv')

for index, info in enumerate(data):
  if index > 0:

    model = PokemonMoveMethod (
        id = int(info[0]),
        name = info[1]
      )
    model.save()


clearTable(PokemonMoveMethodName)
data = loadData('pokemon_move_method_prose.csv')

for index, info in enumerate(data):
  if index > 0:

    model = PokemonMoveMethodName (
        pokemon_move_method = PokemonMoveMethod.objects.get(pk = int(info[0])),
        language = Language.objects.get(pk = int(info[1])),
        name = info[2],
        description = info[3]
      )
    model.save()


clearTable(PokemonMove)
data = loadData('pokemon_moves.csv')

for index, info in enumerate(data):
  if index > 0:

    model = PokemonMove (
        pokemon = Pokemon.objects.get(pk = int(info[0])),
        version_group = VersionGroup.objects.get(pk = int(info[1])),
        move = Move.objects.get(pk = int(info[2])),
        pokemon_move_method = PokemonMoveMethod.objects.get(pk = int(info[3])),
        level = int(info[4]),
        order = int(info[5]) if info[5] != '' else None,
      )
    model.save()


clearTable(PokemonStat)
data = loadData('pokemon_stats.csv')

for index, info in enumerate(data):
  if index > 0:

    model = PokemonStat (
        pokemon = Pokemon.objects.get(pk = int(info[0])),
        stat = Stat.objects.get(pk = int(info[1])),
        base_stat = int(info[2]),
        effort = int(info[3])
      )
    model.save()


clearTable(PokemonType)
data = loadData('pokemon_types.csv')

for index, info in enumerate(data):
  if index > 0:

    model = PokemonType (
        pokemon = Pokemon.objects.get(pk = int(info[0])),
        type = Type.objects.get(pk = int(info[1])),
        slot = int(info[2])
      )
    model.save()



##############
# ENCOUNTER  #
##############

clearTable(Location)
data = loadData('locations.csv')

for index, info in enumerate(data):
  if index > 0:

    model = Location (
        id = int(info[0]),
        region = Region.objects.get(pk = int(info[1])) if info[1] != '' else None,
        name = info[2]
      )
    model.save()


clearTable(LocationName)
data = loadData('location_names.csv')

for index, info in enumerate(data):
  if index > 0:

    model = LocationName (
        location = Location.objects.get(pk = int(info[0])),
        language = Language.objects.get(pk = int(info[1])),
        name = info[2]
      )
    model.save()


clearTable(LocationGameIndex)
data = loadData('location_game_indices.csv')

for index, info in enumerate(data):
  if index > 0:

    model = LocationGameIndex (
        location = Location.objects.get(pk = int(info[0])),
        generation = Generation.objects.get(pk = int(info[1])),
        game_index = int(info[2])
      )
    model.save()


clearTable(LocationArea)
data = loadData('location_areas.csv')

for index, info in enumerate(data):
  if index > 0:

    model = LocationArea (
        id = int(info[0]),
        location = Location.objects.get(pk = int(info[1])),
        game_index = int(info[2]),
        name = info[3]
      )
    model.save()


clearTable(LocationAreaName)
data = loadData('location_area_prose.csv')

for index, info in enumerate(data):
  if index > 0:

    model = LocationAreaName (
        location_area = LocationArea.objects.get(pk = int(info[0])),
        language = Language.objects.get(pk = int(info[1])),
        name = info[2]
      )
    model.save()


clearTable(LocationAreaEncounterRate)
data = loadData('location_area_encounter_rates.csv')

for index, info in enumerate(data):
  if index > 0:

    model = LocationAreaEncounterRate (
        location_area = LocationArea.objects.get(pk = int(info[0])),
        encounter_method = None,
        version = Version.objects.get(pk = int(info[2])),
        rate = int(info[3])
      )
    model.save()



###############
#  ENCOUNTER  #
###############

clearTable(EncounterMethod)
data = loadData('encounter_methods.csv')

for index, info in enumerate(data):
  if index > 0:

    model = EncounterMethod (
        id = int(info[0]),
        name = info[1],
        order = int(info[2])
      )
    model.save()


clearTable(EncounterMethodName)
data = loadData('encounter_method_prose.csv')

for index, info in enumerate(data):
  if index > 0:

    model = EncounterMethodName (
        encounter_method = EncounterMethod.objects.get(pk = int(info[0])),
        language = Language.objects.get(pk = int(info[1])),
        name = info[2]
      )
    model.save()


clearTable(EncounterSlot)
data = loadData('encounter_slots.csv')

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


clearTable(EncounterCondition)
data = loadData('encounter_conditions.csv')

for index, info in enumerate(data):
  if index > 0:

    model = EncounterCondition (
        id = int(info[0]),
        name = info[1]
      )
    model.save()


clearTable(EncounterConditionName)
data = loadData('encounter_condition_prose.csv')

for index, info in enumerate(data):
  if index > 0:

    model = EncounterConditionName (
        encounter_condition = EncounterCondition.objects.get(pk = int(info[0])),
        language = Language.objects.get(pk = int(info[1])),
        name = info[2]
      )
    model.save()


clearTable(Encounter)
data = loadData('encounters.csv')

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


clearTable(EncounterConditionValue)
data = loadData('encounter_condition_values.csv')

for index, info in enumerate(data):
  if index > 0:

    model = EncounterConditionValue (
        id = int(info[0]),
        encounter_condition = EncounterCondition.objects.get(pk = int(info[1])),
        name = info[2],
        is_default = bool(info[3])
      )
    model.save()


clearTable(EncounterConditionValueName)
data = loadData('encounter_condition_value_prose.csv')

for index, info in enumerate(data):
  if index > 0:

    model = EncounterConditionValueName (
        encounter_condition_value = EncounterConditionValue.objects.get(pk = int(info[0])),
        language = Language.objects.get(pk = int(info[1])),
        name = info[2],
      )
    model.save()


clearTable(EncounterConditionValueMap)
data = loadData('encounter_condition_value_map.csv')

for index, info in enumerate(data):
  if index > 0:

    model = EncounterConditionValueMap (
        encounter = Encounter.objects.get(pk = int(info[0])),
        encounter_condition_value = EncounterConditionValue.objects.get(pk = int(info[1]))
      )
    model.save()


#Location/Encounter associations
data = loadData('location_area_encounter_rates.csv')

for index, info in enumerate(data):
  if index > 0:

    laer = LocationAreaEncounterRate.objects.get(pk = int(info[0]))
    laer.encounter_method = EncounterMethod.objects.get(pk = int(info[1]))
    laer.save()



##############
#  PAL PARK  #
##############

clearTable(PalParkArea)
data = loadData('pal_park_areas.csv')

for index, info in enumerate(data):
  if index > 0:

    model = PalParkArea (
        id = int(info[0]),
        name = info[1]
      )
    model.save()


clearTable(PalParkAreaName)
data = loadData('pal_park_area_names.csv')

for index, info in enumerate(data):
  if index > 0:

    model = PalParkAreaName (
        pal_park_area = PalParkArea.objects.get(pk = int(info[0])),
        language = Language.objects.get(pk = int(info[1])),
        name = info[2]
      )
    model.save()


clearTable(PalPark)
data = loadData('pal_park.csv')

for index, info in enumerate(data):
  if index > 0:

    model = PalPark (
        pokemon_species = PokemonSpecies.objects.get(pk = int(info[0])),
        pal_park_area = PalParkArea.objects.get(pk = int(info[1])),
        rate = int(info[2])
      )
    model.save()
