from __future__ import unicode_literals
from .models import (
    Pokemon, Sprite, Move, Description, Game,
    EggGroup, Type, Ability, Evolution, MovePokemon,
    TypeChart, Pokedex
)
from django.contrib import admin

admin.site.register(Pokemon)
admin.site.register(Sprite)
admin.site.register(Move)
admin.site.register(Description)
admin.site.register(Game)
admin.site.register(EggGroup)
admin.site.register(Type)
admin.site.register(Ability)
admin.site.register(Evolution)
admin.site.register(MovePokemon)
admin.site.register(TypeChart)
admin.site.register(Pokedex)
