# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0008_auto_20150911_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abilityflavortext',
            name='version_group',
            field=models.ForeignKey(related_name='abilityflavortext', blank=True, to='pokemon_v2.VersionGroup', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='encounter',
            name='version',
            field=models.ForeignKey(related_name='encounter', blank=True, to='pokemon_v2.Version', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='encounterslot',
            name='version_group',
            field=models.ForeignKey(related_name='encounterslot', blank=True, to='pokemon_v2.VersionGroup', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='itemflavortext',
            name='version_group',
            field=models.ForeignKey(related_name='itemflavortext', blank=True, to='pokemon_v2.VersionGroup', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='locationareaencounterrate',
            name='version',
            field=models.ForeignKey(related_name='locationareaencounterrate', blank=True, to='pokemon_v2.Version', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movechange',
            name='version_group',
            field=models.ForeignKey(related_name='movechange', blank=True, to='pokemon_v2.VersionGroup', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='moveeffectchange',
            name='version_group',
            field=models.ForeignKey(related_name='moveeffectchange', blank=True, to='pokemon_v2.VersionGroup', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='moveflavortext',
            name='version_group',
            field=models.ForeignKey(related_name='moveflavortext', blank=True, to='pokemon_v2.VersionGroup', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokedexversiongroup',
            name='version_group',
            field=models.ForeignKey(related_name='pokedexversiongroup', blank=True, to='pokemon_v2.VersionGroup', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokemongameindex',
            name='version',
            field=models.ForeignKey(related_name='pokemongameindex', blank=True, to='pokemon_v2.Version', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokemonitem',
            name='version',
            field=models.ForeignKey(related_name='pokemonitem', blank=True, to='pokemon_v2.Version', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokemonmove',
            name='version_group',
            field=models.ForeignKey(related_name='pokemonmove', blank=True, to='pokemon_v2.VersionGroup', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokemonspeciesflavortext',
            name='version',
            field=models.ForeignKey(related_name='pokemonspeciesflavortext', blank=True, to='pokemon_v2.Version', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='version',
            name='version_group',
            field=models.ForeignKey(related_name='version', blank=True, to='pokemon_v2.VersionGroup', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='versiongrouppokemonmovemethod',
            name='version_group',
            field=models.ForeignKey(related_name='versiongrouppokemonmovemethod', blank=True, to='pokemon_v2.VersionGroup', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='versiongroupregion',
            name='version_group',
            field=models.ForeignKey(related_name='versiongroupregion', blank=True, to='pokemon_v2.VersionGroup', null=True),
            preserve_default=True,
        ),
    ]
