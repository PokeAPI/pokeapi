# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ability',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('generation', models.IntegerField()),
                ('is_main_series', models.IntegerField()),
                ('name', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AbilityDescription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ability_id', models.IntegerField()),
                ('local_language_id', models.IntegerField()),
                ('short_effect', models.CharField(max_length=200)),
                ('effect', models.CharField(max_length=1000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AbilityFlavorText',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ability_id', models.IntegerField()),
                ('version_group_id', models.IntegerField()),
                ('language_id', models.IntegerField()),
                ('flavor_text', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AbilityName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ability_id', models.IntegerField()),
                ('local_language_id', models.IntegerField()),
                ('name', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='ability',
            name='description',
            field=models.OneToOneField(null=True, blank=True, to='pokemon_v2.AbilityDescription'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ability',
            name='flavor_text',
            field=models.ForeignKey(blank=True, to='pokemon_v2.AbilityFlavorText', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ability',
            name='names',
            field=models.ForeignKey(blank=True, to='pokemon_v2.AbilityName', null=True),
            preserve_default=True,
        ),
    ]
