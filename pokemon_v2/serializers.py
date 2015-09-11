
from __future__ import unicode_literals
from rest_framework import serializers

"""
PokeAPI v2 serializers
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


class AbilityDetailSerializer(serializers.HyperlinkedModelSerializer):

    descriptions = AbilityDescriptionSerializer(many=True, read_only=True, source="abilitydescription")
    flavor_text_entries = AbilityFlavorTextSerializer(many=True, read_only=True, source="abilityflavortext")
    names = AbilityNameSerializer(many=True, read_only=True, source="abilityname")

    # names = serializers.SerializerMethodField('get_names_by_language')
    # descriptions = serializers.SerializerMethodField('get_descriptions_by_language')
    # flavor_text_entries = serializers.SerializerMethodField('get_flavor_text_by_language')

    # def get_names_by_language(self, obj):
    #     language_filter = self.context['request'].query_params['language']
    #     names = AbilityName.objects.filter(ability=obj, language=9)
    #     serializer = AbilityNameSerializer(names, many=True, context=self.context)
    #     return serializer.data

    # def get_flavor_text_by_language(self, obj):
    #     language_filter = self.context['request'].query_params['language']
    #     flavor_text_entries = AbilityFlavorText.objects.filter(ability=obj, language=9)
    #     serializer = AbilityFlavorTextSerializer(flavor_text_entries, many=True, context=self.context)
    #     return serializer.data

    # def get_descriptions_by_language(self, obj):
    #     language_filter = self.context['request'].query_params['language']
    #     descriptions = AbilityDescription.objects.filter(ability=obj, language=9)
    #     serializer = AbilityDescriptionSerializer(descriptions, many=True, context=self.context)
    #     return serializer.data

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



#########################
#  BERRY SERIALIZERS  #
#########################

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


class GenerationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Ability resource
    """
    class Meta:
        model = Generation


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


class LanguageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Language resource
    """
    class Meta:
        model = Language


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


class PokedexSerializer(serializers.ModelSerializer):
    """
    Serializer for the Pokedex resource
    """
    class Meta:
        model = Pokedex


class PokemonSerializer(serializers.ModelSerializer):
    """
    Serializer for the Pokemon resource
    """
    class Meta:
        model = Pokemon


class RegionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Region resource
    """
    class Meta:
        model = Region


class TypeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Type resource
    """
    class Meta:
        model = Type


class VersionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Version resource
    """
    class Meta:
        model = Version