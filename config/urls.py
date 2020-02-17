from django.conf.urls import include, url
from pokemon_v2 import urls as pokemon_v2_urls

# pylint: disable=invalid-name

urlpatterns = [
    url(r"^", include(pokemon_v2_urls)),
]
