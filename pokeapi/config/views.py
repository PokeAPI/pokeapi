#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.cache import cache
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from alerts.models import Alert
from hits.models import ResourceView

import stripe


def about(request):

    total_views = cache.get('total_views')
    if not total_views:
        total_views = ResourceView.objects.total_count()
        cache.set('total_views', total_views)

    average_day = cache.get('average_day')
    if not average_day:
        average_day = int(round(total_views / ResourceView.objects.count()))
        cache.set('average_day', average_day)

    alert = cache.get('alert')
    if not alert:
        active_alerts = Alert.objects.filter(active=True)
        if active_alerts:
            cache.set('alert', active_alerts.first())
        alert = active_alerts.first()

    return render_to_response(
        'pages/about.html',
        {
            'total': total_views,
            'average_day': average_day,
            'alert': alert
        },
        context_instance=RequestContext(request)
    )


def home(request):

    total_views = cache.get('total_views')
    if not total_views:
        total_views = ResourceView.objects.total_count()
        total_views = int(round(total_views, -2))
        cache.set('total_views', total_views)

    stripe_key = settings.STRIPE_KEYS['publishable']

    alert = cache.get('alert')
    if not alert:
        active_alerts = Alert.objects.filter(active=True)
        if active_alerts:
            cache.set('alert', active_alerts.first())
        alert = active_alerts.first()

    return render_to_response(
        'pages/home.html',
        {
            'total_views': total_views,
            'stripe_key': stripe_key,
            'alert': alert
        },
        context_instance=RequestContext(request)
    )


@csrf_exempt
def stripe_donation(request):
    if request.method == 'POST':
        # Amount in cents
        amount = 1000

        stripe.api_key = settings.STRIPE_KEYS['secret']

        customer = stripe.Customer.create(
            email=request.POST.get('stripeEmail', ''),
            card=request.POST.get('stripeToken', '')
        )

        try:
            stripe.Charge.create(
                customer=customer.id,
                amount=amount,
                currency='usd',
                description='PokeAPI donation'
            )
        except:
            return redirect('/')

        return redirect('/')
    return redirect('/')
