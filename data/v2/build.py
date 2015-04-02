import csv
import os

from pokemon_v2.models import *

###############
#  ABILITIES  #
###############

file = open('data/v2/csv/ability_names.csv', 'rb')
data = csv.reader(file, delimiter=',')

for index, info in enumerate(data):
  if index > 0:

    abilityName = AbilityName(
        id=int(info[0]),
        ability_id=int(info[1]),
        local_language_id=int(info[2]),
        name=str(info[3]),
      )
    abilityName.save()
    print 'created ' % abilityName.name


# for filename in os.listdir('data/v2/csv'):

#   print filename

  # file = open('csv/ability_names.csv', 'rb')

  # types_reader = csv.reader(file, delimiter=',')

  # for row in types_reader:

  #   new_type = Type(
  #       id = row[0],
  #       name = row[1],
  #       generation_id = row[2],
  #       damage_class_id = row[3]
  #     )

  #   print new_type
