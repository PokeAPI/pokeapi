# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0005_auto_20151022_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='berryfirmnessname',
            name='berry_firmness',
            field=models.ForeignKey(related_name='berryfirmnessname', blank=True, to='pokemon_v2.BerryFirmness', null=True),
            preserve_default=True,
        ),
    ]
