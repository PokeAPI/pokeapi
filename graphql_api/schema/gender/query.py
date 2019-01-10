import graphene as g
from pokemon_v2 import models
from . import types
from ..base import BaseQuery


class Query(BaseQuery):
    gender = g.Field(types.Gender, id_name=g.ID(required=True))
    genders = g.List(types.Gender, description="A list of genders.")

    def resolve_gender(self, info, id_name):
        return info.context.loaders.n_gender.load(id_name)

    def resolve_genders(self, info):
        return models.Gender.objects.all()
