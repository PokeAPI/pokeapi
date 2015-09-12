# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0009_auto_20150911_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='move',
            name='type',
            field=models.ForeignKey(related_name='move', blank=True, to='pokemon_v2.Type', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movechange',
            name='type',
            field=models.ForeignKey(related_name='movechange', blank=True, to='pokemon_v2.Type', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokemontype',
            name='type',
            field=models.ForeignKey(related_name='pokemontype', blank=True, to='pokemon_v2.Type', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='typegameindex',
            name='type',
            field=models.ForeignKey(related_name='typegameindex', blank=True, to='pokemon_v2.Type', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='typename',
            name='type',
            field=models.ForeignKey(related_name='typename', blank=True, to='pokemon_v2.Type', null=True),
            preserve_default=True,
        ),
    ]
