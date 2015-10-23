# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0004_auto_20151022_1729'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemflingeffectdescription',
            name='effect',
        ),
        migrations.AddField(
            model_name='itemflingeffectdescription',
            name='description',
            field=models.CharField(default='', max_length=1000),
            preserve_default=True,
        ),
    ]
