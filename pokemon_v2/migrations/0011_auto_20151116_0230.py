# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0010_auto_20151116_0219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemonspecies',
            name='pokemon_shape',
            field=models.ForeignKey(related_name='pokemonspecies', blank=True, to='pokemon_v2.PokemonShape', null=True),
            preserve_default=True,
        ),
    ]
