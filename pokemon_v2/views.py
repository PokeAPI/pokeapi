# from __future__ import unicode_literals
# from django.http import HttpResponse
# 
from rest_framework.renderers import JSONRenderer
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from pokemon_v2.serializers import (
	AbilitySerializer
)

from pokemon_v2.models import (
	Ability
)


class AbilityResource(viewsets.ReadOnlyModelViewSet):
    queryset = Ability.objects.all()
    serializer_class = AbilitySerializer


# @api_view(['GET', 'POST'])
class TestResource():

	queryset = Ability.objects.all()
	serializer_class = AbilitySerializer

	def get(self, request, pk, format=None):
		return Response("hello Test")
