
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import include, url

from tastypie.api import Api

from pokemon.api import (
    PokemonResource, TypeResource, AbilityResource, GameResource,
    SpriteResource, DescriptionResource, EggResource, MoveResource,
    PokedexResource
)


from django.contrib import admin
admin.autodiscover()

##################################
#
#   V1 API setup using Tastypie
#
##################################

api_resources = Api()
api_resources.register(PokemonResource())
api_resources.register(AbilityResource())
api_resources.register(TypeResource())
api_resources.register(GameResource())
api_resources.register(SpriteResource())
api_resources.register(DescriptionResource())
api_resources.register(EggResource())
api_resources.register(MoveResource())
api_resources.register(PokedexResource())

urlpatterns = [

    url(r'^api/', include(api_resources.urls)),
]
