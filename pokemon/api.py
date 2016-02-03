from __future__ import unicode_literals
"""
This file holds all the API logic for pokeapi v1
"""
from django.conf.urls import url

from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from tastypie.cache import SimpleCache

from .models import (
    Pokemon, Sprite, Move, Description, Game,
    EggGroup, Type, Ability, Pokedex
)
from hits.models import ResourceView


class PokedexResource(ModelResource):

    class Meta:
        queryset = Pokedex.objects.all()
        resource_name = 'pokedex'
        authorization = Authorization()
        allowed_methods = ['get']
        cache = SimpleCache(timeout=360)
        excludes = ['id']

    def dehydrate(self, bundle):
        bundle.data['pokemon'] = bundle.obj.pokemon
        return bundle


class PokemonResource(ModelResource):

    class Meta:
        queryset = Pokemon.objects.all()
        resource_name = 'pokemon'
        authorization = Authorization()
        allowed_methods = ['get']
        excludes = ['id']
        pkdx_uri_name = 'pkdx_id'
        name_uri_name = 'name'
        cache = SimpleCache(timeout=360)

    def build_descriptions(self, name):
        ds = Description.objects.filter(name__icontains=name)
        lst = []
        if ds.exists():
            for d in ds:
                lst.append(dict(
                    name=d.name,
                    resource_uri='/api/v1/description/' + str(d.id) + '/'
                )
                )

        return lst

    def dehydrate(self, bundle):
        ResourceView.objects.increment_view_count(version=1)
        bundle.data['name'] = bundle.obj.name.capitalize()
        bundle.data['abilities'] = bundle.obj.ability_list
        bundle.data['types'] = bundle.obj.type_list
        bundle.data['national_id'] = bundle.obj.pkdx_id
        bundle.data['evolutions'] = bundle.obj.evolutions
        bundle.data['egg_groups'] = bundle.obj.eggs
        bundle.data['moves'] = bundle.obj.moves
        bundle.data['sprites'] = bundle.obj.my_sprites
        bundle.data['descriptions'] = self.build_descriptions(bundle.obj.name)
        uri = '/api/v1/pokemon/' + str(bundle.obj.pkdx_id) + '/'
        bundle.data['resource_uri'] = uri
        return bundle

    def prepend_urls(self):
        return [
            url(
                r"^(?P<resource_name>%s)/(?P<pkdx_id>\d+)/$"
                % self._meta.resource_name, self.wrap_view('dispatch_detail'),
                name="api_dispatch_detail_pkdx"),
            url(
                r"^(?P<resource_name>%s)/(?P<name>[\w\d_.-]+)/$"
                % self._meta.resource_name, self.wrap_view('dispatch_detail'),
                name="api_dispatch_detail_name"),
        ]


class TypeResource(ModelResource):

    class Meta:
        queryset = Type.objects.all()
        resource_name = 'type'
        authorization = Authorization()
        allowed_methods = ['get']
        cache = SimpleCache(timeout=360)

    def dehydrate(self, bundle):
        ResourceView.objects.increment_view_count(version=1)
        bundle.data['name'] = bundle.obj.name.capitalize()
        bundle.data['weakness'] = bundle.obj.weaknesses
        bundle.data['resistance'] = bundle.obj.resistances
        bundle.data['super_effective'] = bundle.obj.supers
        bundle.data['ineffective'] = bundle.obj.ineffectives
        bundle.data['no_effect'] = bundle.obj.no_effects
        return bundle


class AbilityResource(ModelResource):

    class Meta:
        queryset = Ability.objects.all()
        resource_name = 'ability'
        authorization = Authorization()
        allowed_methods = ['get']
        cache = SimpleCache(timeout=360)

    def dehydrate(self, bundle):
        ResourceView.objects.increment_view_count(version=1)
        bundle.data['name'] = bundle.obj.name.capitalize()
        bundle.data['description'] = unicode(bundle.obj.description)
        return bundle


class GameResource(ModelResource):

    class Meta:
        queryset = Game.objects.all()
        resource_name = 'game'
        authorization = Authorization()
        allowed_methods = ['get']
        cache = SimpleCache(timeout=360)

    def dehydrate(self, bundle):
        ResourceView.objects.increment_view_count(version=1)
        bundle.data['name'] = bundle.obj.name.capitalize()
        return bundle


class SpriteResource(ModelResource):

    class Meta:
        queryset = Sprite.objects.all()
        resource_name = 'sprite'
        authorization = Authorization()
        allowed_methods = ['get']
        cache = SimpleCache(timeout=360)

    def dehydrate(self, bundle):
        ResourceView.objects.increment_view_count(version=1)
        bundle.data['name'] = bundle.obj.name.capitalize()
        bundle.data['pokemon'] = bundle.obj.pokemon
        return bundle


class DescriptionResource(ModelResource):

    class Meta:
        queryset = Description.objects.all()
        resource_name = 'description'
        authorization = Authorization()
        allowed_methods = ['get']
        cache = SimpleCache(timeout=360)

    def dehydrate(self, bundle):
        ResourceView.objects.increment_view_count(version=1)
        bundle.data['name'] = bundle.obj.name.capitalize()
        bundle.data['games'] = bundle.obj.n_game
        bundle.data['pokemon'] = bundle.obj.pokemon
        return bundle


class EggResource(ModelResource):

    class Meta:
        queryset = EggGroup.objects.all()
        resource_name = 'egg'
        authorization = Authorization()
        allowed_methods = ['get']
        cache = SimpleCache(timeout=360)

    def dehydrate(self, bundle):
        ResourceView.objects.increment_view_count(version=1)
        bundle.data['name'] = bundle.obj.name.capitalize()
        bundle.data['pokemon'] = bundle.obj.pokemon
        return bundle


class MoveResource(ModelResource):

    class Meta:
        queryset = Move.objects.all()
        resource_name = 'move'
        authorization = Authorization()
        allowed_methods = ['get']
        cache = SimpleCache(timeout=360)

    def dehydrate(self, bundle):
        ResourceView.objects.increment_view_count(version=1)
        bundle.data['name'] = bundle.obj.name.capitalize()
        return bundle
