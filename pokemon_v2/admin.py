from __future__ import unicode_literals
from django.contrib import admin

from .models import *

admin.site.register(Ability)
admin.site.register(AbilityName)
admin.site.register(AbilityDescription)
admin.site.register(AbilityFlavorText)
admin.site.register(AbilityChange)
admin.site.register(AbilityChangeDescription)

admin.site.register(Characteristic)
admin.site.register(CharacteristicDescription)

admin.site.register(EggGroup)
admin.site.register(EggGroupName)

admin.site.register(EvolutionChain)
admin.site.register(EvolutionTrigger)
admin.site.register(EvolutionTriggerName)

admin.site.register(Experience)

admin.site.register(Gender)

admin.site.register(Generation)
admin.site.register(GenerationName)

admin.site.register(GrowthRate)
admin.site.register(GrowthRateDescription)

admin.site.register(Language)
admin.site.register(LanguageName)

admin.site.register(Machine)

admin.site.register(MoveBattleStyle)
admin.site.register(MoveBattleStyleName)
admin.site.register(MoveChange)
admin.site.register(MoveDamageClass)
admin.site.register(MoveDamageClassDescription)
admin.site.register(MoveEffectChange)
admin.site.register(MoveEffectChangeDescription)
admin.site.register(MoveEffectDescription)
admin.site.register(MoveEffect)
admin.site.register(MoveFlagMap)
admin.site.register(MoveFlagDescription)
admin.site.register(MoveFlag)
admin.site.register(MoveFlavorText)
admin.site.register(MoveMeta)
admin.site.register(MoveMetaAilment)
admin.site.register(MoveMetaAilmentName)
admin.site.register(MoveMetaCategoryDescription)
admin.site.register(MoveMetaCategory)
admin.site.register(MoveMetaStatChange)
admin.site.register(MoveName)
admin.site.register(MoveTargetDescription)
admin.site.register(MoveTarget)
admin.site.register(Move)

admin.site.register(NatureBattleStylePreference)
admin.site.register(NatureName)
admin.site.register(NaturePokeathlonStat)
admin.site.register(Nature)

admin.site.register(Pokedex)
admin.site.register(PokedexVersionGroup)
admin.site.register(PokedexDescription)

admin.site.register(Pokemon)
admin.site.register(PokemonAbility)
admin.site.register(PokemonColor)
admin.site.register(PokemonColorName)
admin.site.register(PokemonDexNumber)
admin.site.register(PokemonEggGroup)
admin.site.register(PokemonEvolution)
admin.site.register(PokemonForm)
admin.site.register(PokemonFormName)
admin.site.register(PokemonFormGeneration)
admin.site.register(PokemonGameIndex)
admin.site.register(PokemonHabitat)
admin.site.register(PokemonHabitatName)
admin.site.register(PokemonItem)
admin.site.register(PokemonMove)
admin.site.register(PokemonMoveMethod)
admin.site.register(PokemonMoveMethodName)
admin.site.register(PokemonShape)
admin.site.register(PokemonShapeName)
admin.site.register(PokemonSpecies)
admin.site.register(PokemonSpeciesName)
admin.site.register(PokemonSpeciesDescription)
admin.site.register(PokemonSpeciesFlavorText)
admin.site.register(PokemonStat)
admin.site.register(PokemonType)

admin.site.register(StatName)
admin.site.register(Stat)

admin.site.register(Type)
admin.site.register(TypeName)
admin.site.register(TypeGameIndex)
admin.site.register(TypeEfficacy)

admin.site.register(Version)
admin.site.register(VersionName)
admin.site.register(VersionGroup)
admin.site.register(VersionGroupRegion)
admin.site.register(VersionGroupPokemonMoveMethod)
