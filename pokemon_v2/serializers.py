from __future__ import unicode_literals
"""
PokeAPI v2 serializers
"""

from rest_framework import serializers

from pokemon_v2.models import (
    Ability,
    Move,
    Nature,
    Type
)


class MoveSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Move resource
    """

    class Meta:
        model = Move


class NatureSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Nature resource
    """

    class Meta:
        model = Nature


class TypeSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Type resource
    """

    class Meta:
        model = Type


class AbilitySerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Ability resource
    """

    class Meta:
        model = Ability
