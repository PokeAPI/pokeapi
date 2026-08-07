from django.urls import include, path

from pokemon_v2 import urls as pokemon_v2_urls

urlpatterns = [
    path("", include(pokemon_v2_urls)),
]
