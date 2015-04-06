# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0007_type_typegameindex_typename'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeEfficacy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('damage_type_id', models.IntegerField()),
                ('target_type_id', models.IntegerField()),
                ('damage_factor', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
