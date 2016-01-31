# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hits', '0001_squashed_0005_auto_20160107_0231'),
    ]

    operations = [
        migrations.AddField(
            model_name='resourceview',
            name='version',
            field=models.IntegerField(default=1, max_length=1),
            preserve_default=True,
        ),
    ]
