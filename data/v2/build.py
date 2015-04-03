import csv
import os

from pokemon_v2.models import *

###############
#  ABILITIES  #
###############

#  Names  #

file = open('data/v2/csv/ability_names.csv', 'rb')
data = csv.reader(file, delimiter=',')

for index, info in enumerate(data):
  if index > 0:

    abilityName = AbilityName(
        ability_id=int(info[0]),
        local_language_id=int(info[1]),
        name=info[2]
      )
    abilityName.save()


#  Descriptions  #

file = open('data/v2/csv/ability_prose.csv', 'rb')
data = csv.reader(file, delimiter=',')

for index, info in enumerate(data):
  if index > 0:

    abilityDesc = AbilityDescription(
        ability_id=int(info[0]),
        local_language_id=int(info[1]),
        short_effect=info[2],
        effect=info[3]
      )
    abilityDesc.save()
