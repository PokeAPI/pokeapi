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


class HasDescription(models.Model):

  description = models.CharField(max_length=1000, default='')

  class Meta:
       abstract = True


class HasGender(models.Model):

  gender = models.ForeignKey('Gender', blank=True, null=True)

  class Meta:
       abstract = True


class HasEggGroup(models.Model):

  egg_group = models.ForeignKey('EggGroup', blank=True, null=True)

  class Meta:
       abstract = True


class HasEvolutionTrigger(models.Model):

  evolution_trigger = models.ForeignKey('EvolutionTrigger', blank=True, null=True)

  class Meta:
       abstract = True


class HasFlavorText(models.Model):

  flavor_text = models.CharField(max_length=500)

  class Meta:
       abstract = True


class HasGameIndex(models.Model):

  game_index = models.IntegerField()

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


class HasMetaAilment(models.Model):

  move_meta_ailment = models.ForeignKey('MoveMetaAilment', blank = True, null = True)

  class Meta:
       abstract = True


class HasMetaCategory(models.Model):

  move_meta_category = models.ForeignKey('MoveMetaCategory', blank = True, null = True)

  class Meta:
       abstract = True


class HasMove(models.Model):

  move = models.ForeignKey('Move', blank = True, null = True)

  class Meta:
       abstract = True


class HasMoveDamageClass(models.Model):

  move_damage_class = models.ForeignKey('MoveDamageClass', blank = True, null = True)

  class Meta:
       abstract = True


class HasMoveEffect(models.Model):

  move_effect = models.ForeignKey('MoveEffect', blank = True, null = True)

  class Meta:
       abstract = True


class HasMoveFlag(models.Model):

  move_flag = models.ForeignKey('MoveFlag', blank = True, null = True)

  class Meta:
       abstract = True


class HasMoveTarget(models.Model):

  move_target = models.ForeignKey('MoveTarget', blank = True, null = True)

  class Meta:
       abstract = True


class HasName(models.Model):

  name = models.CharField(max_length=100)

  class Meta:
       abstract = True


class HasNature(models.Model):

  nature = models.ForeignKey('Nature', blank=True, null=True)

  class Meta:
       abstract = True


class HasOrder(models.Model):

  order = models.IntegerField(blank=True, null=True)

  class Meta:
       abstract = True


class HasPokedex(models.Model):

  pokedex = models.ForeignKey('Pokedex', blank=True, null=True)

  class Meta:
       abstract = True


class HasPokemon(models.Model):

  pokemon = models.ForeignKey('Pokemon', blank=True, null=True)

  class Meta:
       abstract = True


class HasPokemonColor(models.Model):

  pokemon_color = models.ForeignKey('PokemonColor', blank=True, null=True)

  class Meta:
       abstract = True


class HasPokemonForm(models.Model):

  pokemon_form = models.ForeignKey('PokemonForm', blank=True, null=True)

  class Meta:
       abstract = True


class HasPokemonHabitat(models.Model):

  pokemon_habitat = models.ForeignKey('PokemonHabitat', blank=True, null=True)

  class Meta:
       abstract = True


class HasPokemonMoveMethod(models.Model):

  pokemon_move_method = models.ForeignKey('PokemonMoveMethod', blank=True, null=True)

  class Meta:
       abstract = True


class HasPokemonShape(models.Model):

  pokemon_shape = models.ForeignKey('PokemonShape', blank=True, null=True)

  class Meta:
       abstract = True


class HasPokemonSpecies(models.Model):

  pokemon_species = models.ForeignKey('PokemonSpecies', blank=True, null=True)

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


class HasVersion(models.Model):

  version = models.ForeignKey('Version', blank=True, null=True)

  class Meta:
       abstract = True


class HasVersionGroup(models.Model):

  version_group = models.ForeignKey('VersionGroup', blank=True, null=True)

  class Meta:
       abstract = True


class IsDescription(HasLanguage, HasDescription):

  class Meta:
       abstract = True


class IsEffectDescription(HasLanguage):

  short_effect = models.CharField(max_length=300)

  effect = models.CharField(max_length=4000)

  class Meta:
       abstract = True


class IsName(HasLanguage, HasName):

  class Meta:
       abstract = True


class IsFlavorText(HasLanguage, HasFlavorText):

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


class AbilityDescription(IsEffectDescription, HasAbility):
  pass


class AbilityFlavorText(IsFlavorText, HasAbility, HasVersionGroup):
  pass


class AbilityName(IsName, HasAbility):
  pass


class AbilityChange(HasAbility):
  pass


class AbilityChangeDescription(HasLanguage):

  ability_change = models.ForeignKey(AbilityChange, blank=True, null=True)

  effect = models.CharField(max_length=1000)



#################
#  TYPE MODELS  #
#################

class Type(HasName, HasGeneration, HasMoveDamageClass):
  pass


class TypeName(IsName, HasType):
  pass


class TypeGameIndex(HasType, HasGeneration, HasGameIndex):
  pass


class TypeEfficacy(models.Model):

  damage_type_id = models.IntegerField()

  target_type_id = models.IntegerField()

  damage_factor = models.IntegerField()



#################
#  STAT MODELS  #
#################

class Stat(HasName, HasMoveDamageClass):

  is_battle_only = models.BooleanField(default = False)

  game_index = models.IntegerField()


class StatName(IsName, HasStat):
  pass



###########################
#  CHARACTERISTIC MODELS  #
###########################

class Characteristic(HasStat):

  gene_mod_5 = models.IntegerField()


class CharacteristicDescription(HasCharacteristic, IsDescription):
  pass



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


class GrowthRateDescription(HasGrowthRate, IsDescription):
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



#################
#  MOVE MODELS  #
#################

class Move(HasName, HasGeneration, HasType, HasMoveDamageClass, HasMoveEffect, HasMoveTarget):

  power = models.IntegerField(blank = True, null = True)

  pp = models.IntegerField(blank = True, null = True)

  accuracy = models.IntegerField(blank = True, null = True)

  priority = models.IntegerField(blank = True, null = True)

  move_effect_chance = models.IntegerField(blank = True, null = True)

  contest_type_id = models.IntegerField(blank = True, null = True)

  contest_effect_id = models.IntegerField(blank = True, null = True)

  super_contest_effect_id = models.IntegerField(blank = True, null = True)


class MoveName(HasMove, IsName):
  pass


class MoveFlavorText(HasMove, HasVersionGroup, IsFlavorText):
  pass


class MoveChange(HasMove, HasVersionGroup, HasType, HasMoveEffect):

  power = models.IntegerField(blank = True, null = True)

  pp = models.IntegerField(blank = True, null = True)

  accuracy = models.IntegerField(blank = True, null = True)

  move_effect_chance = models.IntegerField(blank = True, null = True)



##############################
#  MOVE DAMAGE CLASS MODELS  #
##############################

class MoveDamageClass(HasName):
  pass


class MoveDamageClassDescription(HasMoveDamageClass, IsDescription, HasName):
  pass



##############################
#  MOVE BATTLE STYLE MODELS  #
##############################

class MoveBattleStyle(HasName):
  pass


class MoveBattleStyleName(IsName):

  move_battle_style = models.ForeignKey(MoveBattleStyle, blank = True, null = True)



########################
#  MOVE EFFECT MODELS  #
########################

class MoveEffect(models.Model):
  pass


class MoveEffectDescription(HasMoveEffect, IsEffectDescription):
  pass


class MoveEffectChange(HasMoveEffect, HasVersionGroup):
  pass


class MoveEffectChangeDescription(HasLanguage):

  move_effect_change = models.ForeignKey('MoveEffectChange', blank = True, null = True)

  effect = models.CharField(max_length=2000)



######################
#  MOVE FLAG MODELS  #
######################

class MoveFlag(HasName):
  pass


class MoveFlagDescription(HasMoveFlag, HasName, IsDescription):
  pass


class MoveFlagMap(HasMove, HasMoveFlag):
  pass



########################
#  MOVE TARGET MODELS  #
########################

class MoveTarget(HasName):
  pass


class MoveTargetDescription(HasMoveTarget, IsDescription, HasName):
  pass



######################
#  MOVE META MODELS  #
######################

class MoveMeta(HasMove, HasMetaAilment, HasMetaCategory):

  min_hits = models.IntegerField(blank = True, null = True)

  max_hits = models.IntegerField(blank = True, null = True)

  min_turns = models.IntegerField(blank = True, null = True)

  max_turns = models.IntegerField(blank = True, null = True)

  drain = models.IntegerField(blank = True, null = True)

  healing = models.IntegerField(blank = True, null = True)

  crit_rate = models.IntegerField(blank = True, null = True)

  ailment_chance = models.IntegerField(blank = True, null = True)

  flinch_chance = models.IntegerField(blank = True, null = True)

  stat_chance = models.IntegerField(blank = True, null = True)


class MoveMetaAilment(HasName):
  pass


class MoveMetaAilmentName(HasMetaAilment, IsName):
  pass


class MoveMetaCategory(HasName):
  pass


class MoveMetaCategoryDescription(HasMetaCategory, IsDescription):
  pass


class MoveMetaStatChange(HasMove, HasStat):

  change = models.IntegerField()



#######################
#  EXPERIENCE MODELS  #
#######################

class Experience(HasGrowthRate):

  level = models.IntegerField()

  experience = models.IntegerField()



###################
#  GENDER MODELS  #
###################

class Gender(HasName):
  pass



####################
#  MACHINE MODELS  #
####################

class Machine(HasGrowthRate):

  machine_number = models.IntegerField()

  version_group = models.ForeignKey(VersionGroup, blank=True, null=True)

  item_id = models.IntegerField()

  move = models.ForeignKey(Move, blank=True, null=True)



######################
#  EVOLUTION MODELS  #
######################

class EvolutionChain(models.Model):

  baby_evolution_item_id = models.IntegerField(blank=True, null=True) #Just for now. Need Item models


class EvolutionTrigger(HasName):
  pass


class EvolutionTriggerName(HasEvolutionTrigger, IsName):
  pass



####################
#  POKEDEX MODELS  #
####################

class Pokedex(HasName):

  region_id = models.IntegerField(blank=True, null=True)

  is_main_series = models.BooleanField(default = False)


class PokedexDescription(HasPokedex, HasName, IsDescription):
  pass


class PokedexVersionGroup(HasPokedex, HasVersionGroup):
  pass



####################
#  POKEMON MODELS  #
####################

class PokemonSpecies(HasName, HasGeneration, HasPokemonColor,
                     HasPokemonShape, HasGrowthRate, HasOrder):

  evolves_from_species = models.ForeignKey('self', blank=True, null=True)

  evolution_chain = models.ForeignKey(EvolutionChain, blank=True, null=True)

  pokemon_habitat = models.ForeignKey('PokemonHabitat', blank=True, null=True)

  gender_rate = models.IntegerField()

  capture_rate = models.IntegerField()

  base_happiness = models.IntegerField()

  is_baby = models.BooleanField(default = False)

  hatch_counter = models.IntegerField()

  has_gender_differences = models.BooleanField(default = False)

  forms_switchable = models.BooleanField(default = False)


class PokemonSpeciesName(IsName, HasPokemonSpecies):

  genus = models.CharField(max_length = 30)


class PokemonSpeciesDescription(HasPokemonSpecies, IsDescription):
  pass


class PokemonSpeciesFlavorText(IsFlavorText, HasPokemonSpecies, HasVersion):
  pass


class Pokemon(HasName, HasPokemonSpecies, HasOrder):

  height = models.IntegerField()

  weight = models.IntegerField()

  base_experience = models.IntegerField()

  is_default = models.BooleanField(default = False)


class PokemonAbility(HasPokemon, HasAbility):

  is_hidden = models.BooleanField(default = False)

  slot = models.IntegerField()


class PokemonColor(HasName):
  pass


class PokemonColorName(HasPokemonColor, IsName):
  pass


class PokemonDexNumber(HasPokemonSpecies, HasPokedex):

  pokedex_number = models.IntegerField()


class PokemonEggGroup(HasPokemonSpecies, HasEggGroup):
  pass


class PokemonEvolution(HasEvolutionTrigger, HasGender):

  evolution_item_id = models.IntegerField(blank=True, null=True) # need item tables

  evolved_species = models.ForeignKey(PokemonSpecies, related_name="evolved_species", blank=True, null=True)

  min_level = models.IntegerField(blank=True, null=True)

  location_id = models.IntegerField(blank=True, null=True) # need location tables

  held_item_id = models.IntegerField(blank=True, null=True) # need item tables

  time_of_day = models.CharField(max_length = 10, blank=True, null=True)

  known_move = models.ForeignKey(Move, blank=True, null=True)

  known_move_type = models.ForeignKey(Type, related_name="known_move", blank=True, null=True)

  min_happiness = models.IntegerField(blank=True, null=True)

  min_beauty = models.IntegerField(blank=True, null=True)

  min_affection = models.IntegerField(blank=True, null=True)

  relative_physical_stats = models.IntegerField(blank=True, null=True)

  party_species = models.ForeignKey(PokemonSpecies, related_name="party_species", blank=True, null=True)

  party_type = models.ForeignKey(Type, related_name="party_type", blank=True, null=True)

  trade_species = models.ForeignKey(PokemonSpecies, related_name="trade_species", blank=True, null=True)

  needs_overworld_rain = models.BooleanField(default = False)

  turn_upside_down = models.BooleanField(default = False)


class PokemonForm(HasName, HasPokemon, HasOrder):

  form_identifier = models.CharField(max_length = 30)

  introduced_in_version_group = models.ForeignKey(VersionGroup, blank=True, null=True)

  is_default = models.BooleanField(default = False)

  is_battle_only = models.BooleanField(default = False)

  is_mega = models.BooleanField(default = False)

  form_order = models.IntegerField(blank=True, null=True)


class PokemonFormGeneration(HasPokemonForm, HasGeneration, HasGameIndex):
  pass


class PokemonFormName(HasPokemonForm, IsName):

  pokemon_name = models.CharField(max_length = 30)


class PokemonGameIndex(HasPokemon, HasGameIndex, HasVersion):
  pass


class PokemonHabitat(HasName):
  pass


class PokemonHabitatName(IsName):

  pokemon_habitat = models.ForeignKey(PokemonHabitat, blank=True, null=True)


class PokemonItem(HasPokemon, HasVersion):

  item_id = models.IntegerField()

  rarity = models.IntegerField()


class PokemonMoveMethod(HasName):
  pass


class PokemonMoveMethodName(IsName, HasPokemonMoveMethod, HasDescription):
  pass


class PokemonMove(HasPokemon, HasPokemonMoveMethod, HasVersionGroup, HasMove, HasOrder):

  level = models.IntegerField()


class PokemonShape(HasName):
  pass


class PokemonShapeName(IsName):

  awesome_name = models.CharField(max_length = 30)

  pokemon_shape = models.ForeignKey(PokemonShape, blank=True, null=True)


class PokemonStat(HasPokemon, HasStat):

  base_stat = models.IntegerField()

  effort = models.IntegerField()


class PokemonType(HasPokemon, HasType):

  slot = models.IntegerField()
