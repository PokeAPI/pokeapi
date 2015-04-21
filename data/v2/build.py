import csv
import os

from django.db import migrations

from pokemon_v2.models import *


data_location = 'data/v2/csv/'

# migrations.RunSQL('INSERT INTO pokemon_v2_statname VALUES name=banana')


def loadData(fileName):
  return csv.reader(open(data_location + fileName, 'rb'), delimiter=',')

def clearTable(model):
  print str(model)
  model.objects.all().delete()

def parseNumber(num):
  try:
      result = int(num)
  except ValueError:
      result = ''

  return result


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
        language = Language.objects.get(id = int(info[0])),
        local_language_id = int(info[1]),
        name = info[2]
      )

    languageName.save()


################
#  GENERATION  #
################

clearTable(Generation)
data = loadData('generations.csv')

for index, info in enumerate(data):
  if index > 0:

    generation = Generation (
        id = int(info[0]),
        main_region_id = info[1],
        name = info[2]
      )
    generation.save()


clearTable(GenerationName)
data = loadData('generation_names.csv')

for index, info in enumerate(data):
  if index > 0:

    generationName = GenerationName (
        generation = Generation.objects.get(id = int(info[0])),
        language = Language.objects.get(id = int(info[1])),
        name = info[2]
      )
    generationName.save()



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
        generation = Generation.objects.get(id = int(info[2])),
        order = int(info[3])
      )
    versionGroup.save()


clearTable(VersionGroupRegion)
data = loadData('version_group_regions.csv')

for index, info in enumerate(data):
  if index > 0:

    versionGroupRegion = VersionGroupRegion (
        version_group = VersionGroup.objects.get(id = int(info[0])),
        region_id = int(info[1])
      )
    versionGroupRegion.save()


clearTable(Version)
data = loadData('versions.csv')

for index, info in enumerate(data):
  if index > 0:

    version = Version (
        id = int(info[0]),
        version_group = VersionGroup.objects.get(id = int(info[1])),
        name = info[2]
      )
    version.save()


clearTable(VersionName)
data = loadData('version_names.csv')

for index, info in enumerate(data):
  if index > 0:

    versionName = VersionName (
        version = Version.objects.get(id = int(info[0])),
        language = Language.objects.get(id = int(info[1])),
        name = info[2]
      )
    versionName.save()



# ##################
# #  DAMAGE CLASS  #
# ##################

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
        move_damage_class = MoveDamageClass.objects.get(id = int(info[0])),
        language = Language.objects.get(id = int(info[1])),
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
        move_damage_class = MoveDamageClass.objects.get(id = int(info[1])) if info[1] != '' else None,
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
        stat = Stat.objects.get(id = int(info[0])),
        language = Language.objects.get(id = int(info[1])),
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
        generation = Generation.objects.get(id = int(info[2])),
        is_main_series = bool(info[3])
      )
    ability.save()


clearTable(AbilityName)
data = loadData('ability_names.csv')

for index, info in enumerate(data):
  if index > 0:

    abilityName = AbilityName (
        ability = Ability.objects.get(id = int(info[0])),
        language = Language.objects.get(id = int(info[1])),
        name = info[2]
      )
    abilityName.save()


clearTable(AbilityDescription)
data = loadData('ability_prose.csv')

for index, info in enumerate(data):
  if index > 0:

    abilityDesc = AbilityDescription (
        ability = Ability.objects.get(id = int(info[0])),
        language = Language.objects.get(id = int(info[1])),
        short_effect = info[2],
        effect = info[3]
      )
    abilityDesc.save()


clearTable(AbilityFlavorText)
data = loadData('ability_flavor_text.csv')

for index, info in enumerate(data):
  if index > 0:

    abilityFlavorText = AbilityFlavorText (
        ability = Ability.objects.get(id = int(info[0])),
        version_group = VersionGroup.objects.get(id = int(info[1])),
        language = Language.objects.get(id = int(info[2])),
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
        stat = Stat.objects.get(id = int(info[1])),
        gene_mod_5 = int(info[2])
      )
    model.save()


clearTable(CharacteristicDescription)
data = loadData('characteristic_text.csv')

for index, info in enumerate(data):
  if index > 0:

    model = CharacteristicDescription (
        characteristic = Characteristic.objects.get(id = int(info[0])),
        language = Language.objects.get(id = int(info[1])),
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
        egg_group = EggGroup.objects.get(id = int(info[0])),
        language = Language.objects.get(id = int(info[1])),
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
        growth_rate = GrowthRate.objects.get(id = int(info[0])),
        language = Language.objects.get(id = int(info[1])),
        description = info[2]
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
        decreased_stat_id = Stat.objects.get(id = int(info[2])),
        increased_stat_id = Stat.objects.get(id = int(info[3])),
        hates_flavor_id = info[4],
        likes_flavor_id = info[5],
        game_index = info[6]
      )
    nature.save()


clearTable(NatureName)
data = loadData('nature_names.csv')

for index, info in enumerate(data):
  if index > 0:

    natureName = NatureName (
        nature = Nature.objects.get(id = int(info[0])),
        language = Language.objects.get(id = int(info[1])),
        name = info[2]
      )
    natureName.save()


clearTable(NaturePokeathlonStat)
data = loadData('nature_pokeathlon_stats.csv')

for index, info in enumerate(data):
  if index > 0:

    naturePokeathlonStat = NaturePokeathlonStat (
        nature = Nature.objects.get(id = int(info[0])),
        pokeathlon_stat_id = Stat.objects.get(id = int(info[1])),
        max_change = info[2]
      )
    naturePokeathlonStat.save()


clearTable(NatureBattleStylePreference)
data = loadData('nature_battle_style_preferences.csv')

for index, info in enumerate(data):
  if index > 0:

    model = NatureBattleStylePreference (
        nature = Nature.objects.get(id = int(info[0])),
        move_battle_style_id = int(info[1]),
        low_hp_preference = info[2],
        high_hp_preference = info[3]
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
        generation = Generation.objects.get(id = int(info[2])),
        move_damage_class = MoveDamageClass.objects.get(id = int(info[3])) if info[3] != '' else None
      )
    type.save()


clearTable(TypeName)
data = loadData('type_names.csv')

for index, info in enumerate(data):
  if index > 0:

    typeName = TypeName (
        type = Type.objects.get(id = int(info[0])),
        language = Language.objects.get(id = int(info[1])),
        name = info[2]
      )
    typeName.save()


clearTable(TypeGameIndex)
data = loadData('type_game_indices.csv')

for index, info in enumerate(data):
  if index > 0:

    typeGameIndex = TypeGameIndex (
        type = Type.objects.get(id = int(info[0])),
        generation = Generation.objects.get(id = int(info[1])),
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



# ###########
# #  MOVES  #
# ###########

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
        move_effect = MoveEffect.objects.get(id = int(info[1])),
        language = Language.objects.get(id = int(info[1])),
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
        move_effect = MoveEffect.objects.get(id = int(info[1])),
        version_group = VersionGroup.objects.get(id = int(info[2]))
      )
    model.save()


clearTable(MoveEffectChangeDescription)
data = loadData('move_effect_changelog_prose.csv')

for index, info in enumerate(data):
  if index > 0:

    model = MoveEffectChangeDescription (
        move_effect_change = MoveEffectChange.objects.get(id = int(info[0])),
        language = Language.objects.get(id = int(info[1])),
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
        move_target = MoveTarget.objects.get(id = int(info[0])),
        language = Language.objects.get(id = int(info[1])),
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
        generation = Generation.objects.get(id = int(info[2])),
        type = Type.objects.get(id = int(info[3])),

        power = int(info[4]) if info[4] != '' else None,

        pp = int(info[5]) if info[5] != '' else None,

        accuracy = int(info[6]) if info[6] != '' else None,

        priority = int(info[7]) if info[7] != '' else None,

        move_target = MoveTarget.objects.get(id = int(info[8])),
        move_damage_class = MoveDamageClass.objects.get(id = int(info[9])),
        move_effect = MoveEffect.objects.get(id = int(info[10])),

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
        move = Move.objects.get(id = int(info[0])),
        language = Language.objects.get(id = int(info[1])),
        name = info[2]
      )
    model.save()


clearTable(MoveFlavorText)
data = loadData('move_flavor_text.csv')

for index, info in enumerate(data):
  if index > 0:

    model = MoveFlavorText (
        move = Move.objects.get(id = int(info[0])),
        version_group = VersionGroup.objects.get(id = int(info[1])),
        language = Language.objects.get(id = int(info[2])),
        flavor_text = info[3]
      )
    model.save()


clearTable(MoveChange)
data = loadData('move_changelog.csv')

for index, info in enumerate(data):
  if index > 0:

    model = MoveChange (
        move = Move.objects.get(id = int(info[0])),
        version_group = VersionGroup.objects.get(id = int(info[1])),

        type = Type.objects.get(id = int(info[2])) if info[2] != '' else None,

        power = int(info[3]) if info[3] != '' else None,

        pp = int(info[4]) if info[4] != '' else None,

        accuracy = int(info[5]) if info[5] != '' else None,

        move_effect = MoveEffect.objects.get(id = int(info[6])) if info[6] != '' else None,

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
        move_battle_style = MoveBattleStyle.objects.get(id = int(info[0])),
        language = Language.objects.get(id = int(info[1])),
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
        move = Move.objects.get(id = int(info[0])),
        move_flag = MoveFlag.objects.get(id = int(info[1])),
      )
    model.save()


clearTable(MoveFlagDescription)
data = loadData('move_flag_prose.csv')

for index, info in enumerate(data):
  if index > 0:

    model = MoveFlagDescription (
        move_flag = MoveFlag.objects.get(id = int(info[0])),
        language = Language.objects.get(id = int(info[1])),
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
        move_meta_ailment = MoveMetaAilment.objects.get(id = int(info[0])),
        language = Language.objects.get(id = int(info[1])),
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
        move_meta_category = MoveMetaCategory.objects.get(id = int(info[0])),
        language = Language.objects.get(id = int(info[1])),
        description = info[2]
      )
    model.save()


clearTable(MoveMeta)
data = loadData('move_meta.csv')

for index, info in enumerate(data):
  if index > 0:

    model = MoveMeta (
        move = Move.objects.get(id = int(info[0])),
        move_meta_category = MoveMetaCategory.objects.get(id = int(info[1])),
        move_meta_ailment = MoveMetaAilment.objects.get(id = int(info[2])),
        min_hits = int(info[3]) if info[3] != '' else None,
        max_hits = int(info[4]) if info[4] != '' else None,
        min_turns = int(info[5]) if info[5] != '' else None,
        max_turns = int(info[6]) if info[6] != '' else None,
        drain = int(info[7]) if info[7] != '' else None,
        healing = int(info[8]) if info[8] != '' else None,
        crit_rate = int(info[9]) if info[9] != '' else None,
        ailment_chance = int(info[10]) if info[10] != '' else None,
        flinch_chance = int(info[11]) if info[11] != '' else None,
        stat_chance = int(info[12]) if info[12] != '' else None,
      )
    model.save()


clearTable(MoveMetaStatChange)
data = loadData('move_meta_stat_changes.csv')

for index, info in enumerate(data):
  if index > 0:

    model = MoveMetaStatChange (
        move = Move.objects.get(id = int(info[0])),
        stat = Stat.objects.get(id = int(info[1])),
        change = int(info[2])
      )
    model.save()
