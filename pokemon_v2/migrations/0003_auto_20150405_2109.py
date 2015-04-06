# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0002_auto_20150405_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='languagename',
            name='language_id',
            field=models.ForeignKey(related_name='language', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
    ]
