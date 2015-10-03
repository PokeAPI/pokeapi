# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0002_itemflingeffect_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemonhabitatname',
            name='pokemon_habitat',
            field=models.ForeignKey(related_name='pokemonhabitatname', blank=True, to='pokemon_v2.PokemonHabitat', null=True),
            preserve_default=True,
        ),
    ]
