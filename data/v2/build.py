import csv
import os

from pokemon_v2.models import *


data_location = 'data/v2/csv/'


def loadData(fileName):
  return csv.reader(open(data_location + fileName, 'rb'), delimiter=',')

def clearTable(model):
  model.objects.all().delete()


##############
#  LANGUAGE  #
##############

clearTable(Language)
print str(Language)
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
        language = Language.objects.filter(id = int(info[0]))[0],
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
        generation = Generation.objects.filter(id = int(info[0]))[0],
        language = Language.objects.filter(id = int(info[1]))[0],
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
        generation = Generation.objects.filter(id = int(info[2]))[0],
        order = int(info[3])
      )
    versionGroup.save()


clearTable(VersionGroupRegion)
data = loadData('version_group_regions.csv')

for index, info in enumerate(data):
  if index > 0:

    versionGroupRegion = VersionGroupRegion (
        version_group = VersionGroup.objects.filter(id = int(info[0]))[0],
        region_id = int(info[1])
      )
    versionGroupRegion.save()


clearTable(Version)
data = loadData('versions.csv')

for index, info in enumerate(data):
  if index > 0:

    version = Version (
        id = int(info[0]),
        version_group = VersionGroup.objects.filter(id = int(info[1]))[0],
        name = info[2]
      )
    version.save()


clearTable(VersionName)
data = loadData('version_names.csv')

for index, info in enumerate(data):
  if index > 0:

    versionName = VersionName (
        version = Version.objects.filter(id = int(info[0]))[0],
        language = Language.objects.filter(id = int(info[1]))[0],
        name = info[2]
      )
    versionName.save()


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
        generation = Generation.objects.filter(id = int(info[2]))[0],
        is_main_series = bool(info[3])
      )
    ability.save()


clearTable(AbilityName)
data = loadData('ability_names.csv')

for index, info in enumerate(data):
  if index > 0:

    abilityName = AbilityName (
        ability = Ability.objects.filter(id = int(info[0]))[0],
        language = Language.objects.filter(id = int(info[1]))[0],
        name = info[2]
      )
    abilityName.save()


clearTable(AbilityDescription)
data = loadData('ability_prose.csv')

for index, info in enumerate(data):
  if index > 0:

    abilityDesc = AbilityDescription (
        ability = Ability.objects.filter(id = int(info[0]))[0],
        language = Language.objects.filter(id = int(info[1]))[0],
        short_effect = info[2],
        effect = info[3]
      )
    abilityDesc.save()


clearTable(AbilityFlavorText)
data = loadData('ability_flavor_text.csv')

for index, info in enumerate(data):
  if index > 0:

    abilityFlavorText = AbilityFlavorText (
        ability = Ability.objects.filter(id = int(info[0]))[0],
        version_group = VersionGroup.objects.filter(id = int(info[1]))[0],
        language = Language.objects.filter(id = int(info[2]))[0],
        flavor_text = info[2]
      )
    abilityFlavorText.save()



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
        generation = Generation.objects.filter(id = int(info[2]))[0],
        damage_class_id = int(info[3]) if info[3] else 0
      )
    type.save()


clearTable(TypeName)
data = loadData('type_names.csv')

for index, info in enumerate(data):
  if index > 0:

    typeName = TypeName (
        type = Type.objects.filter(id = int(info[0]))[0],
        language = Language.objects.filter(id = int(info[1]))[0],
        name = info[2]
      )
    typeName.save()


clearTable(TypeGameIndex)
data = loadData('type_game_indices.csv')

for index, info in enumerate(data):
  if index > 0:

    typeGameIndex = TypeGameIndex (
        type = Type.objects.filter(id = int(info[0]))[0],
        generation = Generation.objects.filter(id = int(info[1]))[0],
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
