# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0001_squashed_0003_auto_20151119_1409'),
    ]

    operations = [
        migrations.CreateModel(
            name='PokemonImageSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('front_default', models.BooleanField(default=False)),
                ('front_female', models.BooleanField(default=False)),
                ('front_shiny', models.BooleanField(default=False)),
                ('front_shiny_female', models.BooleanField(default=False)),
                ('back_default', models.BooleanField(default=False)),
                ('back_female', models.BooleanField(default=False)),
                ('back_shiny', models.BooleanField(default=False)),
                ('back_shiny_female', models.BooleanField(default=False)),
                ('pokemon', models.ForeignKey(related_name='pokemonimageset', blank=True, to='pokemon_v2.Pokemon', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
