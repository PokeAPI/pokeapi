
from __future__ import unicode_literals
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
import re


class NameOrIdLookupMixin(viewsets.ReadOnlyModelViewSet):
    """
    This will allow a resource to be looked up by name or id (pk in this case).
    """
    idPattern = re.compile("^[0-9]+$")
    namePattern = re.compile("^[0-9A-Za-z\-]+$")

    def get_object(self):

        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        lookup =  self.kwargs['pk']

        if (self.idPattern.match(lookup)):
            resp = get_object_or_404(queryset, pk=lookup)

        elif (self.namePattern.match(lookup)):
            resp = get_object_or_404(queryset, name=lookup)

        else:
            resp = get_object_or_404(queryset, pk="")
        
        return resp


class AbilityResource(NameOrIdLookupMixin):
    """
    Views for the Ability V2 Resource
    """
    queryset = Ability.objects.all()
    serializer_class = AbilitySerializer


class GenerationResource(NameOrIdLookupMixin):
    """
    Views for the Generation V2 Resource
    """
    queryset = Generation.objects.all()
    serializer_class = GenerationSerializer


class MoveResource(NameOrIdLookupMixin):
    """
    Views for the Move V2 Resource
    """
    queryset = Move.objects.all()
    serializer_class = MoveSerializer


class NatureResource(NameOrIdLookupMixin):
    """
    Views for the Nature V2 Resource
    """
    queryset = Nature.objects.all()
    serializer_class = NatureSerializer


class PokemonResource(NameOrIdLookupMixin):
    """
    Views for the Pokemon V2 Resource
    """
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer


class TypeResource(NameOrIdLookupMixin):
    """
    Views for the Type V2 Resource
    """
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


