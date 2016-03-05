# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0001_squashed_0002_auto_20160301_1408'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemSprites',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sprites', models.CharField(max_length=500)),
                ('item', models.ForeignKey(related_name='itemsprites', blank=True, to='pokemon_v2.Item', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
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
        ),
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
        ),
    ]
