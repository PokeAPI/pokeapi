
from __future__ import unicode_literals
from rest_framework import serializers

"""
PokeAPI v2 serializers
"""

from pokemon.models import (
    Sprite
)

from .models import (
    Ability,
    Move,
    Nature,
    Type
)


class AbilitySerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Ability resource
    """

    class Meta:
        model = Ability
        

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


class SpriteSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Type resource
    """

    class Meta:
        model = Sprite


class TypeSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Type resource
    """

    class Meta:
        model = Type
