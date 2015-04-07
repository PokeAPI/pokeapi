from __future__ import unicode_literals
from django.db import models


#####################
#  ABSTRACT MODELS  #
#####################

class HasAbility(models.Model):

  ability = models.ForeignKey('Ability', blank=True, null=True)

  class Meta:
       abstract = True

class HasCharacteristic(models.Model):

  characteristic = models.ForeignKey('Characteristic', blank=True, null=True)

  class Meta:
       abstract = True

class HasDamageClass(models.Model):

  damage_class_id = models.IntegerField(blank = True, null = True)

  class Meta:
       abstract = True

class HasEggGroup(models.Model):

  egg_group = models.ForeignKey('EggGroup', blank=True, null=True)

  class Meta:
       abstract = True

class HasGeneration(models.Model):

  generation = models.ForeignKey('Generation', blank=True, null=True)

  class Meta:
       abstract = True

class HasGrowthRate(models.Model):

  growth_rate = models.ForeignKey('GrowthRate', blank=True, null=True)

  class Meta:
       abstract = True

class HasLanguage(models.Model):

  language = models.ForeignKey('Language', blank = True, null = True)

  class Meta:
       abstract = True

class HasName(models.Model):

  name = models.CharField(max_length=30)

  class Meta:
       abstract = True

class HasNature(models.Model):

  nature = models.ForeignKey('Nature', blank=True, null=True)

  class Meta:
       abstract = True

class HasOrder(models.Model):

  order = models.IntegerField()

  class Meta:
       abstract = True

class HasStat(models.Model):

  stat = models.ForeignKey('Stat', blank=True, null=True)

  class Meta:
       abstract = True

class HasType(models.Model):

  type = models.ForeignKey('Type', blank=True, null=True)

  class Meta:
       abstract = True

class HasVersionGroup(models.Model):

  version_group = models.ForeignKey('VersionGroup', blank=True, null=True)

  class Meta:
       abstract = True

class IsName(HasLanguage, HasName):

  class Meta:
       abstract = True


####################
#  VERSION MODELS  #
####################

class Version(HasName, HasVersionGroup):
  pass

class VersionName(IsName):

  version = models.ForeignKey('Version', blank=True, null=True)


class VersionGroup(HasName, HasGeneration, HasOrder):
  pass


class VersionGroupRegion(HasVersionGroup):

  region_id = models.IntegerField()


class VersionGroupPokemonMoveMethod(HasVersionGroup):

  pokemon_move_method_id = models.IntegerField()



#####################
#  LANGUAGE MODELS  #
#####################

class Language(HasName, HasOrder):

  iso639 = models.CharField(max_length=2)

  iso3166 = models.CharField(max_length=2)

  official = models.BooleanField(default = False)


class LanguageName(IsName):

  local_language_id = models.IntegerField()



#######################
#  GENERATION MODELS  #
#######################

class Generation(HasName):

  main_region_id = models.IntegerField()


class GenerationName(IsName, HasGeneration):
  pass



####################
#  ABILITY MODELS  #
####################

class Ability(HasName, HasGeneration):

  is_main_series = models.BooleanField(default = False)


class AbilityDescription(HasLanguage, HasAbility):

  short_effect = models.CharField(max_length=300)

  effect = models.CharField(max_length=2000)


class AbilityFlavorText(HasLanguage, HasAbility, HasVersionGroup):

  flavor_text = models.CharField(max_length=100)


class AbilityName(IsName, HasAbility):
  pass



#################
#  TYPE MODELS  #
#################

class Type(HasName, HasGeneration):

  damage_class_id = models.IntegerField(blank = True, null = True)


class TypeName(IsName, HasType):
  pass


class TypeGameIndex(HasType, HasGeneration):

  game_index = models.IntegerField()


class TypeEfficacy(models.Model):

  damage_type_id = models.IntegerField()

  target_type_id = models.IntegerField()

  damage_factor = models.IntegerField()



#################
#  STAT MODELS  #
#################

class Stat(HasName, HasDamageClass):

  is_battle_only = models.BooleanField(default = False)

  game_index = models.IntegerField()


class StatName(IsName, HasStat):
  pass



###########################
#  CHARACTERISTIC MODELS  #
###########################

class Characteristic(HasStat):

  gene_mod_5 = models.IntegerField()


class CharacteristicDescription(HasCharacteristic, HasLanguage):

  description = models.CharField(max_length = 60)



######################
#  EGG GROUP MODELS  #
######################

class EggGroup(HasName):
  pass


class EggGroupName(IsName, HasEggGroup):
  pass



########################
#  GROWTH RATE MODELS  #
########################

class GrowthRate(HasName):

  formula = models.CharField(max_length = 500)


class GrowthRateDescription(HasName, HasLanguage, HasGrowthRate):
  pass



###################
#  NATURE MODELS  #
###################

class Nature(HasName):

  decreased_stat_id = models.ForeignKey(Stat, blank = True, null = True, related_name = 'decreased')

  increased_stat_id = models.ForeignKey(Stat, blank = True, null = True, related_name = 'increased')

  hates_flavor_id = models.IntegerField()

  likes_flavor_id = models.IntegerField()

  game_index = models.IntegerField()


class NatureName(IsName, HasNature):
  pass


class NaturePokeathlonStat(HasNature):

  pokeathlon_stat_id = models.ForeignKey(Stat, blank = True, null = True)

  max_change = models.IntegerField()


class NatureBattleStylePreference(HasNature):

  move_battle_style_id = models.IntegerField()

  low_hp_preference = models.IntegerField()

  high_hp_preference = models.IntegerField()
