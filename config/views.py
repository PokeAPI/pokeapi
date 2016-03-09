#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import inspect, re

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

# from pokemon.models import (
#     Pokemon, Sprite, Move, Description, Game,
#     EggGroup, Type, Ability, MovePokemon
# )

from pokemon_v2.models import *
import pokemon_v2.models as models

from hits.models import ResourceView


def convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def _total_site_data():

    """
    Compute the total count of objects on the site

    Using count() is drastically cheaper than len(objects.all())
    """

    # v1
    # data = dict(
    #     pokemon=Pokemon.objects.count(),
    #     sprites=Sprite.objects.count(),
    #     moves=Move.objects.count(),
    #     descriptions=Description.objects.count(),
    #     games=Game.objects.count(),
    #     egg_groups=EggGroup.objects.count(),
    #     types=Type.objects.count(),
    #     abilities=Ability.objects.count(),
    #     move_pokes=MovePokemon.objects.count()
    # )

    data = {}
    resource_count = 0

    for name, obj in inspect.getmembers(models):
        if inspect.isclass(obj):
            try :
                data[convert(name)] = obj.objects.count()
                resource_count += obj.objects.count()
            except(AttributeError):
                pass

    print resource_count

    data['total_lines'] = 0
    data['total_resources'] = resource_count

    print type(data)
    return data


def about(request):

    site_data = _total_site_data()
    total_views = ResourceView.objects.total_count()
    total_v1_views = ResourceView.objects.total_count(version=1)
    total_v2_views = ResourceView.objects.total_count(version=2)

    average_day = int(round(total_views / ResourceView.objects.count()))

    return render_to_response(
        'pages/about.html',
        {
            'total': total_views,
            'total_v1': total_v1_views,
            'total_v2': total_v2_views,
            'average_day': average_day,
            'site_data': site_data,
        },
        context_instance=RequestContext(request)
    )


def home(request):

    total_views = ResourceView.objects.total_count()

    if total_views > 100:
        total_views = int(round(total_views, -2))

    return render_to_response(
        'pages/home.html',
        {
            'total_views': total_views,
        },
        context_instance=RequestContext(request)
    )
