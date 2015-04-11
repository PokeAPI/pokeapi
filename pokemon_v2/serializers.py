from __future__ import unicode_literals
"""
PokeAPI v2 serializers
"""

from rest_framework import serializers

from pokemon_v2.models import (
    Move
)


class MoveSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Move resource
    """

    class Meta:
        model = Move
