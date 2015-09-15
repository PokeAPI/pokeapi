
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



#########################
#  POKEMON SERIALIZERS  #
#########################

class PokemonSummarySerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Pokemon
        fields = ('name', 'url')


class PokemonDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Pokemon


class PokemonDexNumberSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PokemonDexNumber



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
    # pokemon = PokemonDexNumberSerializer(many=True, read_only=True, source="pokedex")
    pokemon = serializers.SerializerMethodField('get_pokedex_entries')

    class Meta:
        model = Pokedex
        fields = ('id', 'name', 'is_main_series', 'region', 'names', 'descriptions', 'pokemon')

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
        data  = serializer.data

        for name in data:
            del name['name']

        return data

    def get_pokedex_entries(self, obj):

        results = PokemonDexNumber.objects.filter(pokedex=obj)
        serializer = PokemonDexNumberSerializer(results, many=True, context=self.context)
        return serializer.data



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
        

class MoveSerializer(serializers.ModelSerializer):
    """
    Serializer for the Move resource
    """
    class Meta:
        model = Move


class NatureSerializer(serializers.ModelSerializer):
    """
    Serializer for the Nature resource
    """
    class Meta:
        model = Nature
