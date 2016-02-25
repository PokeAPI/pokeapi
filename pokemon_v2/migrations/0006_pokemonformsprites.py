# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0005_auto_20160214_1651'),
    ]

    operations = [
        migrations.CreateModel(
            name='PokemonFormSprites',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sprites', models.CharField(max_length=500)),
                ('pokemon_form', models.ForeignKey(related_name='pokemonformsprites', blank=True, to='pokemon_v2.PokemonForm', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
