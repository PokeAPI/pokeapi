# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0004_auto_20150910_0225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abilitychangedescription',
            name='language',
            field=models.ForeignKey(related_name='abilitychangedescription', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='abilitydescription',
            name='language',
            field=models.ForeignKey(related_name='abilitydescription', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='abilityflavortext',
            name='language',
            field=models.ForeignKey(related_name='abilityflavortext', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='abilityname',
            name='language',
            field=models.ForeignKey(related_name='abilityname', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='berryfirmnessname',
            name='language',
            field=models.ForeignKey(related_name='berryfirmnessname', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='characteristicdescription',
            name='language',
            field=models.ForeignKey(related_name='characteristicdescription', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contesteffectdescription',
            name='language',
            field=models.ForeignKey(related_name='contesteffectdescription', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contesttypename',
            name='language',
            field=models.ForeignKey(related_name='contesttypename', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='egggroupname',
            name='language',
            field=models.ForeignKey(related_name='egggroupname', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='encounterconditionname',
            name='language',
            field=models.ForeignKey(related_name='encounterconditionname', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='encounterconditionvaluename',
            name='language',
            field=models.ForeignKey(related_name='encounterconditionvaluename', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='encountermethodname',
            name='language',
            field=models.ForeignKey(related_name='encountermethodname', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='evolutiontriggername',
            name='language',
            field=models.ForeignKey(related_name='evolutiontriggername', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='generationname',
            name='language',
            field=models.ForeignKey(related_name='generationname', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='growthratedescription',
            name='language',
            field=models.ForeignKey(related_name='growthratedescription', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='itemcategoryname',
            name='language',
            field=models.ForeignKey(related_name='itemcategoryname', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='itemdescription',
            name='language',
            field=models.ForeignKey(related_name='itemdescription', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='itemflagdescription',
            name='language',
            field=models.ForeignKey(related_name='itemflagdescription', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='itemflavortext',
            name='language',
            field=models.ForeignKey(related_name='itemflavortext', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='itemflingeffectdescription',
            name='language',
            field=models.ForeignKey(related_name='itemflingeffectdescription', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='itemname',
            name='language',
            field=models.ForeignKey(related_name='itemname', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='itempocketname',
            name='language',
            field=models.ForeignKey(related_name='itempocketname', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='languagename',
            name='language',
            field=models.ForeignKey(related_name='languagename', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='locationareaname',
            name='language',
            field=models.ForeignKey(related_name='locationareaname', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='locationname',
            name='language',
            field=models.ForeignKey(related_name='locationname', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movebattlestylename',
            name='language',
            field=models.ForeignKey(related_name='movebattlestylename', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movedamageclassdescription',
            name='language',
            field=models.ForeignKey(related_name='movedamageclassdescription', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='moveeffectchangedescription',
            name='language',
            field=models.ForeignKey(related_name='moveeffectchangedescription', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='moveeffectdescription',
            name='language',
            field=models.ForeignKey(related_name='moveeffectdescription', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='moveflagdescription',
            name='language',
            field=models.ForeignKey(related_name='moveflagdescription', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='moveflavortext',
            name='language',
            field=models.ForeignKey(related_name='moveflavortext', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movemetaailmentname',
            name='language',
            field=models.ForeignKey(related_name='movemetaailmentname', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movemetacategorydescription',
            name='language',
            field=models.ForeignKey(related_name='movemetacategorydescription', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movename',
            name='language',
            field=models.ForeignKey(related_name='movename', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movetargetdescription',
            name='language',
            field=models.ForeignKey(related_name='movetargetdescription', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='naturename',
            name='language',
            field=models.ForeignKey(related_name='naturename', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='palparkareaname',
            name='language',
            field=models.ForeignKey(related_name='palparkareaname', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokeathlonstatname',
            name='language',
            field=models.ForeignKey(related_name='pokeathlonstatname', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokedexdescription',
            name='language',
            field=models.ForeignKey(related_name='pokedexdescription', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokemoncolorname',
            name='language',
            field=models.ForeignKey(related_name='pokemoncolorname', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokemonformname',
            name='language',
            field=models.ForeignKey(related_name='pokemonformname', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokemonhabitatname',
            name='language',
            field=models.ForeignKey(related_name='pokemonhabitatname', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokemonmovemethodname',
            name='language',
            field=models.ForeignKey(related_name='pokemonmovemethodname', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokemonshapename',
            name='language',
            field=models.ForeignKey(related_name='pokemonshapename', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokemonspeciesdescription',
            name='language',
            field=models.ForeignKey(related_name='pokemonspeciesdescription', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokemonspeciesflavortext',
            name='language',
            field=models.ForeignKey(related_name='pokemonspeciesflavortext', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokemonspeciesname',
            name='language',
            field=models.ForeignKey(related_name='pokemonspeciesname', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='regionname',
            name='language',
            field=models.ForeignKey(related_name='regionname', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='statname',
            name='language',
            field=models.ForeignKey(related_name='statname', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='supercontesteffectdescription',
            name='language',
            field=models.ForeignKey(related_name='supercontesteffectdescription', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='typename',
            name='language',
            field=models.ForeignKey(related_name='typename', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='versionname',
            name='language',
            field=models.ForeignKey(related_name='versionname', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
    ]
