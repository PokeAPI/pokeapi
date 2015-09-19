# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0004_auto_20150915_0448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemonshapename',
            name='pokemon_shape',
            field=models.ForeignKey(related_name='pokemonshapename', blank=True, to='pokemon_v2.PokemonShape', null=True),
            preserve_default=True,
        ),
    ]
