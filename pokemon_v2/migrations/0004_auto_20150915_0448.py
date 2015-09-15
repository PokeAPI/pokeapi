# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0003_auto_20150915_0055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='palpark',
            name='pokemon_species',
            field=models.ForeignKey(related_name='palpark', blank=True, to='pokemon_v2.PokemonSpecies', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokedexdescription',
            name='pokedex',
            field=models.ForeignKey(related_name='pokedexdescription', blank=True, to='pokemon_v2.Pokedex', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokedexversiongroup',
            name='pokedex',
            field=models.ForeignKey(related_name='pokedexversiongroup', blank=True, to='pokemon_v2.Pokedex', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='pokemon_species',
            field=models.ForeignKey(related_name='pokemon', blank=True, to='pokemon_v2.PokemonSpecies', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokemondexnumber',
            name='pokedex',
            field=models.ForeignKey(related_name='pokemondexnumber', blank=True, to='pokemon_v2.Pokedex', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokemondexnumber',
            name='pokemon_species',
            field=models.ForeignKey(related_name='pokemondexnumber', blank=True, to='pokemon_v2.PokemonSpecies', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokemonegggroup',
            name='pokemon_species',
            field=models.ForeignKey(related_name='pokemonegggroup', blank=True, to='pokemon_v2.PokemonSpecies', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokemonspeciesdescription',
            name='pokemon_species',
            field=models.ForeignKey(related_name='pokemonspeciesdescription', blank=True, to='pokemon_v2.PokemonSpecies', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokemonspeciesflavortext',
            name='pokemon_species',
            field=models.ForeignKey(related_name='pokemonspeciesflavortext', blank=True, to='pokemon_v2.PokemonSpecies', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokemonspeciesname',
            name='pokemon_species',
            field=models.ForeignKey(related_name='pokemonspeciesname', blank=True, to='pokemon_v2.PokemonSpecies', null=True),
            preserve_default=True,
        ),
    ]
