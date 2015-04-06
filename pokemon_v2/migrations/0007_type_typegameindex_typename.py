# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0006_auto_20150406_0336'),
    ]

    operations = [
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('damage_class_id', models.IntegerField()),
                ('generation', models.ForeignKey(blank=True, to='pokemon_v2.Generation', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TypeGameIndex',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('game_index', models.IntegerField()),
                ('generation', models.ForeignKey(blank=True, to='pokemon_v2.Generation', null=True)),
                ('type', models.ForeignKey(blank=True, to='pokemon_v2.Type', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TypeName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('language', models.ForeignKey(blank=True, to='pokemon_v2.Language', null=True)),
                ('type', models.ForeignKey(blank=True, to='pokemon_v2.Type', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
