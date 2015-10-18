
from __future__ import unicode_literals
from rest_framework import serializers
from collections import OrderedDict

"""
PokeAPI v2 serializers in order of dependency
"""

from .models import *

#########################
#  SUMMARY SERIALIZERS  #
#########################

# Summary serializers are just for list and reference behavior

# Putting summary serializers up top so there are no conflicts
# with reference accross models due to script running order

class LanguageSummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Language
        fields = ('name', 'url')

class RegionSummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Region
        fields = ('name', 'url')

class GenerationSummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Generation
        fields = ('name', 'url')

class GrowthRateSummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = GrowthRate
        fields = ('name', 'url')

class VersionSummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Version
        fields = ('name', 'url')

class VersionGroupSummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = VersionGroup
        fields = ('name', 'url')

class AbilitySummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Ability
        fields = ('name', 'url')

class StatSummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Stat
        fields = ('name', 'url')

class ItemPocketSummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ItemPocket
        fields = ('name', 'url')

class ItemCategorySummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ItemCategory
        fields = ('name', 'url')

class ItemFlagSummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ItemFlag
        fields = ('name', 'url')

class ItemFlingEffectSummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ItemFlingEffect
        fields = ('name', 'url')

class ItemSummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Item
        fields = ('name', 'url')

class NatureSummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Nature
        fields = ('name', 'url')

class BerryFirmnessSummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = BerryFirmness
        fields = ('name', 'url')
        
class BerrySummarySerializer(serializers.HyperlinkedModelSerializer):

    name = serializers.SerializerMethodField('get_berry_name')

    class Meta:
        model = Berry
        fields = ('url', 'name')

    def get_berry_name(self,obj):

        item = Item.objects.get(id=obj.item.id)
        serializer = ItemSummarySerializer(item, context=self.context)
        name = serializer.data['name']

        return name[:name.index('-')]

class EggGroupSummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = EggGroup
        fields = ('name', 'url')
        
class TypeSummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Type
        fields = ('name', 'url')
        
class MoveDamageClassSummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = MoveDamageClass
        fields = ('name', 'url')
        
class MoveMetaAilmentSummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = MoveMetaAilment
        fields = ('name', 'url')

class MoveMetaCategorySummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = MoveMetaCategory
        fields = ('name', 'url')
        
class MoveTargetSummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = MoveTarget
        fields = ('name', 'url')
        
class MoveSummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Move
        fields = ('name', 'url')
        
class PokemonColorSummarySerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = PokemonColor
        fields = ('name', 'url')
        
class PokemonHabitatSummarySerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = PokemonHabitat
        fields = ('name', 'url')

class MoveLearnMethodSummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = MoveLearnMethod
        fields = ('name', 'url')
        
class PokemonShapeSummarySerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = PokemonShape
        fields = ('name', 'url')
        
class PokemonSummarySerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Pokemon
        fields = ('name', 'url')
        
class PokemonSpeciesSummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta: 
        model = PokemonSpecies
        fields = ('name', 'url')
        
class EvolutionTriggerSummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = EvolutionTrigger
        fields = ('name', 'url')

class EvolutionChainSummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = EvolutionChain
        fields = ('url',)


class PokedexSummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Pokedex
        fields = ('name', 'url')

class LocationSummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Location
        fields = ('name', 'url')

class PokemonFormSummarySerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = PokemonForm
        fields = ('name', 'url')



##########################
#  LANGUAGE SERIALIZERS  #
##########################

class LanguageNameSerializer(serializers.ModelSerializer):

    local_language_url = serializers.HyperlinkedRelatedField(read_only='True', source="local_language_id", view_name='language-detail')

    class Meta:
        model = LanguageName
        fields = ('name', 'local_language_url')


class LanguageDetailSerializer(serializers.ModelSerializer):

    names = LanguageNameSerializer(many=True, read_only=True, source='languagename_language')

    class Meta:
        model = Language
        fields = ('name', 'official', 'iso639', 'iso3166', 'id', 'names')



########################
#  REGION SERIALIZERS  #
########################

class RegionNameSerializer(serializers.ModelSerializer):

    language = LanguageSummarySerializer()

    class Meta:
        model = RegionName
        fields = ('name', 'language')


class RegionDetailSerializer(serializers.ModelSerializer):

    names = RegionNameSerializer(many=True, read_only=True, source="regionname")

    class Meta:
        model = Region
        fields = ('id', 'name', 'names')



############################
#  GENERATION SERIALIZERS  #
############################

class GenerationNameSerializer(serializers.ModelSerializer):

    language = LanguageSummarySerializer()

    class Meta:
        model = GenerationName
        fields = ('name', 'language')


class GenerationDetailSerializer(serializers.ModelSerializer):

    region = RegionSummarySerializer()
    names = GenerationNameSerializer(many=True, read_only=True, source="generationname")

    class Meta:
        model = Generation
        fields = ('id', 'name', 'region', 'names')



#############################
#  GROWTH RATE SERIALIZERS  #
#############################

class ExperienceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Experience
        fields = ('level', 'experience')


class GrowthRateDescriptionSerializer(serializers.ModelSerializer):

    language = LanguageSummarySerializer()

    class Meta:
        model = GrowthRateDescription
        fields = ('description', 'language')


class GrowthRateDetailSerializer(serializers.ModelSerializer):

    descriptions = GrowthRateDescriptionSerializer(many=True, read_only=True, source="growthratedescription")
    levels = ExperienceSerializer(many=True, read_only=True, source="experience")

    class Meta:
        model = GrowthRate
        fields = ('id', 'name', 'formula', 'descriptions', 'levels')



#########################
#  VERSION SERIALIZERS  #
#########################

class VersionNameSerializer(serializers.ModelSerializer):

    language = LanguageSummarySerializer()

    class Meta:
        model = VersionName
        fields = ('name', 'language')


class VersionDetailSerializer(serializers.ModelSerializer):
    """
    Should have a link to Version Group info but the Circular
    dependency and compilation order fight eachother and I'm
    not sure how to add anything other than a hyperlink
    """

    names = VersionNameSerializer(many=True, read_only=True, source="versionname")
    version_group = VersionGroupSummarySerializer()

    class Meta:
        model = Version
        fields = ('id', 'name', 'names', 'version_group')


class VersionGroupDetailSerializer(serializers.ModelSerializer):

    generation = GenerationSummarySerializer()
    versions = VersionSummarySerializer(many=True, read_only=True, source="version")

    class Meta:
        model = VersionGroup
        fields = ('id', 'name', 'order', 'generation', 'versions')



##########################
#  LOCATION SERIALIZERS  #
##########################

class LocationNameSerializer(serializers.ModelSerializer):

    language = LanguageSummarySerializer()

    class Meta:
        model = LocationName
        fields = ('name', 'language')


class LocationDetailSerializer(serializers.ModelSerializer):

    region = RegionSummarySerializer()
    names = VersionNameSerializer(many=True, read_only=True, source="locationname")

    class Meta:
        model = Location
        fields = ('id', 'name', 'region', 'names')



#########################
#  ABILITY SERIALIZERS  #
#########################

class AbilityDescriptionSerializer(serializers.ModelSerializer):

    language = LanguageSummarySerializer()

    class Meta:
        model = AbilityDescription
        fields = ('effect', 'short_effect', 'language')


class AbilityFlavorTextSerializer(serializers.ModelSerializer):

    text = serializers.CharField(source="flavor_text")
    language = LanguageSummarySerializer()
    version_group = VersionGroupSummarySerializer()

    class Meta:
        model = AbilityFlavorText
        fields = ('text', 'version_group', 'language')


class AbilityNameSerializer(serializers.ModelSerializer):

    language = LanguageSummarySerializer()

    class Meta:
        model = AbilityName
        fields = ('name', 'language')


class AbilityDetailSerializer(serializers.ModelSerializer):

    descriptions = AbilityDescriptionSerializer(many=True, read_only=True, source="abilitydescription")
    flavor_text_entries = AbilityFlavorTextSerializer(many=True, read_only=True, source="abilityflavortext")
    names = AbilityNameSerializer(many=True, read_only=True, source="abilityname")
    generation = GenerationSummarySerializer()

    class Meta:
        model = Ability
        fields = (
            'id', 
            'name',
            'is_main_series',
            'generation',
            'names',
            'descriptions', 
            'flavor_text_entries'
        )



######################
#  STAT SERIALIZERS  #
######################

class StatDetailSerializer(serializers.HyperlinkedModelSerializer):

    move_damage_class = MoveDamageClassSummarySerializer()

    class Meta:
        model = Stat



#############################
#  ITEM POCKET SERIALIZERS  #
#############################

class ItemPocketNameSerializer(serializers.ModelSerializer):

    language = LanguageSummarySerializer()

    class Meta:
        model = ItemName
        fields = ('name', 'language')


class ItemPocketDetailSerializer(serializers.ModelSerializer):

    names = ItemPocketNameSerializer(many=True, read_only=True, source="itempocketname")

    class Meta:
        model = ItemPocket
        fields = ('id', 'name', 'names')



###############################
#  ITEM CATEGORY SERIALIZERS  #
###############################

class ItemCategoryNameSerializer(serializers.ModelSerializer):

    language = LanguageSummarySerializer()

    class Meta:
        model = ItemName
        fields = ('name', 'language')


class ItemCategoryDetailSerializer(serializers.ModelSerializer):

    names = ItemCategoryNameSerializer(many=True, read_only=True, source="itemcategoryname")
    pocket = ItemPocketSummarySerializer(source="item_pocket")

    class Meta:
        model = ItemCategory
        fields = ('id', 'name', 'pocket', 'names')


###########################
#  ITEM FLAG SERIALIZERS  #
###########################

# Calling these Attributes instead of Flags cause I think that just makes more sense
# Probably should change the names of the models as well. Work To Do.

class ItemFlagDescriptionSerializer(serializers.ModelSerializer):

    language = LanguageSummarySerializer()

    class Meta:
        model = ItemFlagDescription
        fields = ('name', 'description', 'language')


class ItemFlagDetailSerializer(serializers.ModelSerializer):

    names = serializers.SerializerMethodField('get_flag_names')
    descriptions = serializers.SerializerMethodField('get_flag_descriptions')

    class Meta:
        model = ItemFlag
        fields = ('id', 'name', 'names', 'descriptions')

    def get_flag_names(self, obj):

        item_flag = ItemFlagDescription.objects.filter(item_flag_id=obj)
        serializer = ItemFlagDescriptionSerializer(item_flag, many=True, context=self.context)
        data  = serializer.data

        print data

        for flag in data:
            del flag['description']

        return data

    def get_flag_descriptions(self, obj):

        item_flag = ItemFlagDescription.objects.filter(item_flag_id=obj)
        serializer = ItemFlagDescriptionSerializer(item_flag, many=True, context=self.context)
        data = serializer.data

        for flag in data:
            del flag['name']

        return data


class ItemFlagMapSerializer(serializers.ModelSerializer):

    attribute = ItemFlagSummarySerializer(source='item_flag')

    class Meta:
        model = ItemFlagMap
        fields = ('attribute',)



###########################
#  ITEM FLAG SERIALIZERS  #
###########################

class ItemFlingEffectDescriptionSerializer(serializers.ModelSerializer):

    language = LanguageSummarySerializer()
    description = serializers.CharField(source="effect")

    class Meta:
        model = ItemFlingEffectDescription
        fields = ('description', 'language')


class ItemFlingEffectDetailSerializer(serializers.ModelSerializer):

    descriptions = ItemCategoryNameSerializer(many=True, read_only=True, source="itemflingeffectdescription")

    class Meta:
        model = ItemFlingEffect
        fields = ('id', 'name', 'descriptions')



#######################
#  ITEM  SERIALIZERS  #
#######################

class ItemFlavorTextSerializer(serializers.ModelSerializer):

    text = serializers.CharField(source="flavor_text")
    language = LanguageSummarySerializer()
    version_group = VersionGroupSummarySerializer()

    class Meta:
        model = ItemFlavorText
        fields = ('text', 'version_group', 'language')


class ItemDescriptionSerializer(serializers.ModelSerializer):

    language = LanguageSummarySerializer()

    class Meta:
        model = ItemDescription
        fields = ('effect', 'short_effect', 'language')


class ItemNameSerializer(serializers.ModelSerializer):

    language = LanguageSummarySerializer()

    class Meta:
        model = ItemName
        fields = ('name', 'language')


class ItemDetailSerializer(serializers.ModelSerializer):

    names = ItemNameSerializer(many=True, read_only=True, source="itemname")
    descriptions = ItemDescriptionSerializer(many=True, read_only=True, source="itemdescription")
    flavor_text_entries = ItemFlavorTextSerializer(many=True, read_only=True, source="itemflavortext")
    category = ItemCategorySummarySerializer(source="item_category")
    attributes = ItemFlagMapSerializer(many=True, read_only=True, source="itemflagmap")
    fling_effect = ItemFlingEffectSummarySerializer(source="item_fling_effect")

    class Meta:
        model = Item
        fields = (
            'id',
            'name',
            'cost',
            'fling_power',
            'fling_effect',
            'category',
            'attributes',
            'names',
            'descriptions',
            'flavor_text_entries'
        )



########################
#  NATURE SERIALIZERS  #
########################

class NatureNameSerializer(serializers.ModelSerializer):

    name = LanguageSummarySerializer()

    class Meta:
        model = NatureName
        fields = ('description', 'language')


class NatureDetailSerializer(serializers.ModelSerializer):

    names = NatureNameSerializer(many=True, read_only=True, source="naturename")

    class Meta:
        model = Nature
        fields = ('id', 'name', 'names')



#######################
#  BERRY SERIALIZERS  #
#######################

class BerryFirmnessNameSerializer(serializers.ModelSerializer):

    language = LanguageSummarySerializer()

    class Meta:
        model = BerryFirmnessName
        fields = ('name', 'language')


class BerryFirmnessDetailSerializer(serializers.ModelSerializer):

    names = BerryFirmnessNameSerializer(many=True, read_only=True, source="berryfirmnessname")

    class Meta:
        model = BerryFirmness
        fields = ('id', 'name', 'names')


class BerryDetailSerializer(serializers.ModelSerializer):

    item = ItemSummarySerializer()
    name = serializers.SerializerMethodField('get_berry_name')
    nature = NatureSummarySerializer()
    nature_power = serializers.IntegerField(source='natural_gift_power')
    firmness = BerryFirmnessSummarySerializer(source="berry_firmness")

    class Meta:
        model = Berry
        fields = (
            'id',
            'name',
            'firmness',
            'growth_time',
            'item',
            'max_harvest',
            'nature',
            'nature_power',
            'size',
            'smoothness',
            'soil_dryness'
        )

    def get_berry_name(self,obj):

        item = Item.objects.get(id=obj.item.id)
        serializer = ItemSummarySerializer(item, context=self.context)
        name = serializer.data['name']

        return name[:name.index('-')]



###########################
#  EGG GROUP SERIALIZERS  #
###########################

class PokemonEggGroupSerializer(serializers.ModelSerializer):

    species = PokemonSpeciesSummarySerializer(source="pokemon_species")
    egg_group = EggGroupSummarySerializer()

    class Meta:
        model = PokemonEggGroup
        fields = ('species', 'egg_group')


class EggGroupNameSerializer(serializers.ModelSerializer):

    language = LanguageSummarySerializer()

    class Meta:
        model = EggGroupName
        fields = ('name', 'language')


class EggGroupDetailSerializer(serializers.ModelSerializer):

    names = EggGroupNameSerializer(many=True, read_only=True, source="egggroupname")
    species = serializers.SerializerMethodField('get_pokemon_species')

    class Meta:
        model = EggGroup
        fields = ('id', 'name', 'names', 'species')

    def get_pokemon_species(self, obj):

        results = PokemonEggGroup.objects.filter(egg_group=obj)
        data = PokemonEggGroupSerializer(results, many=True, context=self.context).data
        associated_species = []
        for species in data:
            associated_species.append(species['species'])

        return associated_species



######################
#  TYPE SERIALIZERS  #
######################

class TypeEfficacySerializer(serializers.ModelSerializer):

    class Meta:
        model = TypeEfficacy


class TypeNameSerializer(serializers.ModelSerializer):

    language = LanguageSummarySerializer()

    class Meta:
        model = TypeName
        fields = ('name', 'language')


class TypeDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for the Type resource
    """
    generation = GenerationSummarySerializer()
    names = AbilityNameSerializer(many=True, read_only=True, source="typename")
    damage_relations = serializers.SerializerMethodField('get_type_relationships')

    class Meta:
        model = Type
        fields = ('id', 'name', 'move_damage_class', 'generation', 'names', 'damage_relations')

    def get_type_relationships(self, obj):

        relations = OrderedDict()
        relations['no_damage_to'] = []
        relations['half_damage_to'] = []
        relations['double_damage_to'] = []

        relations['no_damage_from'] = []
        relations['half_damage_from'] = []
        relations['double_damage_from'] = []

        # Damage To
        results = TypeEfficacy.objects.filter(damage_type=obj)
        serializer = TypeEfficacySerializer(results, many=True, context=self.context)

        for relation in serializer.data:
            type = Type.objects.get(pk=relation['target_type'])
            if relation['damage_factor'] == 200:
                relations['double_damage_to'].append(TypeSummarySerializer(type, context=self.context).data)
            elif relation['damage_factor'] == 50:
                relations['half_damage_to'].append(TypeSummarySerializer(type, context=self.context).data)
            elif relation['damage_factor'] == 0:
                relations['no_damage_to'].append(TypeSummarySerializer(type, context=self.context).data)

        # Damage From
        results = TypeEfficacy.objects.filter(target_type=obj)
        serializer = TypeEfficacySerializer(results, many=True, context=self.context)

        for relation in serializer.data:
            type = Type.objects.get(pk=relation['damage_type'])
            if relation['damage_factor'] == 200:
                relations['double_damage_from'].append(TypeSummarySerializer(type, context=self.context).data)
            elif relation['damage_factor'] == 50:
                relations['half_damage_from'].append(TypeSummarySerializer(type, context=self.context).data)
            elif relation['damage_factor'] == 0:
                relations['no_damage_from'].append(TypeSummarySerializer(type, context=self.context).data)

        return relations



###################################
#  MOVE DAMAGE CLASS SERIALIZERS  #
###################################

class MoveDamageClassDescriptionSerializer(serializers.ModelSerializer):

    language = LanguageSummarySerializer()

    class Meta:
        model = MoveDamageClassDescription
        fields = ('name', 'description', 'language')


class MoveDamageClassDetailSerializer(serializers.ModelSerializer):

    names = serializers.SerializerMethodField('get_move_damage_class_names')
    descriptions = serializers.SerializerMethodField('get_move_damage_class_descriptions')

    class Meta:
        model = MoveDamageClass
        fields = ('id', 'name', 'names', 'descriptions')

    def get_move_damage_class_names(self, obj):

        move_methods = MoveDamageClassDescription.objects.filter(move_damage_class_id=obj)
        serializer = MoveDamageClassDescriptionSerializer(move_methods, many=True, context=self.context)
        data  = serializer.data

        for name in data:
            del name['description']

        return data

    def get_move_damage_class_descriptions(self, obj):

        move_methods = MoveDamageClassDescription.objects.filter(move_damage_class_id=obj)
        serializer = MoveDamageClassDescriptionSerializer(move_methods, many=True, context=self.context)
        data = serializer.data

        for name in data:
            del name['name']

        return data



###########################
#  MOVE META SERIALIZERS  #
###########################

class MoveMetaAilmentDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = MoveMetaAilment


class MoveMetaCategoryDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = MoveMetaCategory


class MoveMetaSerializer(serializers.ModelSerializer):

    ailment = MoveMetaAilmentSummarySerializer(source="move_meta_category")
    category = MoveMetaCategorySummarySerializer(source="move_meta_category")

    class Meta:
        model = MoveMeta
        fields = (
            'ailment',
            'category',
            'min_hits',
            'max_hits',
            'min_turns',
            'max_turns',
            'drain',
            'healing',
            'crit_rate',
            'ailment_chance',
            'flinch_chance',
            'stat_chance'
        )



#############################
#  MOVE TARGET SERIALIZERS  #
#############################

class MoveTargetDescriptionSerializer(serializers.ModelSerializer):

    language = LanguageSummarySerializer()

    class Meta:
        model = MoveTargetDescription
        fields = ('name', 'description', 'language')


class MoveTargetDetailSerializer(serializers.ModelSerializer):

    names = serializers.SerializerMethodField('get_move_target_names')
    descriptions = serializers.SerializerMethodField('get_move_target_descriptions')

    class Meta:
        model = MoveTarget
        fields = ('id', 'name', 'names', 'descriptions')

    def get_move_target_names(self, obj):

        move_methods = MoveTargetDescription.objects.filter(move_target_id=obj)
        serializer = MoveTargetDescriptionSerializer(move_methods, many=True, context=self.context)
        data  = serializer.data

        for name in data:
            del name['description']

        return data

    def get_move_target_descriptions(self, obj):

        move_methods = MoveTargetDescription.objects.filter(move_target_id=obj)
        serializer = MoveTargetDescriptionSerializer(move_methods, many=True, context=self.context)
        data = serializer.data

        for name in data:
            del name['name']

        return data



######################
#  MOVE SERIALIZERS  #
######################

class MoveNameSerializer(serializers.ModelSerializer):

    language = LanguageSummarySerializer()

    class Meta:
        model = AbilityName
        fields = ('name', 'language')


class MoveDetailSerializer(serializers.ModelSerializer):

    generation = GenerationSummarySerializer()
    type = TypeSummarySerializer()
    move_target = MoveTargetSummarySerializer()
    damage_class = MoveDamageClassSummarySerializer(source="move_damage_class")
    meta = MoveMetaSerializer(read_only=True, source="movemeta")
    names = MoveNameSerializer(many=True, read_only=True, source="movename")
    effect_chance = serializers.IntegerField(source="move_effect_chance")

    class Meta:
        model = Move
        fields = (
            'id', 
            'name',
            'accuracy',
            'damage_class',
            'effect_chance',
            'generation',
            'meta',
            'move_target',
            'names',
            'power', 
            'pp', 
            'priority',
            'type',
        )



#################################
#  POKEMON ABILITY SERIALIZERS  #
#################################

class PokemonAbilitySerializer(serializers.ModelSerializer):

    ability = AbilitySummarySerializer()
    
    class Meta:
        model = PokemonAbility
        fields = ('is_hidden', 'slot', 'ability')



###############################
#  POKEMON COLOR SERIALIZERS  #
###############################

class PokemonColorNameSerializer(serializers.HyperlinkedModelSerializer):

    language = LanguageSummarySerializer()

    class Meta:
        model = PokemonColorName
        fields = ('name', 'language')


class PokemonColorDetailSerializer(serializers.ModelSerializer):

    names = PokemonColorNameSerializer(many=True, read_only=True, source="pokemoncolorname")
    
    class Meta:
        model = PokemonColor
        fields = ('id', 'name', 'names')



##############################
#  POKEMON FORM SERIALIZERS  #
##############################

class PokemonFormDetailSerializer(serializers.ModelSerializer):

    pokemon = PokemonSummarySerializer()
    version_group = VersionGroupSummarySerializer()
    
    class Meta:
        model = PokemonForm
        fields = (
            'id', 
            'name',
            'order',
            'form_order',
            'is_default',
            'is_battle_only',
            'is_mega',
            'form_name',
            'pokemon',
            'version_group'
        )



#################################
#  POKEMON HABITAT SERIALIZERS  #
#################################

class PokemonHabitatNameSerializer(serializers.HyperlinkedModelSerializer):

    language = LanguageSummarySerializer()

    class Meta:
        model = PokemonHabitatName
        fields = ('name', 'language')


class PokemonHabitatDetailSerializer(serializers.ModelSerializer):

    names = PokemonHabitatNameSerializer(many=True, read_only=True, source="pokemonhabitatname")
    
    class Meta:
        model = PokemonHabitat
        fields = ('id', 'name', 'names')


##############################
#  POKEMON MOVE SERIALIZERS  #
##############################

class MoveLearnMethodDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = MoveLearnMethod

    def get_move_method_names(self, obj):

        move_methods = MoveLearnMethodName.objects.filter(pokemon_move_method_id=obj)
        serializer = MoveLearnMethodNameSerializer(move_methods, many=True, context=self.context)
        data  = serializer.data

        for name in data:
            del name['description']

        return data

    def get_move_method_descriptions(self, obj):

        move_methods = MoveLearnMethodName.objects.filter(pokemon_move_method_id=obj)
        serializer = MoveLearnMethodNameSerializer(move_methods, many=True, context=self.context)
        data = serializer.data

        for name in data:
            del name['name']

        return data


class PokemonMoveSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PokemonMove



###############################
#  POKEMON SHAPE SERIALIZERS  #
###############################

class PokemonShapeNameSerializer(serializers.HyperlinkedModelSerializer):

    language = LanguageSummarySerializer()

    class Meta:
        model = PokemonShapeName
        fields = ('name', 'awesome_name', 'language')


class PokemonShapeDetailSerializer(serializers.ModelSerializer):

    names = serializers.SerializerMethodField('get_shape_names')
    awesome_names = serializers.SerializerMethodField('get_shape_awesome_names')
    
    class Meta:
        model = PokemonShape
        fields = ('id', 'name', 'names', 'awesome_names')

    def get_shape_names(self, obj):

        results = PokemonShapeName.objects.filter(pokemon_shape_id=obj)
        serializer = PokemonShapeNameSerializer(results, many=True, context=self.context)
        data  = serializer.data

        for entry in data:
            del entry['awesome_name']

        return data

    def get_shape_awesome_names(self, obj):

        results = PokemonShapeName.objects.filter(pokemon_shape_id=obj)
        serializer = PokemonShapeNameSerializer(results, many=True, context=self.context)
        data = serializer.data

        for entry in data:
            del entry['name']

        return data



##############################
#  POKEMON ITEM SERIALIZERS  #
##############################

class PokemonItemSerializer(serializers.ModelSerializer):

    # version = VersionSummarySerializer()
    item = ItemSummarySerializer()

    class Meta:
        model = PokemonItem
        fields = ('rarity', 'item', 'version')



##############################
#  POKEMON STAT SERIALIZERS  #
##############################

class PokemonStatSerializer(serializers.ModelSerializer):

    stat = StatSummarySerializer()

    class Meta:
        model = PokemonStat
        fields = ('base_stat', 'effort', 'stat')



##############################
#  POKEMON TYPE SERIALIZERS  #
##############################

class PokemonTypeSerializer(serializers.ModelSerializer):

    type = TypeSummarySerializer()

    class Meta:
        model = PokemonType
        """
        Hiding Pokemon field
        """
        fields = ('slot', 'type')



#########################
#  POKEMON SERIALIZERS  #
#########################

class PokemonDetailSerializer(serializers.ModelSerializer):
    
    abilities = PokemonAbilitySerializer(many=True, read_only=True, source="pokemonability")
    moves = serializers.SerializerMethodField('get_pokemon_moves')
    species = PokemonSpeciesSummarySerializer(source="pokemon_species")
    stats = PokemonStatSerializer(many=True, read_only=True, source="pokemonstat")
    types = PokemonTypeSerializer(many=True, read_only=True, source="pokemontype")
    forms = PokemonFormSummarySerializer(many=True, read_only=True, source="pokemonform")
    held_items = serializers.SerializerMethodField('get_pokemon_held_items')

    class Meta:
        model = Pokemon
        fields = (
            'id',
            'name', 
            'order',
            'is_default', 
            'height', 
            'weight', 
            'base_experience',
            'species',
            'abilities',
            'stats',
            'types',
            'forms',
            'held_items',
            'moves'
        )

    def get_pokemon_moves(self, obj):
        # Doin moves a little differently because pokemon
        # move resources are a beast

        # Get all possible Version Groups and Move Methods for later use
        version_objects = VersionGroup.objects.all()
        version_data = VersionGroupSummarySerializer(version_objects, many=True, context=self.context).data
        method_objects = MoveLearnMethod.objects.all()
        method_data = MoveLearnMethodSummarySerializer(method_objects, many=True, context=self.context).data

        # Get moves related to this pokemon and pull out unique Move IDs
        pokemon_moves = PokemonMove.objects.filter(pokemon_id=obj).order_by('level')
        move_ids = pokemon_moves.values('move_id').distinct()
        move_list = []

        for id in move_ids:

            pokemon_move_details = OrderedDict()

            # Get each Unique Move by ID
            move_object = Move.objects.get(pk=id['move_id'])
            move_data = MoveSummarySerializer(move_object, context=self.context).data
            pokemon_move_details['move'] = move_data

            # Get Versions and Move Methods associated with each unique move
            pokemon_move_objects = pokemon_moves.filter(move_id=id['move_id'])
            serializer = PokemonMoveSerializer(pokemon_move_objects, many=True, context=self.context)
            pokemon_move_details['version_group_details'] = []

            for move in serializer.data:

                print move

                version_detail = OrderedDict()

                version_detail['level_learned_at'] = move['level']
                version_detail['version_group'] = version_data[move['version_group'] - 1]
                version_detail['move_learn_method'] = method_data[move['move_learn_method'] - 1]

                pokemon_move_details['version_group_details'].append(version_detail)


            move_list.append(pokemon_move_details)

        return move_list

    def get_pokemon_held_items(self, obj):
        # Doin held_items pretty much like moves

        # Get all possible Version Groups and Move Methods for later use
        version_objects = Version.objects.all()
        version_data = VersionSummarySerializer(version_objects, many=True, context=self.context).data

        # Get items related to this pokemon and pull out unique Move IDs
        pokemon_items = PokemonItem.objects.filter(pokemon_id=obj).order_by('item_id')
        item_ids = pokemon_items.values('item_id').distinct()
        item_list = []

        for id in item_ids:

            pokemon_item_details = OrderedDict()

            # Get each Unique Item by ID
            item_object = Item.objects.get(pk=id['item_id'])
            item_data = ItemSummarySerializer(item_object, context=self.context).data
            pokemon_item_details['item'] = item_data

            # Get Versions associated with each unique item
            pokemon_item_objects = pokemon_items.filter(item_id=id['item_id'])
            serializer = PokemonItemSerializer(pokemon_item_objects, many=True, context=self.context)
            pokemon_item_details['version_details'] = []

            for item in serializer.data:

                print item

                version_detail = OrderedDict()

                version_detail['rarity'] = item['rarity']
                version_detail['version'] = version_data[item['version'] - 1]

                pokemon_item_details['version_details'].append(version_detail)

            item_list.append(pokemon_item_details)

        return item_list



#################################
#  POKEMON SPECIES SERIALIZERS  #
#################################

class EvolutionTriggerNameSerializer(serializers.HyperlinkedModelSerializer):

    language = LanguageSummarySerializer()

    class Meta:
        model = EvolutionTriggerName
        fields = ('name', 'language')


class EvolutionTriggerDetailSerializer(serializers.HyperlinkedModelSerializer):

    names = EvolutionTriggerNameSerializer(many=True, read_only=True, source="evolutiontriggername")

    class Meta:
        model = EvolutionTrigger
        fields = ('id', 'name', 'names')


class PokemonDexEntrySerializer(serializers.ModelSerializer):

    entry_number = serializers.IntegerField(source="pokedex_number")
    pokedex = PokedexSummarySerializer()
    
    class Meta:
        model = PokemonDexNumber
        fields = ('entry_number', 'pokedex')


class PokemonSpeciesNameSerializer(serializers.ModelSerializer):

    language = LanguageSummarySerializer()

    class Meta:
        model = PokemonSpeciesName
        fields = ('name', 'genus', 'language')


class PokemonSpeciesEvolutionSerializer(serializers.ModelSerializer):
    """
    This is here purely to help build pokemon evolution chains
    """

    class Meta: 
        model = PokemonSpecies
        fields = ('name', 'id', 'evolves_from_species', 'is_baby')


class PokemonSpeciesDetailSerializer(serializers.ModelSerializer):

    names = serializers.SerializerMethodField('get_pokemon_names')
    pokedex_numbers = PokemonDexEntrySerializer(many=True, read_only=True, source="pokemondexnumber")
    egg_groups = serializers.SerializerMethodField('get_pokemon_egg_groups')
    genera = serializers.SerializerMethodField('get_pokemon_genera')
    generation = GenerationSummarySerializer()
    growth_rate = GrowthRateSummarySerializer()
    color = PokemonColorSummarySerializer(source="pokemon_color")
    habitat = PokemonHabitatSummarySerializer(source="pokemon_habitat")
    shape = PokemonShapeSummarySerializer(source="pokemon_shape")
    evolves_from_species = PokemonSpeciesSummarySerializer()
    varieties = PokemonSummarySerializer(many=True, read_only=True, source="pokemon")
    varieties = serializers.SerializerMethodField('get_pokemon_varieties')
    evolution_chain = EvolutionChainSummarySerializer()

    class Meta: 
        model = PokemonSpecies
        fields = (
            'id',
            'name',
            'order',
            'gender_rate',
            'capture_rate',
            'base_happiness',
            'is_baby',
            'hatch_counter',
            'has_gender_differences',
            'forms_switchable',
            'growth_rate',
            'pokedex_numbers',
            'egg_groups',
            'color',
            'shape',
            'evolves_from_species',
            'evolution_chain',
            'habitat',
            'generation',
            'names',
            'genera',
            'varieties'
        )

    def get_pokemon_names(self, obj):

        species_results = PokemonSpeciesName.objects.filter(pokemon_species=obj)
        species_serializer = PokemonSpeciesNameSerializer(species_results, many=True, context=self.context)

        data  = species_serializer.data

        for name in data:
            del name['genus']

        return data

    def get_pokemon_genera(self, obj):

        results = PokemonSpeciesName.objects.filter(pokemon_species=obj)
        serializer = PokemonSpeciesNameSerializer(results, many=True, context=self.context)
        data = serializer.data
        genera = []

        for entry in data:
            if entry['genus']:
                del entry['name']
                genera.append(entry)

        return genera

    def get_pokemon_egg_groups(self, obj):

        results = PokemonEggGroup.objects.filter(pokemon_species=obj)
        data = PokemonEggGroupSerializer(results, many=True, context=self.context).data
        groups = []
        for group in data:
            groups.append(group['egg_group'])

        return groups

    def get_pokemon_varieties(self, obj):

        results = Pokemon.objects.filter(pokemon_species=obj)
        summary_data = PokemonSummarySerializer(results, many=True, context=self.context).data
        detail_data = PokemonDetailSerializer(results, many=True, context=self.context).data

        varieties = []

        for index, pokemon in enumerate(detail_data):
            entry = OrderedDict()
            entry['is_default'] = pokemon['is_default']
            entry['pokemon'] = summary_data[index]
            varieties.append(entry)

        return varieties


class PokemonEvolutionSerializer(serializers.ModelSerializer):

    item = ItemSummarySerializer(source="evolution_item")
    held_item = ItemSummarySerializer()
    known_move = MoveSummarySerializer()
    known_move_type = TypeSummarySerializer()
    party_species = PokemonSpeciesSummarySerializer()
    party_type = TypeSummarySerializer()
    trade_species = PokemonSpeciesSummarySerializer()
    trigger = EvolutionTriggerSummarySerializer(source="evolution_trigger")

    class Meta:
        model = PokemonEvolution
        fields = (
            'item',
            'trigger',
            'gender',
            'held_item',
            'known_move',
            'known_move_type',
            'location_id',
            'min_level',
            'min_happiness',
            'min_beauty',
            'min_affection',
            'needs_overworld_rain',
            'party_species',
            'party_type',
            'relative_physical_stats',
            'time_of_day',
            'trade_species',
            'turn_upside_down'
        )


class EvolutionChainDetailSerializer(serializers.ModelSerializer):

    baby_trigger_item = ItemSummarySerializer()
    chain = serializers.SerializerMethodField('build_chain')

    class Meta:
        model = EvolutionChain
        fields = (
            'id',
            'baby_trigger_item',
            'chain'
        )

    def build_chain(self, obj):

        chain_id = obj.id

        pokemon_objects = PokemonSpecies.objects.filter(evolution_chain_id=chain_id).order_by('order')
        summary_data = PokemonSpeciesSummarySerializer(pokemon_objects, many=True, context=self.context).data
        ref_data = PokemonSpeciesEvolutionSerializer(pokemon_objects, many=True, context=self.context).data

        chain = entry = OrderedDict()
        current_evolutions = None
        evolution_data = None
        previous_entry = None
        previous_species = None

        for index, species in enumerate(ref_data):

            # If evolves from something
            if species['evolves_from_species']:

                # In case this pokemon is one of multiple evolutions a pokemon can make
                if previous_species['id'] == species['evolves_from_species']:
                    current_evolutions = previous_entry['evolves_to']
                
                entry = OrderedDict()

                evolution_object = PokemonEvolution.objects.filter(evolved_species=species['id'])
                evolution_data = PokemonEvolutionSerializer(evolution_object, many=True, context=self.context).data

                current_evolutions.append(entry)


            entry['is_baby'] = species['is_baby']
            entry['species'] = summary_data[index]
            if evolution_data: entry['evolution_details'] = evolution_data
            entry['evolves_to'] = []

            # Keep track of previous entries for complex chaining
            previous_entry = entry
            previous_species = species

        return chain



class PokemonDexNumberSerializer(serializers.ModelSerializer):

    entry_number = serializers.IntegerField(source="pokedex_number")
    pokemon_species = PokemonSpeciesSummarySerializer(source="pokemon_species")
    
    class Meta:
        model = PokemonDexNumber
        fields = ('pokedex', 'entry_number', 'pokemon_species')



#########################
#  POKEDEX SERIALIZERS  #
#########################

class PokedexDescriptionSerializer(serializers.HyperlinkedModelSerializer):

    language = LanguageSummarySerializer()

    class Meta:
        model = PokedexDescription
        fields = ('name', 'description', 'language')


class PokedexDetailSerializer(serializers.ModelSerializer):
    """
    Name and descriptions for pokedex are stored in a 'prose'
    table so this serializer wont act like the others. Need to build 
    the return data manually.
    """

    region = RegionSummarySerializer()
    names = serializers.SerializerMethodField('get_pokedex_names')
    descriptions = serializers.SerializerMethodField('get_pokedex_descriptions')
    # pokemon_entries = serializers.SerializerMethodField('get_pokedex_entries')

    class Meta:
        model = Pokedex
        fields = ('id', 'name', 'is_main_series', 'region', 'names', 'descriptions',)# 'pokemon_entries')

    def get_pokedex_names(self, obj):

        results = PokedexDescription.objects.filter(pokedex_id=obj)
        serializer = PokedexDescriptionSerializer(results, many=True, context=self.context)
        data  = serializer.data

        for name in data:
            del name['description']

        return data

    def get_pokedex_descriptions(self, obj):

        results = PokedexDescription.objects.filter(pokedex_id=obj)
        serializer = PokedexDescriptionSerializer(results, many=True, context=self.context)
        data = serializer.data

        for name in data:
            del name['name']

        return data

    def get_pokedex_entries(self, obj):

        results = PokemonDexNumber.objects.order_by('pokedex_number').filter(pokedex=obj)
        serializer = PokemonDexNumberSerializer(results, many=True, context=self.context)
        data = serializer.data

        for entry in data:
            del entry['pokedex']

        return data
