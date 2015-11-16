# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0002_auto_20151110_1756'),
    ]

    operations = [
        migrations.CreateModel(
            name='BerryFlavorMap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('potency', models.IntegerField()),
                ('berry', models.ForeignKey(related_name='berryflavormap', blank=True, to='pokemon_v2.Berry', null=True)),
                ('berry_flavor', models.ForeignKey(related_name='berryflavormap', blank=True, to='pokemon_v2.BerryFlavor', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
