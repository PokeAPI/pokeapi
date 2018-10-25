from django.conf.urls import include, url
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

from pokemon_v2 import urls as pokemon_v2_urls
from graphql_api.schema import schema

# pylint: disable=invalid-name

urlpatterns = [
    url(r"^", include(pokemon_v2_urls)),
    url(r"^graphql", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
]
