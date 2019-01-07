from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from .views import GraphQLView
from .schema import schema


urlpatterns = [
    url(r"^graphql", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema)))
]
