# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0009_auto_20150407_0216'),
    ]

    operations = [
        migrations.CreateModel(
            name='NatureName',
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
        migrations.RemoveField(
            model_name='naturenames',
            name='language',
        ),
        migrations.RemoveField(
            model_name='naturenames',
            name='nature',
        ),
        migrations.DeleteModel(
            name='NatureNames',
        ),
    ]
