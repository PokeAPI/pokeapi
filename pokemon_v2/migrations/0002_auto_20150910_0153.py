# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0001_squashed_0013_auto_20150420_0114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abilitydescription',
            name='ability',
            field=models.ForeignKey(related_name='descriptions', blank=True, to='pokemon_v2.Ability', null=True),
            preserve_default=True,
        ),
    ]
