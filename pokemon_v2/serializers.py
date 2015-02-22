from __future__ import unicode_literals
"""
PokeAPI v2 serializers
"""

from urlparse import urljoin

from rest_framework import serializers

from config.settings import BASE_URL

from pokemon.models import (
    Ability,
    EggGroup,
    Game,
    Move,
    Pokemon,
    Pokedex,
    Sprite,
    Type
)



class PokemonSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Pokemon resource
    """

    class Meta:
        model = Pokemon
        fields = (
            'name',
            'pkdx_id'
            'species',
            'height',
            'weight',
            'ev_yield',
            'catch_rate',
            'happiness',
            'exp',
            'growth_rate',
            'male_female_ratio',
            'hp',
            'attack',
            'defense',
            'sp_atk',
            'sp_def',
            'speed',
            'total',
            'egg_cycles',
            'abilities',
            'types',
            'evolutions', # Will need some hacking
            'egg_group',
            'descriptions',
            'sprites',
            'moves',
            'modified',
            'created',
        )


class PokedexSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Pokedex resource
    """

    class Meta:
        model = Pokedex
        fields = (
            'name',
            'pokemon',
            'modified',
            'created',
        )


class SpriteSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Sprite resource
    """

    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        return urljoin(BASE_URL, obj.image.url)

    class Meta:
        model = Sprite
        fields = (
            'name',
            'image',
            'modified',
            'created',
        )


class AbilitySerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Ability resource
    """

    class Meta:
        model = Ability
        fields = (
            'name',
            'description',
            'modified',
            'created',
        )


class TypeSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Type resource
    """

    class Meta:
        model = Type
        fields = (
            'name',
            'weaknesses',
            'resistances',
            'supers',
            'ineffectives',
            'no_effects',
            'modified',
            'created',
        )


class GameSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Game resource
    """

    class Meta:
        model = Game
        fields = (
            'name',
            'generation',
            'release_year',
            'modified',
            'created',
        )


class EggGroupSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Egg resource
    """

    class Meta:
        model = EggGroup
        fields = (
            'name',
            'pokemon',
            'modified',
            'created',
        )


class MoveSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Move resource
    """

    class Meta:
        model = Move
        fields = (
            'name',
            'description',
            'etype',
            'pp',
            'category',
            'power',
            'accuracy',
            'modified',
            'created',
        )
