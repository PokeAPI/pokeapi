# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import imagekit.models.fields
import pokemon.utils


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ability',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Description',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EggGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Evolution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('level', models.IntegerField(default=0, max_length=3)),
                ('method', models.CharField(default=0, max_length=10, choices=[(b'level up', b'level_up'), (b'stone', b'stone'), (b'trade', b'trade'), (b'other', b'other')])),
                ('detail', models.CharField(max_length=10, null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=50)),
                ('generation', models.IntegerField(max_length=4)),
                ('release_year', models.IntegerField(max_length=6)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Move',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=200)),
                ('pp', models.IntegerField(max_length=5)),
                ('category', models.CharField(max_length=10, choices=[(b'physical', b'physical'), (b'special', b'special'), (b'status', b'status')])),
                ('power', models.IntegerField(max_length=6)),
                ('accuracy', models.IntegerField(max_length=6)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MovePokemon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('learn_type', models.CharField(default=b'level up', max_length=15, choices=[(b'level up', b'level up'), (b'machine', b'machine'), (b'egg move', b'egg move'), (b'tutor', b'tutor'), (b'other', b'other')])),
                ('level', models.IntegerField(default=0, max_length=6, null=True, blank=True)),
                ('move', models.ForeignKey(related_name='pokemon', blank=True, to='pokemon.Move', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pokedex',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=60)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pokemon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=50)),
                ('pkdx_id', models.IntegerField(max_length=4, blank=True)),
                ('species', models.CharField(max_length=30)),
                ('height', models.CharField(max_length=10)),
                ('weight', models.CharField(max_length=10)),
                ('ev_yield', models.CharField(max_length=20)),
                ('catch_rate', models.IntegerField(max_length=4)),
                ('happiness', models.IntegerField(max_length=4)),
                ('exp', models.IntegerField(max_length=5)),
                ('growth_rate', models.CharField(max_length=15, choices=[(b'slow', b'slow'), (b'medium slow', b'medium slow'), (b'medium', b'medium'), (b'medium fast', b'medium fast'), (b'fast', b'fast')])),
                ('male_female_ratio', models.CharField(max_length=10)),
                ('hp', models.IntegerField(max_length=4)),
                ('attack', models.IntegerField(max_length=4)),
                ('defense', models.IntegerField(max_length=4)),
                ('sp_atk', models.IntegerField(max_length=4)),
                ('sp_def', models.IntegerField(max_length=4)),
                ('speed', models.IntegerField(max_length=4)),
                ('total', models.IntegerField(max_length=6)),
                ('egg_cycles', models.IntegerField(max_length=6)),
                ('abilities', models.ManyToManyField(to='pokemon.Ability', null=True, blank=True)),
                ('descriptions', models.ManyToManyField(to='pokemon.Description', null=True, blank=True)),
                ('egg_group', models.ManyToManyField(to='pokemon.EggGroup', null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sprite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=50)),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to=pokemon.utils.unique_filename)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TypeChart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('ttype', models.CharField(blank=True, max_length=15, null=True, choices=[(b'weak', b'weak'), (b'super effective', b'super effective'), (b'resistant', b'resistant'), (b'ineffective', b'ineffective'), (b'noeffect', b'noeffect'), (b'resist', b'resist')])),
                ('frm', models.ForeignKey(related_name='type_frm', blank=True, to='pokemon.Type', null=True)),
                ('to', models.ForeignKey(related_name='type_to', blank=True, to='pokemon.Type', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='pokemon',
            name='sprites',
            field=models.ManyToManyField(to='pokemon.Sprite', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pokemon',
            name='types',
            field=models.ManyToManyField(to='pokemon.Type', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='movepokemon',
            name='pokemon',
            field=models.ForeignKey(related_name='move', blank=True, to='pokemon.Pokemon', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='move',
            name='etype',
            field=models.ManyToManyField(to='pokemon.Type', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='evolution',
            name='frm',
            field=models.ForeignKey(related_name='frm_evol_pokemon', blank=True, to='pokemon.Pokemon', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='evolution',
            name='to',
            field=models.ForeignKey(related_name='to_evol_pokemon', blank=True, to='pokemon.Pokemon', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='description',
            name='game',
            field=models.ManyToManyField(to='pokemon.Game', null=True, blank=True),
            preserve_default=True,
        ),
    ]
