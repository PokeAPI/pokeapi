
from __future__ import unicode_literals
from rest_framework import viewsets

from pokemon.models import (

    Sprite
)

from .models import (
	Ability
)

from .serializers import (
	AbilitySerializer, SpriteSerializer
)

class SpriteResource(viewsets.ReadOnlyModelViewSet):
    """
    Views for the Sprite V2 Resource
    """

    queryset = Sprite.objects.all()
    serializer_class = SpriteSerializer

class AbilityResource(viewsets.ReadOnlyModelViewSet):
    """
    Views for the Ability V2 Resource
    """

    queryset = Ability.objects.all()
    serializer_class = AbilitySerializer
