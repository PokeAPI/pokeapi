
from __future__ import unicode_literals
from rest_framework import serializers

"""
PokeAPI v2 serializers
"""

from .models import *


class AbilitySerializer(serializers.ModelSerializer):
    """
    Serializer for the Ability resource
    """
    class Meta:
        model = Ability


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