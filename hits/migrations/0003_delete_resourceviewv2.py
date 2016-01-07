# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hits', '0002_resourceviewv2'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ResourceViewV2',
        ),
    ]
