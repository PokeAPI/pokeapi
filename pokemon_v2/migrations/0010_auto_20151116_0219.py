# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0009_auto_20151114_0433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemonspecies',
            name='pokemon_habitat',
            field=models.ForeignKey(related_name='pokemonspecies', blank=True, to='pokemon_v2.PokemonHabitat', null=True),
            preserve_default=True,
        ),
    ]
