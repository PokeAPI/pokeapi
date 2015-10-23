# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0006_auto_20151023_0135'),
    ]

    operations = [
        migrations.AddField(
            model_name='berry',
            name='name',
            field=models.CharField(default='name', max_length=100),
            preserve_default=False,
        ),
    ]
