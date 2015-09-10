# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0005_auto_20150910_0353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abilitychangedescription',
            name='language',
            field=models.ForeignKey(related_name='abilitychangedescriptionlanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='abilitydescription',
            name='language',
            field=models.ForeignKey(related_name='abilitydescriptionlanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='abilityflavortext',
            name='language',
            field=models.ForeignKey(related_name='abilityflavortextlanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='abilityname',
            name='language',
            field=models.ForeignKey(related_name='abilitynamelanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='berryfirmnessname',
            name='language',
            field=models.ForeignKey(related_name='berryfirmnessnamelanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='characteristicdescription',
            name='language',
            field=models.ForeignKey(related_name='characteristicdescriptionlanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contesteffectdescription',
            name='language',
            field=models.ForeignKey(related_name='contesteffectdescriptionlanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contesttypename',
            name='language',
            field=models.ForeignKey(related_name='contesttypenamelanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='egggroupname',
            name='language',
            field=models.ForeignKey(related_name='egggroupnamelanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='encounterconditionname',
            name='language',
            field=models.ForeignKey(related_name='encounterconditionnamelanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='encounterconditionvaluename',
            name='language',
            field=models.ForeignKey(related_name='encounterconditionvaluenamelanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='encountermethodname',
            name='language',
            field=models.ForeignKey(related_name='encountermethodnamelanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='evolutiontriggername',
            name='language',
            field=models.ForeignKey(related_name='evolutiontriggernamelanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='generationname',
            name='language',
            field=models.ForeignKey(related_name='generationnamelanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='growthratedescription',
            name='language',
            field=models.ForeignKey(related_name='growthratedescriptionlanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='itemcategoryname',
            name='language',
            field=models.ForeignKey(related_name='itemcategorynamelanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='itemdescription',
            name='language',
            field=models.ForeignKey(related_name='itemdescriptionlanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='itemflagdescription',
            name='language',
            field=models.ForeignKey(related_name='itemflagdescriptionlanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='itemflavortext',
            name='language',
            field=models.ForeignKey(related_name='itemflavortextlanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='itemflingeffectdescription',
            name='language',
            field=models.ForeignKey(related_name='itemflingeffectdescriptionlanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='itemname',
            name='language',
            field=models.ForeignKey(related_name='itemnamelanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='itempocketname',
            name='language',
            field=models.ForeignKey(related_name='itempocketnamelanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='languagename',
            name='language',
            field=models.ForeignKey(related_name='languagenamelanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='locationareaname',
            name='language',
            field=models.ForeignKey(related_name='locationareanamelanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='locationname',
            name='language',
            field=models.ForeignKey(related_name='locationnamelanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movebattlestylename',
            name='language',
            field=models.ForeignKey(related_name='movebattlestylenamelanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movedamageclassdescription',
            name='language',
            field=models.ForeignKey(related_name='movedamageclassdescriptionlanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='moveeffectchangedescription',
            name='language',
            field=models.ForeignKey(related_name='moveeffectchangedescriptionlanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='moveeffectdescription',
            name='language',
            field=models.ForeignKey(related_name='moveeffectdescriptionlanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='moveflagdescription',
            name='language',
            field=models.ForeignKey(related_name='moveflagdescriptionlanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='moveflavortext',
            name='language',
            field=models.ForeignKey(related_name='moveflavortextlanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movemetaailmentname',
            name='language',
            field=models.ForeignKey(related_name='movemetaailmentnamelanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movemetacategorydescription',
            name='language',
            field=models.ForeignKey(related_name='movemetacategorydescriptionlanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movename',
            name='language',
            field=models.ForeignKey(related_name='movenamelanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movetargetdescription',
            name='language',
            field=models.ForeignKey(related_name='movetargetdescriptionlanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='naturename',
            name='language',
            field=models.ForeignKey(related_name='naturenamelanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='palparkareaname',
            name='language',
            field=models.ForeignKey(related_name='palparkareanamelanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokeathlonstatname',
            name='language',
            field=models.ForeignKey(related_name='pokeathlonstatnamelanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokedexdescription',
            name='language',
            field=models.ForeignKey(related_name='pokedexdescriptionlanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokemoncolorname',
            name='language',
            field=models.ForeignKey(related_name='pokemoncolornamelanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokemonformname',
            name='language',
            field=models.ForeignKey(related_name='pokemonformnamelanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokemonhabitatname',
            name='language',
            field=models.ForeignKey(related_name='pokemonhabitatnamelanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokemonmovemethodname',
            name='language',
            field=models.ForeignKey(related_name='pokemonmovemethodnamelanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokemonshapename',
            name='language',
            field=models.ForeignKey(related_name='pokemonshapenamelanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokemonspeciesdescription',
            name='language',
            field=models.ForeignKey(related_name='pokemonspeciesdescriptionlanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokemonspeciesflavortext',
            name='language',
            field=models.ForeignKey(related_name='pokemonspeciesflavortextlanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokemonspeciesname',
            name='language',
            field=models.ForeignKey(related_name='pokemonspeciesnamelanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='regionname',
            name='language',
            field=models.ForeignKey(related_name='regionnamelanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='statname',
            name='language',
            field=models.ForeignKey(related_name='statnamelanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='supercontesteffectdescription',
            name='language',
            field=models.ForeignKey(related_name='supercontesteffectdescriptionlanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='typename',
            name='language',
            field=models.ForeignKey(related_name='typenamelanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='versionname',
            name='language',
            field=models.ForeignKey(related_name='versionnamelanguage', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
    ]
