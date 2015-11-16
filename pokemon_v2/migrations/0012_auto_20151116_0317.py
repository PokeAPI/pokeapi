# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0011_auto_20151116_0230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generation',
            name='region',
            field=models.OneToOneField(related_name='generation', null=True, blank=True, to='pokemon_v2.Region'),
            preserve_default=True,
        ),
    ]
