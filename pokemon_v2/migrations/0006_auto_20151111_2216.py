# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0005_auto_20151111_0541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='palpark',
            name='pal_park_area',
            field=models.ForeignKey(related_name='palpark', blank=True, to='pokemon_v2.PalParkArea', null=True),
            preserve_default=True,
        ),
    ]
