# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()


##################################
#
#   V1 API setup using Tastypie
# 
##################################

from tastypie.api import Api

from pokemon.api import (
    PokemonResource, TypeResource, AbilityResource, GameResource,
    SpriteResource, DescriptionResource, EggResource, MoveResource,
    PokedexResource
)

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


#####################################
#
#   V2 API setup using Django Rest
# 
#####################################

from rest_framework import routers
from pokemon_v2.views import *

router = routers.DefaultRouter()

router.register(r"ability", AbilityResource)
router.register(r"berry", BerryResource)
router.register(r"berry-firmness", BerryFirmnessResource)
router.register(r"berry-flavor", BerryFlavorResource)
router.register(r"characteristic", CharacteristicResource)
router.register(r"contest-type", ContestTypeResource)
router.register(r"contest-effect", ContestEffectResource)
router.register(r"egg-group", EggGroupResource)
router.register(r"encounter-method", EncounterMethodResource) # ?
router.register(r"encounter-condition", EncounterConditionResource) # ?
router.register(r"encounter-condition-value", EncounterConditionValueResource) # ?
router.register(r"evolution-chain", EvolutionChainResource)
router.register(r"evolution-trigger", EvolutionTriggerResource)
router.register(r"generation", GenerationResource)
router.register(r"gender", GenderResource)
router.register(r"growth-rate", GrowthRateResource)
router.register(r"item", ItemResource)
router.register(r"item-category", ItemCategoryResource)
router.register(r"item-attribute", ItemAttributeResource)
router.register(r"item-fling-effect", ItemFlingEffectResource)
router.register(r"item-pocket", ItemPocketResource)
router.register(r"language", LanguageResource)
router.register(r"location", LocationResource)
router.register(r"location-area", LocationAreaResource)
router.register(r"move", MoveResource)
router.register(r"move-ailment", MoveMetaAilmentResource)
router.register(r"move-battle-style", MoveBattleStyleResource)
router.register(r"move-category", MoveMetaCategoryResource)
router.register(r"move-damage-class", MoveDamageClassResource)
router.register(r"move-learn-method", MoveLearnMethodResource)
router.register(r"move-target", MoveTargetResource)
router.register(r"nature", NatureResource)
router.register(r"pal-park-area", PalParkAreaResource)
router.register(r"pokedex", PokedexResource)
router.register(r"pokemon", PokemonResource)
router.register(r"pokemon-color", PokemonColorResource)
router.register(r"pokemon-form", PokemonFormResource)
router.register(r"pokemon-habitat", PokemonHabitatResource)
router.register(r"pokemon-shape", PokemonShapeResource)
router.register(r"pokemon-species", PokemonSpeciesResource)
router.register(r"pokeathlon-stat", PokeathlonStatResource)
router.register(r"region", RegionResource)
router.register(r"stat", StatResource)
router.register(r"super-contest-effect", SuperContestEffectResource)
router.register(r"type", TypeResource)
router.register(r"version", VersionResource)
router.register(r"version-group", VersionGroupResource)


###########################
#
#   Gotta Get Em' All
# 
###########################

urlpatterns = patterns(

    '',

    url(r'^$', 'config.views.home'),

    url(r'^docs/$',
        TemplateView.as_view(template_name='pages/docs.html'),
        name="documentation"),

    url(r'^about/$', 'config.views.about'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^api/', include(api_resources.urls)),

    url(r'^api/v2/', include(router.urls)),

    url(r'^media/(?P<path>.*)',
        'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),

    url(r'^static/(?P<path>.*)',
        'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT}),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
