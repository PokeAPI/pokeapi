import graphene as g
from pokemon_v2 import models
from . import types
from ..base import BaseQuery


class Query(BaseQuery):
    characteristic = g.Field(types.Characteristic, id_name=g.ID(required=True))
    characteristics = g.List(
        types.Characteristic,
        description='A list of characteristics (e.g. "Loves to eat, Alert to sounds").',
    )

    def resolve_characteristic(self, info, id_name):
        return info.context.loaders.characteristic.load(id_name)

    def resolve_characteristics(self, info):
        return models.Characteristic.objects.all()
