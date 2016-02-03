#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from pokemon.models import (
    Pokemon, Sprite, Move, Description, Game,
    EggGroup, Type, Ability, MovePokemon
)

from hits.models import ResourceView


def _total_site_data():
    """
    Compute the total count of objects on the site

    Using count() is drastically cheaper than len(objects.all())
    """

    data = dict(
        pokemon=Pokemon.objects.count(),
        sprites=Sprite.objects.count(),
        moves=Move.objects.count(),
        descriptions=Description.objects.count(),
        games=Game.objects.count(),
        egg_groups=EggGroup.objects.count(),
        types=Type.objects.count(),
        abilities=Ability.objects.count(),
        move_pokes=MovePokemon.objects.count()
    )

    t = 0
    for i in data.iteritems():
        t += i[1]

    data['total_items'] = t

    return data


@login_required
def moderate(request):

    return render_to_response(
        'pages/moderate.html',
        {}, context_instance=RequestContext(request))


def about(request):

    site_data = _total_site_data()

    total_views = ResourceView.objects.total_count()

    average_day = int(round(total_views / ResourceView.objects.count()))

    return render_to_response(
        'pages/about.html',
        {
            'total': total_views,
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


def twilio(request):

    return render_to_response(
        'pages/twilio.html',
        {}, context_instance=RequestContext(request))
