from __future__ import unicode_literals


from pokemon.models import Sprite

from .serializers import SpriteSerializer

from rest_framework import viewsets


class SpriteResource(viewsets.ReadOnlyModelViewSet):
    """
    Views for the Sprite V2 Resource
    """

    queryset = Sprite.objects.all()
    serializer_class = SpriteSerializer
