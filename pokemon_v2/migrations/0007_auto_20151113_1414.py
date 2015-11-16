# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0006_auto_20151111_2216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='berry',
            name='berry_firmness',
            field=models.ForeignKey(related_name='berry', blank=True, to='pokemon_v2.BerryFirmness', null=True),
            preserve_default=True,
        ),
    ]
