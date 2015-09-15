# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0002_auto_20150914_1324'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='typeefficacy',
            name='damage_type_id',
        ),
        migrations.RemoveField(
            model_name='typeefficacy',
            name='target_type_id',
        ),
        migrations.AddField(
            model_name='typeefficacy',
            name='damage_type',
            field=models.ForeignKey(related_name='damage_type', blank=True, to='pokemon_v2.Type', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='typeefficacy',
            name='target_type',
            field=models.ForeignKey(related_name='target_type', blank=True, to='pokemon_v2.Type', null=True),
            preserve_default=True,
        ),
    ]
