# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hits', '0003_delete_resourceviewv2'),
    ]

    operations = [
        migrations.AddField(
            model_name='resourceview',
            name='version',
            field=models.IntegerField(default=0, max_length=1000),
            preserve_default=True,
        ),
    ]
