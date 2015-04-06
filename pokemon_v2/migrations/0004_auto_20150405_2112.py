# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0003_auto_20150405_2109'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='languagename',
            name='language_id',
        ),
        migrations.AddField(
            model_name='languagename',
            name='language',
            field=models.ForeignKey(blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
    ]
