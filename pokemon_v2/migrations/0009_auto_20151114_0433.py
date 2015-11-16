# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0008_auto_20151114_0241'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='move',
            name='contest_effect_id',
        ),
        migrations.RemoveField(
            model_name='move',
            name='contest_type_id',
        ),
        migrations.RemoveField(
            model_name='move',
            name='super_contest_effect_id',
        ),
        migrations.AddField(
            model_name='move',
            name='contest_effect',
            field=models.ForeignKey(related_name='move', blank=True, to='pokemon_v2.ContestEffect', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='move',
            name='contest_type',
            field=models.ForeignKey(related_name='move', blank=True, to='pokemon_v2.ContestType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='move',
            name='super_contest_effect',
            field=models.ForeignKey(related_name='move', blank=True, to='pokemon_v2.SuperContestEffect', null=True),
            preserve_default=True,
        ),
    ]
