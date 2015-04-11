from __future__ import unicode_literals
from django.contrib import admin

from .models import *

admin.site.register(Language)
admin.site.register(LanguageName)

admin.site.register(Generation)
admin.site.register(GenerationName)

admin.site.register(Version)
admin.site.register(VersionName)
admin.site.register(VersionGroup)
admin.site.register(VersionGroupRegion)
admin.site.register(VersionGroupPokemonMoveMethod)

admin.site.register(Ability)
admin.site.register(AbilityName)
admin.site.register(AbilityDescription)
admin.site.register(AbilityFlavorText)
