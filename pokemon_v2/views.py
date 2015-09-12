
from __future__ import unicode_literals
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
import re


###########################
#  BEHAVOIR ABSTRACTIONS  #
###########################

class ListOrDetailSerialRelation():
    """
    Mixin to allow association with separate serializers
    for list or detail view.
    """

    list_serializer_class = None

    def get_serializer_class(self):
        if (self.action == 'list' and self.list_serializer_class != None):
            return self.list_serializer_class
        return self.serializer_class


class NameOrIdRetrieval():
    """
    Mixin to allow retrieval of resources by 
    pk (in this case ID) or by name
    """

    idPattern = re.compile("^[0-9]+$")
    namePattern = re.compile("^[0-9A-Za-z\-]+$")

    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        lookup =  self.kwargs['pk']

        if self.idPattern.match(lookup):
            resp = get_object_or_404(queryset, pk=lookup)

        elif self.namePattern.match(lookup):
            resp = get_object_or_404(queryset, name=lookup)

        else:
            resp = get_object_or_404(queryset, pk="")
        
        return resp


class PokeapiCommonViewset(ListOrDetailSerialRelation, NameOrIdRetrieval, viewsets.ReadOnlyModelViewSet):
    pass


##########
#  APIS  #
##########

class AbilityResource(PokeapiCommonViewset):

    queryset = Ability.objects.all()
    serializer_class = AbilityDetailSerializer
    list_serializer_class = AbilitySummarySerializer


class GenerationResource(PokeapiCommonViewset):

    queryset = Generation.objects.all()
    serializer_class = GenerationDetailSerializer
    list_serializer_class = GenerationSummarySerializer

class LanguageResource(PokeapiCommonViewset):

    queryset = Language.objects.all()
    serializer_class = LanguageDetailSerializer


class MoveResource(PokeapiCommonViewset):

    queryset = Move.objects.all()
    serializer_class = MoveSerializer


class NatureResource(PokeapiCommonViewset):

    queryset = Nature.objects.all()
    serializer_class = NatureSerializer


class PokemonResource(PokeapiCommonViewset):

    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer


class RegionResource(PokeapiCommonViewset):

    queryset = Region.objects.all()
    serializer_class = RegionDetailSerializer
    list_serializer_class = RegionSummarySerializer


class TypeResource(PokeapiCommonViewset):

    queryset = Type.objects.all()
    serializer_class = TypeDetailSerializer
    list_serializer_class = TypeSummarySerializer


class VersionResource(PokeapiCommonViewset):

    queryset = Version.objects.all()
    serializer_class = VersionDetailSerializer
    list_serializer_class = VersionSummarySerializer


class VersionGroupResource(PokeapiCommonViewset):

    queryset = VersionGroup.objects.all()
    serializer_class = VersionGroupDetailSerializer
    list_serializer_class = VersionGroupSummarySerializer
