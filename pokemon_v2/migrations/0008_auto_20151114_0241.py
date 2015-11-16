# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0007_auto_20151113_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='berryflavor',
            name='contest_type',
            field=models.OneToOneField(related_name='berryflavor', null=True, blank=True, to='pokemon_v2.ContestType'),
            preserve_default=True,
        ),
    ]
