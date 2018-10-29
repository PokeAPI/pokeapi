import graphene as g
from pokemon_v2 import models

_languages = [
    (l.name.upper().replace("-", "_"), l.name) for l in models.Language.objects.all()
]
if len(_languages) == 0:
    _languages = [("EN", "en")]

LanguageEnum = g.Enum("LanguageEnum", _languages)
