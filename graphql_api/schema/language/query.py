import graphene as g
from pokemon_v2 import models
from . import types as t
from ..base import BaseQuery


class Query(BaseQuery):
    language = g.Field(t.Language, name=g.ID(required=True))
    languages = g.List(
        t.Language,
        description="A list of languages used for translations of resource information.",
    )

    def resolve_language(self, info, name):
        return info.context.loaders.n_language.load(name)

    def resolve_languages(self, info):
        return models.Language.objects.all()
