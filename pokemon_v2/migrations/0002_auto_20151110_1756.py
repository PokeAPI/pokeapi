# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0001_squashed_0011_auto_20151108_0352'),
    ]

    operations = [
        migrations.CreateModel(
            name='BerryFlavorName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('berry_flavor', models.ForeignKey(related_name='berryflavorname', blank=True, to='pokemon_v2.BerryFlavor', null=True)),
                ('language', models.ForeignKey(related_name='berryflavorname_language', blank=True, to='pokemon_v2.Language', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='berryflavor',
            name='berry',
        ),
        migrations.RemoveField(
            model_name='berryflavor',
            name='flavor',
        ),
        migrations.AddField(
            model_name='berryflavor',
            name='name',
            field=models.CharField(default='name', max_length=100),
            preserve_default=False,
        ),
    ]
