
from __future__ import unicode_literals
from rest_framework import serializers
from collections import OrderedDict

"""
PokeAPI v2 serializers in order of dependency
"""

from .models import *


##########################
#  LANGUAGE SERIALIZERS  #
##########################

class LanguageNameSerializer(serializers.ModelSerializer):

    local_language_url = serializers.HyperlinkedRelatedField(read_only='True', source="local_language_id", view_name='language-detail')

    class Meta:
        model = LanguageName
        fields = ('name', 'local_language_url')


class LanguageSummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Language
        fields = ('name', 'url')


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


class RegionSummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Region
        fields = ('name', 'url')


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


class GenerationSummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Generation
        fields = ('name', 'url')


class GenerationDetailSerializer(serializers.ModelSerializer):

    region = RegionSummarySerializer()
    names = GenerationNameSerializer(many=True, read_only=True, source="generationname")

    class Meta:
        model = Generation
        fields = ('id', 'name', 'region', 'names')


############################
#  GENERATION SERIALIZERS  #
############################

class GrowthRateDescriptionSerializer(serializers.ModelSerializer):

    language = LanguageSummarySerializer()

    class Meta:
        model = GrowthRateDescription
        fields = ('description', 'language')


class GrowthRateSummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = GrowthRate
        fields = ('name', 'url')


class GrowthRateDetailSerializer(serializers.ModelSerializer):

    descriptions = GrowthRateDescriptionSerializer(many=True, read_only=True, source="growthratedescription")

    class Meta:
        model = GrowthRate
        fields = ('id', 'name', 'formula', 'descriptions')


#########################
#  VERSION SERIALIZERS  #
#########################

class VersionNameSerializer(serializers.ModelSerializer):

    language = LanguageSummarySerializer()

    class Meta:
        model = VersionName
        fields = ('name', 'language')


class VersionSummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Version
        fields = ('name', 'url')


class VersionDetailSerializer(serializers.ModelSerializer):
    """
    Should have a link to Version Group info but the Circular
    dependency and compilation order fight eachother and I'm
    not sure how to add anything other than a hyperlink
    """

    names = VersionNameSerializer(many=True, read_only=True, source="versionname")
    version_group_url = serializers.HyperlinkedRelatedField(read_only='True', source="version_group", view_name='versiongroup-detail')

    class Meta:
        model = Version
        fields = ('id', 'name', 'names', 'version_group_url')


class VersionGroupSummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = VersionGroup
        fields = ('name', 'url')


class VersionGroupDetailSerializer(serializers.ModelSerializer):

    generation = GenerationSummarySerializer()
    versions = VersionSummarySerializer(many=True, read_only=True, source="version")

    class Meta:
        model = VersionGroup
        fields = ('id', 'name', 'order', 'generation', 'versions')


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


class AbilitySummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Ability
        fields = ('name', 'url')


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

class StatSummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Stat
        fields = ('name', 'url')


class StatDetailSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Stat



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


class TypeSummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Type
        fields = ('name', 'url')


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


class MoveDamageClassSummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = MoveDamageClass
        fields = ('name', 'url')


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

class MoveMetaAilmentSummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = MoveMetaAilment
        fields = ('name', 'url')


class MoveMetaAilmentDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = MoveMetaAilment


class MoveMetaCategorySummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = MoveMetaCategory
        fields = ('name', 'url')


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


class MoveTargetSummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = MoveTarget
        fields = ('name', 'url')


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


class MoveSummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Move
        fields = ('name', 'url')


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


class PokemonColorSummarySerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = PokemonColor
        fields = ('name', 'url')


class PokemonColorDetailSerializer(serializers.ModelSerializer):

    names = PokemonColorNameSerializer(many=True, read_only=True, source="pokemoncolorname")
    
    class Meta:
        model = PokemonColor
        fields = ('id', 'name', 'names')



##############################
#  POKEMON FORM SERIALIZERS  #
##############################

class PokemonFormSerializer(serializers.ModelSerializer):

    version_group = VersionGroupSummarySerializer()
    
    class Meta:
        model = PokemonForm
        # fields = (
        #     'form_name', 
        #     'is_default',
        #     'is_battle_only',
        #     'is_mega',
        #     'form_order',
        #     'version_group'
        # )



##############################
#  POKEMON MOVE SERIALIZERS  #
##############################

class MoveLearnMethodSummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = MoveLearnMethod
        fields = ('name', 'url')


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

    # move = MoveSummarySerializer()
    # move_method = PokemonMoveMethodSummarySerializer(source="pokemon_move_method")
    # version_group = VersionGroupSummarySerializer()
    
    class Meta:
        model = PokemonMove
        # fields = ('level', 'move_method', 'move', 'version_group')



###############################
#  POKEMON SHAPE SERIALIZERS  #
###############################

class PokemonShapeNameSerializer(serializers.HyperlinkedModelSerializer):

    language = LanguageSummarySerializer()

    class Meta:
        model = PokemonShapeName
        fields = ('name', 'awesome_name', 'language')


class PokemonShapeSummarySerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = PokemonShape
        fields = ('name', 'url')


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



#################################
#  POKEMON SPECIES SERIALIZERS  #
#################################

class PokemonSpeciesNameSerializer(serializers.ModelSerializer):

    language = LanguageSummarySerializer()

    class Meta:
        model = PokemonSpeciesName
        fields = ('name', 'genus', 'language')


class PokemonSpeciesSummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta: 
        model = PokemonSpecies
        fields = ('name', 'url')


class PokemonSpeciesDetailSerializer(serializers.ModelSerializer):

    names = serializers.SerializerMethodField('get_pokemon_names')
    genera = serializers.SerializerMethodField('get_pokemon_genera')
    generation = GenerationSummarySerializer()
    growth_rate = GrowthRateSummarySerializer()
    pokemon_color = PokemonColorSummarySerializer()
    pokemon_shape = PokemonShapeSummarySerializer()
    # varieties = PokemonDetailSerializer(many=True, read_only=True, source="pokemon")
    # types = TypeSummarySerializer(many=True, read_only=True, source="pokemonspecies")

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
            'pokemon_color',
            'pokemon_shape',
            'evolves_from_species',
            'evolution_chain',
            'pokemon_habitat',
            'generation',
            # 'types',
            'names',
            'genera',
            # 'varieties'
        )

    def get_pokemon_names(self, obj):

        results = PokemonSpeciesName.objects.filter(pokemon_species=obj)
        serializer = PokemonSpeciesNameSerializer(results, many=True, context=self.context)
        data  = serializer.data

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

    # def get_pokemon_types()



##############################
#  POKEMON STAT SERIALIZERS  #
##############################

class PokemonStatSerializer(serializers.ModelSerializer):

    stat = StatSummarySerializer()

    class Meta:
        model = PokemonStat
        """
        Hiding Pokemon and ID fields
        """
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

class PokemonSummarySerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Pokemon
        fields = ('name', 'url')


class PokemonDetailSerializer(serializers.ModelSerializer):
    
    abilities = PokemonAbilitySerializer(many=True, read_only=True, source="pokemonability")
    # moves = PokemonMoveSerializer(many=True, read_only=True, source="pokemonmove")
    moves = serializers.SerializerMethodField('get_pokemon_moves')
    stats = PokemonStatSerializer(many=True, read_only=True, source="pokemonstat")
    types = PokemonTypeSerializer(many=True, read_only=True, source="pokemontype")
    # forms = PokemonFormSerializer(many=True, read_only=True, source="pokemonform")

    class Meta:
        model = Pokemon
        fields = (
            'id', 
            'order', 
            'name', 
            'is_default', 
            'height', 
            'weight', 
            'base_experience', 
            'abilities',
            'moves',
            'stats',
            'types'
            # 'forms',
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
        pokemon_moves = PokemonMove.objects.filter(pokemon_id=obj).order_by('move_id')
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
            pokemon_move_details['version_details'] = []

            for move in serializer.data:

                version_detail = OrderedDict()

                version_detail['level_learned_at'] = move['level']
                version_detail['version_group'] = version_data[move['version_group'] - 1]
                version_detail['move_learn_method'] = method_data[move['move_learn_method'] - 1]

                pokemon_move_details['version_details'].append(version_detail)


            move_list.append(pokemon_move_details)

        return move_list




class PokemonDexNumberSerializer(serializers.ModelSerializer):

    entry_number = serializers.IntegerField(source="pokedex_number")
    pokemon = PokemonSpeciesSummarySerializer(source="pokemon_species")
    
    class Meta:
        model = PokemonDexNumber
        fields = ('pokedex', 'entry_number', 'pokemon')



#########################
#  POKEDEX SERIALIZERS  #
#########################

class PokedexDescriptionSerializer(serializers.HyperlinkedModelSerializer):

    language = LanguageSummarySerializer()

    class Meta:
        model = PokedexDescription
        fields = ('name', 'description', 'language')


class PokedexSummarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Pokedex


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


#######################
#  BERRY SERIALIZERS  #
#######################

class BerrySerializer(serializers.ModelSerializer):
    """
    Serializer for the Berry resource
    """
    class Meta:
        model = Berry


class CharacteristicSerializer(serializers.ModelSerializer):
    """
    Serializer for the Characteristic resource
    """
    class Meta:
        model = Characteristic


class EggGroupSerializer(serializers.ModelSerializer):
    """
    Serializer for the EggGroup resource
    """
    class Meta:
        model = EggGroup


class EncounterSerializer(serializers.ModelSerializer):
    """
    Serializer for the Encounter resource
    """
    class Meta:
        model = Encounter


class GenderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Gender resource
    """
    class Meta:
        model = Gender


class GrowthRateSerializer(serializers.ModelSerializer):
    """
    Serializer for the GrowthRate resource
    """
    class Meta:
        model = GrowthRate


class ItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the Item resource
    """
    class Meta:
        model = Item


class LocationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Location resource
    """
    class Meta:
        model = Location


class NatureSerializer(serializers.ModelSerializer):
    """
    Serializer for the Nature resource
    """
    class Meta:
        model = Nature
