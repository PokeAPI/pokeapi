# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0004_pokemonsprites'),
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
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='pokemonimageset',
            name='pokemon',
        ),
        migrations.DeleteModel(
            name='PokemonImageSet',
        ),
    ]
