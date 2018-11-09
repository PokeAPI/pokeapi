import graphene as g
from pokemon_v2 import models

# This module must be loaded lazily

_languages = [
    (l.name.upper().replace("-", "_"), l.name) for l in models.Language.objects.all()
]
if not _languages:
    _languages = [("EN", "en")]

LanguageEnum = g.Enum("LanguageEnum", _languages)
