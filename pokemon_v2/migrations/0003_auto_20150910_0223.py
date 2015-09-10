# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0002_auto_20150910_0153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abilitychange',
            name='ability',
            field=models.ForeignKey(related_name='abilitychange_descriptions', blank=True, to='pokemon_v2.Ability', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='abilitydescription',
            name='ability',
            field=models.ForeignKey(related_name='abilitydescription_descriptions', blank=True, to='pokemon_v2.Ability', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='abilityflavortext',
            name='ability',
            field=models.ForeignKey(related_name='abilityflavortext_descriptions', blank=True, to='pokemon_v2.Ability', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='abilityname',
            name='ability',
            field=models.ForeignKey(related_name='abilityname_descriptions', blank=True, to='pokemon_v2.Ability', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokemonability',
            name='ability',
            field=models.ForeignKey(related_name='pokemonability_descriptions', blank=True, to='pokemon_v2.Ability', null=True),
            preserve_default=True,
        ),
    ]
