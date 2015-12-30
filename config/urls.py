# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from pokemon import urls as pokemon_urls
from pokemon_v2 import urls as pokemon_v2_urls

urlpatterns = [
    
    url(r'^', include(pokemon_urls)),

    url(r'^', include(pokemon_v2_urls)),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^media/(?P<path>.*)',
        'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),

    url(r'^static/(?P<path>.*)',
        'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT}),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)