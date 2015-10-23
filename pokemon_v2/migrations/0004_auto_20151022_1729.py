# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0003_auto_20151022_1725'),
    ]

    operations = [
        migrations.RenameField(
            model_name='itemattributedescription',
            old_name='item_flag',
            new_name='item_attribute',
        ),
    ]
