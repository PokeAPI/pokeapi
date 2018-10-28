import graphene as g
from pokemon_v2 import models

LanguageEnum = g.Enum(  # pylint: disable=invalid-name
    "LanguageEnum",
    [(l.name.upper().replace("-", "_"), l.name) for l in models.Language.objects.all()],
)
