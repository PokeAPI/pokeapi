# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0002_auto_20150403_0536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abilitydescription',
            name='effect',
            field=models.CharField(max_length=2000),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='abilitydescription',
            name='short_effect',
            field=models.CharField(max_length=300),
            preserve_default=True,
        ),
    ]
