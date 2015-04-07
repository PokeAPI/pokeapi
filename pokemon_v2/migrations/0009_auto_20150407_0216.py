# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0008_typeefficacy'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('hates_flavor_id', models.IntegerField()),
                ('likes_flavor_id', models.IntegerField()),
                ('game_index', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NatureBattleStylePreference',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('move_battle_style_id', models.IntegerField()),
                ('low_hp_preference', models.IntegerField()),
                ('high_hp_preference', models.IntegerField()),
                ('nature', models.ForeignKey(blank=True, to='pokemon_v2.Nature', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NatureNames',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('language', models.ForeignKey(blank=True, to='pokemon_v2.Language', null=True)),
                ('nature', models.ForeignKey(blank=True, to='pokemon_v2.Nature', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NaturePokeathalonStats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('max_change', models.IntegerField()),
                ('nature', models.ForeignKey(blank=True, to='pokemon_v2.Nature', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Stat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('damage_class_id', models.IntegerField(null=True, blank=True)),
                ('name', models.CharField(max_length=30)),
                ('is_battle_only', models.BooleanField(default=False)),
                ('game_index', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StatName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('language', models.ForeignKey(blank=True, to='pokemon_v2.Language', null=True)),
                ('stat', models.ForeignKey(blank=True, to='pokemon_v2.Stat', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='naturepokeathalonstats',
            name='pokeathalon_stat_id',
            field=models.ForeignKey(blank=True, to='pokemon_v2.Stat', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='nature',
            name='decreased_stat_id',
            field=models.ForeignKey(related_name='decreased', blank=True, to='pokemon_v2.Stat', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='nature',
            name='increased_stat_id',
            field=models.ForeignKey(related_name='increased', blank=True, to='pokemon_v2.Stat', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='type',
            name='damage_class_id',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
