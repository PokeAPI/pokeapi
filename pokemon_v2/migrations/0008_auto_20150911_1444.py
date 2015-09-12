# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0007_auto_20150911_1436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generation',
            name='region',
            field=models.ForeignKey(related_name='generation', blank=True, to='pokemon_v2.Region', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='location',
            name='region',
            field=models.ForeignKey(related_name='location', blank=True, to='pokemon_v2.Region', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokedex',
            name='region',
            field=models.ForeignKey(related_name='pokedex', blank=True, to='pokemon_v2.Region', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='regionname',
            name='region',
            field=models.ForeignKey(related_name='regionname', blank=True, to='pokemon_v2.Region', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='versiongroupregion',
            name='region',
            field=models.ForeignKey(related_name='versiongroupregion', blank=True, to='pokemon_v2.Region', null=True),
            preserve_default=True,
        ),
    ]
