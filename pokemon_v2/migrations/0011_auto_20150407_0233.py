# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0010_auto_20150407_0231'),
    ]

    operations = [
        migrations.CreateModel(
            name='NaturePokeathalonStat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('max_change', models.IntegerField()),
                ('nature', models.ForeignKey(blank=True, to='pokemon_v2.Nature', null=True)),
                ('pokeathalon_stat_id', models.ForeignKey(blank=True, to='pokemon_v2.Stat', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='naturepokeathalonstats',
            name='nature',
        ),
        migrations.RemoveField(
            model_name='naturepokeathalonstats',
            name='pokeathalon_stat_id',
        ),
        migrations.DeleteModel(
            name='NaturePokeathalonStats',
        ),
    ]
