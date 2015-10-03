# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0001_squashed_0013_auto_20150926_0913'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemflingeffect',
            name='name',
            field=models.CharField(default='name', max_length=100),
            preserve_default=False,
        ),
    ]
