# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    # replaces = [(b'hits', '0001_squashed_0005_auto_20160107_0231'), (b'hits', '0002_resourceview_version')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ResourceView',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.IntegerField(default=0, max_length=1000)),
                ('date', models.DateField(auto_now=True)),
                ('version', models.IntegerField(default=1, max_length=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
