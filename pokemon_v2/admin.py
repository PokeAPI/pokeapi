from __future__ import unicode_literals
from django.contrib import admin

from .models import *

admin.site.register(Ability)
admin.site.register(AbilityName)
admin.site.register(AbilityDescription)
admin.site.register(AbilityFlavorText)
