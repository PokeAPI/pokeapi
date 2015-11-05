# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0002_auto_20151102_2124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supercontesteffectflavortext',
            name='super_contest_effect',
            field=models.ForeignKey(related_name='supercontesteffectflavortext', blank=True, to='pokemon_v2.SuperContestEffect', null=True),
            preserve_default=True,
        ),
    ]
