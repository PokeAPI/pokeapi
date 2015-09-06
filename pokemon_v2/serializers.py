from rest_framework import serializers
from pokemon_v2.models import (
	Ability
)


class AbilitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ability
        fields = ('id', 'name', 'generation', 'is_main_series')
