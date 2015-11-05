# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0001_squashed_0024_auto_20151027_0023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encounterconditionvaluename',
            name='encounter_condition_value',
            field=models.ForeignKey(related_name='encounterconditionvaluename', blank=True, to='pokemon_v2.EncounterConditionValue', null=True),
            preserve_default=True,
        ),
    ]
