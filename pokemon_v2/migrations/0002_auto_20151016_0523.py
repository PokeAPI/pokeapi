# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0001_squashed_0004_auto_20151005_0138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='versionname',
            name='version',
            field=models.ForeignKey(related_name='versionname', blank=True, to='pokemon_v2.Version', null=True),
            preserve_default=True,
        ),
    ]
