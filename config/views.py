#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import inspect
import os
import re

from django.shortcuts import render_to_response
from django.template import RequestContext

from hits.models import ResourceView
from pokemon import models as models_v1
from pokemon_v2 import models


# converts CapitalCase to snake_case, for dictionary keys
# makes keys singular, not plural i.e. type, not types, but I
# think it's worth it for consistency and DRYness
def convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def _total_site_data():

    """
    Compute the total count of objects on the site

    Using count() is drastically cheaper than len(objects.all())
    """

    data = {
        'total_resources': 0,
        'total_lines': 0
    }

    # v2 objects count
    for name, obj in inspect.getmembers(models):
        if inspect.isclass(obj) and hasattr(obj, 'objects'):
            data[convert(name)] = obj.objects.count()
            data['total_resources'] += obj.objects.count()

    # v2 line count
    for file_name in os.listdir('data/v2/csv'):
        file_read = open('data/v2/csv/' + file_name)
        data['total_lines'] += sum(1 for row in file_read)
        file_read.close()

    # v1 objects count
    for name, obj in inspect.getmembers(models_v1):
        if inspect.isclass(obj) and hasattr(obj, 'objects'):
            data['total_resources'] += obj.objects.count()

    # v1 line count
    for file_name in os.listdir('data/v1'):
        if file_name.endswith('.csv'):
            file_read = open('data/v1/' + file_name)
            data['total_lines'] += sum(1 for row in file_read)
            file_read.close()

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
