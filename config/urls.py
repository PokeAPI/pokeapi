from django.urls import include, path
from pokemon_v2 import urls as pokemon_v2_urls

# pylint: disable=invalid-name

urlpatterns = [
    path("", include(pokemon_v2_urls)),
]
