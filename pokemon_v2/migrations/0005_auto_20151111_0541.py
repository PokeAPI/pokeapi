# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0004_auto_20151111_0531'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemflingeffecteffecttext',
            name='description',
        ),
        migrations.AddField(
            model_name='itemflingeffecteffecttext',
            name='effect',
            field=models.CharField(default='string', max_length=4000),
            preserve_default=False,
        ),
    ]
