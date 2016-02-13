# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0003_auto_20160128_0523'),
    ]

    operations = [
        migrations.CreateModel(
            name='PokemonSprites',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sprites', models.CharField(max_length=500)),
                ('pokemon', models.ForeignKey(related_name='pokemonsprites', blank=True, to='pokemon_v2.Pokemon', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
