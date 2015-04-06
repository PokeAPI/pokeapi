# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0005_generation_generationname'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ability',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('is_main_series', models.BooleanField(default=False)),
                ('generation', models.ForeignKey(blank=True, to='pokemon_v2.Generation', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AbilityDescription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('short_effect', models.CharField(max_length=300)),
                ('effect', models.CharField(max_length=2000)),
                ('ability', models.ForeignKey(blank=True, to='pokemon_v2.Ability', null=True)),
                ('language', models.ForeignKey(blank=True, to='pokemon_v2.Language', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AbilityFlavorText',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('flavor_text', models.CharField(max_length=100)),
                ('ability', models.ForeignKey(blank=True, to='pokemon_v2.Ability', null=True)),
                ('language', models.ForeignKey(blank=True, to='pokemon_v2.Language', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AbilityName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('ability', models.ForeignKey(blank=True, to='pokemon_v2.Ability', null=True)),
                ('language', models.ForeignKey(blank=True, to='pokemon_v2.Language', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VersionGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('order', models.IntegerField()),
                ('generation', models.ForeignKey(blank=True, to='pokemon_v2.Generation', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VersionGroupPokemonMoveMethod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pokemon_move_method_id', models.IntegerField()),
                ('version_group', models.ForeignKey(blank=True, to='pokemon_v2.VersionGroup', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VersionGroupRegion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('region_id', models.IntegerField()),
                ('version_group', models.ForeignKey(blank=True, to='pokemon_v2.VersionGroup', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VersionName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('language', models.ForeignKey(blank=True, to='pokemon_v2.Language', null=True)),
                ('version', models.ForeignKey(blank=True, to='pokemon_v2.Version', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='version',
            name='version_group',
            field=models.ForeignKey(blank=True, to='pokemon_v2.VersionGroup', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='abilityflavortext',
            name='version_group',
            field=models.ForeignKey(blank=True, to='pokemon_v2.VersionGroup', null=True),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='generationname',
            name='local_language_id',
        ),
        migrations.AddField(
            model_name='generationname',
            name='language',
            field=models.ForeignKey(blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='language',
            name='name',
            field=models.CharField(max_length=30),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='language',
            name='official',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
