# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    replaces = [(b'pokemon_v2', '0001_squashed_0021_auto_20150409_0453'), (b'pokemon_v2', '0002_auto_20150412_1636'), (b'pokemon_v2', '0003_auto_20150412_1705'), (b'pokemon_v2', '0004_auto_20150412_1715'), (b'pokemon_v2', '0005_auto_20150412_1721'), (b'pokemon_v2', '0006_auto_20150412_1808'), (b'pokemon_v2', '0007_auto_20150412_1809'), (b'pokemon_v2', '0008_auto_20150412_1810'), (b'pokemon_v2', '0009_auto_20150412_1814'), (b'pokemon_v2', '0010_auto_20150412_1818'), (b'pokemon_v2', '0011_auto_20150412_1820'), (b'pokemon_v2', '0012_auto_20150412_1821'), (b'pokemon_v2', '0013_auto_20150412_1822'), (b'pokemon_v2', '0014_auto_20150412_1823'), (b'pokemon_v2', '0015_auto_20150412_1825'), (b'pokemon_v2', '0016_auto_20150412_1827'), (b'pokemon_v2', '0017_auto_20150412_1828'), (b'pokemon_v2', '0018_auto_20150412_1833'), (b'pokemon_v2', '0019_auto_20150412_1837'), (b'pokemon_v2', '0020_machine')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('iso639', models.CharField(max_length=2)),
                ('iso3166', models.CharField(max_length=2)),
                ('name', models.CharField(max_length=10)),
                ('official', models.BooleanField()),
                ('order', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LanguageName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('local_language_id', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('language', models.ForeignKey(blank=True, to='pokemon_v2.Language', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Generation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('main_region_id', models.IntegerField()),
                ('name', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GenerationName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('generation', models.ForeignKey(blank=True, to='pokemon_v2.Generation', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ability',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('is_main_series', models.BooleanField(default=False)),
                ('generation', models.ForeignKey(blank=True, to='pokemon_v2.Generation', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AbilityDescription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('short_effect', models.CharField(max_length=300)),
                ('effect', models.CharField(max_length=4000)),
                ('ability', models.ForeignKey(blank=True, to='pokemon_v2.Ability', null=True)),
                ('language', models.ForeignKey(blank=True, to='pokemon_v2.Language', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AbilityFlavorText',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('flavor_text', models.CharField(max_length=100)),
                ('ability', models.ForeignKey(blank=True, to='pokemon_v2.Ability', null=True)),
                ('language', models.ForeignKey(blank=True, to='pokemon_v2.Language', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AbilityName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('ability', models.ForeignKey(blank=True, to='pokemon_v2.Ability', null=True)),
                ('language', models.ForeignKey(blank=True, to='pokemon_v2.Language', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VersionGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('order', models.IntegerField()),
                ('generation', models.ForeignKey(blank=True, to='pokemon_v2.Generation', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VersionGroupPokemonMoveMethod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pokemon_move_method_id', models.IntegerField()),
                ('version_group', models.ForeignKey(blank=True, to='pokemon_v2.VersionGroup', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VersionGroupRegion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('region_id', models.IntegerField()),
                ('version_group', models.ForeignKey(blank=True, to='pokemon_v2.VersionGroup', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VersionName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('language', models.ForeignKey(blank=True, to='pokemon_v2.Language', null=True)),
                ('version', models.ForeignKey(blank=True, to='pokemon_v2.Version', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='version',
            name='version_group',
            field=models.ForeignKey(blank=True, to='pokemon_v2.VersionGroup', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='abilityflavortext',
            name='version_group',
            field=models.ForeignKey(blank=True, to='pokemon_v2.VersionGroup', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='generationname',
            name='language',
            field=models.ForeignKey(blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='language',
            name='name',
            field=models.CharField(max_length=30),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='language',
            name='official',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('damage_class_id', models.IntegerField()),
                ('generation', models.ForeignKey(blank=True, to='pokemon_v2.Generation', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TypeGameIndex',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('game_index', models.IntegerField()),
                ('generation', models.ForeignKey(blank=True, to='pokemon_v2.Generation', null=True)),
                ('type', models.ForeignKey(blank=True, to='pokemon_v2.Type', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TypeName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('language', models.ForeignKey(blank=True, to='pokemon_v2.Language', null=True)),
                ('type', models.ForeignKey(blank=True, to='pokemon_v2.Type', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
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
        migrations.CreateModel(
            name='Nature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('hates_flavor_id', models.IntegerField()),
                ('likes_flavor_id', models.IntegerField()),
                ('game_index', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NatureBattleStylePreference',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('move_battle_style_id', models.IntegerField()),
                ('low_hp_preference', models.IntegerField()),
                ('high_hp_preference', models.IntegerField()),
                ('nature', models.ForeignKey(blank=True, to='pokemon_v2.Nature', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Stat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('damage_class_id', models.IntegerField(null=True, blank=True)),
                ('name', models.CharField(max_length=30)),
                ('is_battle_only', models.BooleanField(default=False)),
                ('game_index', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StatName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('language', models.ForeignKey(blank=True, to='pokemon_v2.Language', null=True)),
                ('stat', models.ForeignKey(blank=True, to='pokemon_v2.Stat', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='nature',
            name='decreased_stat_id',
            field=models.ForeignKey(related_name='decreased', blank=True, to='pokemon_v2.Stat', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='nature',
            name='increased_stat_id',
            field=models.ForeignKey(related_name='increased', blank=True, to='pokemon_v2.Stat', null=True),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='type',
            name='damage_class_id',
        ),
        migrations.CreateModel(
            name='NatureName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('language', models.ForeignKey(blank=True, to='pokemon_v2.Language', null=True)),
                ('nature', models.ForeignKey(blank=True, to='pokemon_v2.Nature', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NaturePokeathlonStat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('max_change', models.IntegerField()),
                ('nature', models.ForeignKey(blank=True, to='pokemon_v2.Nature', null=True)),
                ('pokeathlon_stat_id', models.ForeignKey(blank=True, to='pokemon_v2.Stat', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Characteristic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gene_mod_5', models.IntegerField()),
                ('stat', models.ForeignKey(blank=True, to='pokemon_v2.Stat', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CharacteristicDescription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(default='', max_length=1000)),
                ('characteristic', models.ForeignKey(blank=True, to='pokemon_v2.Characteristic', null=True)),
                ('language', models.ForeignKey(blank=True, to='pokemon_v2.Language', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EggGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EggGroupName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('egg_group', models.ForeignKey(blank=True, to='pokemon_v2.EggGroup', null=True)),
                ('language', models.ForeignKey(blank=True, to='pokemon_v2.Language', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GrowthRate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('formula', models.CharField(max_length=500)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GrowthRateDescription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('growth_rate', models.ForeignKey(blank=True, to='pokemon_v2.GrowthRate', null=True)),
                ('language', models.ForeignKey(blank=True, to='pokemon_v2.Language', null=True)),
                ('description', models.CharField(default='', max_length=1000)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Move',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('power', models.IntegerField()),
                ('pp', models.IntegerField()),
                ('accuracy', models.IntegerField()),
                ('priority', models.IntegerField()),
                ('move_effect_chance', models.IntegerField()),
                ('contest_type_id', models.IntegerField()),
                ('contest_effect_id', models.IntegerField()),
                ('super_contest_effect_id', models.IntegerField()),
                ('generation', models.ForeignKey(blank=True, to='pokemon_v2.Generation', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MoveBattleStyle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MoveBattleStyleName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('language', models.ForeignKey(blank=True, to='pokemon_v2.Language', null=True)),
                ('move_battle_style', models.ForeignKey(blank=True, to='pokemon_v2.MoveBattleStyle', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MoveChange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('power', models.IntegerField()),
                ('pp', models.IntegerField()),
                ('accuracy', models.IntegerField()),
                ('move_effect_chance', models.IntegerField()),
                ('move', models.ForeignKey(blank=True, to='pokemon_v2.Move', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MoveDamageClass',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MoveDamageClassDescription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(default='', max_length=1000)),
                ('name', models.CharField(max_length=100)),
                ('language', models.ForeignKey(blank=True, to='pokemon_v2.Language', null=True)),
                ('move_damage_class', models.ForeignKey(blank=True, to='pokemon_v2.MoveDamageClass', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MoveEffect',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MoveEffectChange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('move_effect', models.ForeignKey(blank=True, to='pokemon_v2.MoveEffect', null=True)),
                ('version_group', models.ForeignKey(blank=True, to='pokemon_v2.VersionGroup', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MoveEffectChangeDescription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('effect', models.CharField(max_length=2000)),
                ('language', models.ForeignKey(blank=True, to='pokemon_v2.Language', null=True)),
                ('move_effect_change', models.ForeignKey(blank=True, to='pokemon_v2.MoveEffectChange', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MoveEffectDescription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('short_effect', models.CharField(max_length=300)),
                ('effect', models.CharField(max_length=4000)),
                ('language', models.ForeignKey(blank=True, to='pokemon_v2.Language', null=True)),
                ('move_effect', models.ForeignKey(blank=True, to='pokemon_v2.MoveEffect', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MoveFlag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MoveFlagDescription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(default='', max_length=1000)),
                ('name', models.CharField(max_length=100)),
                ('language', models.ForeignKey(blank=True, to='pokemon_v2.Language', null=True)),
                ('move_flag', models.ForeignKey(blank=True, to='pokemon_v2.MoveFlag', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MoveFlagMap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('move', models.ForeignKey(blank=True, to='pokemon_v2.Move', null=True)),
                ('move_flag', models.ForeignKey(blank=True, to='pokemon_v2.MoveFlag', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MoveFlavorText',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('flavor_text', models.CharField(max_length=500)),
                ('language', models.ForeignKey(blank=True, to='pokemon_v2.Language', null=True)),
                ('move', models.ForeignKey(blank=True, to='pokemon_v2.Move', null=True)),
                ('version_group', models.ForeignKey(blank=True, to='pokemon_v2.VersionGroup', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MoveMeta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('min_hits', models.IntegerField()),
                ('max_hits', models.IntegerField()),
                ('min_turns', models.IntegerField()),
                ('max_turns', models.IntegerField()),
                ('drain', models.BooleanField(default=False)),
                ('healing', models.BooleanField(default=False)),
                ('crit_rate', models.IntegerField()),
                ('ailment_chance', models.IntegerField()),
                ('flinch_chance', models.IntegerField()),
                ('stat_chance', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MoveMetaAilment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MoveMetaAilmentName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('language', models.ForeignKey(blank=True, to='pokemon_v2.Language', null=True)),
                ('move_meta_ailment', models.ForeignKey(blank=True, to='pokemon_v2.MoveMetaAilment', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MoveMetaCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MoveMetaCategoryDescription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(default='', max_length=1000)),
                ('language', models.ForeignKey(blank=True, to='pokemon_v2.Language', null=True)),
                ('move_meta_category', models.ForeignKey(blank=True, to='pokemon_v2.MoveMetaCategory', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MoveMetaStatChange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('change', models.IntegerField()),
                ('move', models.ForeignKey(blank=True, to='pokemon_v2.Move', null=True)),
                ('stat', models.ForeignKey(blank=True, to='pokemon_v2.Stat', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MoveName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('language', models.ForeignKey(blank=True, to='pokemon_v2.Language', null=True)),
                ('move', models.ForeignKey(blank=True, to='pokemon_v2.Move', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MoveTarget',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MoveTargetDescription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(default='', max_length=1000)),
                ('name', models.CharField(max_length=100)),
                ('language', models.ForeignKey(blank=True, to='pokemon_v2.Language', null=True)),
                ('move_target', models.ForeignKey(blank=True, to='pokemon_v2.MoveTarget', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='movemeta',
            name='move_meta_category',
            field=models.ForeignKey(blank=True, to='pokemon_v2.MoveMetaCategory', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='movemeta',
            name='move',
            field=models.ForeignKey(blank=True, to='pokemon_v2.Move', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='movemeta',
            name='move_meta_ailment',
            field=models.ForeignKey(blank=True, to='pokemon_v2.MoveMetaAilment', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='movechange',
            name='move_effect',
            field=models.ForeignKey(blank=True, to='pokemon_v2.MoveEffect', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='movechange',
            name='type',
            field=models.ForeignKey(blank=True, to='pokemon_v2.Type', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='movechange',
            name='version_group',
            field=models.ForeignKey(blank=True, to='pokemon_v2.VersionGroup', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='move',
            name='move_damage_class',
            field=models.ForeignKey(blank=True, to='pokemon_v2.MoveDamageClass', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='move',
            name='move_effect',
            field=models.ForeignKey(blank=True, to='pokemon_v2.MoveEffect', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='move',
            name='move_target',
            field=models.ForeignKey(blank=True, to='pokemon_v2.MoveTarget', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='move',
            name='type',
            field=models.ForeignKey(blank=True, to='pokemon_v2.Type', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='move',
            name='accuracy',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='move',
            name='move_effect_chance',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='move',
            name='power',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='move',
            name='pp',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='move',
            name='priority',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='move',
            name='contest_effect_id',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='move',
            name='contest_type_id',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='move',
            name='super_contest_effect_id',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='abilityflavortext',
            name='flavor_text',
            field=models.CharField(max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movechange',
            name='accuracy',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movechange',
            name='move_effect_chance',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movechange',
            name='power',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movechange',
            name='pp',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ability',
            name='name',
            field=models.CharField(max_length=40),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='egggroup',
            name='name',
            field=models.CharField(max_length=40),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='generation',
            name='name',
            field=models.CharField(max_length=40),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='generationname',
            name='name',
            field=models.CharField(max_length=40),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='growthrate',
            name='name',
            field=models.CharField(max_length=40),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='language',
            name='name',
            field=models.CharField(max_length=40),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='move',
            name='name',
            field=models.CharField(max_length=40),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movebattlestyle',
            name='name',
            field=models.CharField(max_length=40),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movedamageclass',
            name='name',
            field=models.CharField(max_length=40),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='moveflag',
            name='name',
            field=models.CharField(max_length=40),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movemetaailment',
            name='name',
            field=models.CharField(max_length=40),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movemetacategory',
            name='name',
            field=models.CharField(max_length=40),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movetarget',
            name='name',
            field=models.CharField(max_length=40),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='nature',
            name='name',
            field=models.CharField(max_length=40),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='stat',
            name='name',
            field=models.CharField(max_length=40),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='type',
            name='name',
            field=models.CharField(max_length=40),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='version',
            name='name',
            field=models.CharField(max_length=40),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='versiongroup',
            name='name',
            field=models.CharField(max_length=40),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ability',
            name='name',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='egggroup',
            name='name',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='generation',
            name='name',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='generationname',
            name='name',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='growthrate',
            name='name',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='language',
            name='name',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='move',
            name='name',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movebattlestyle',
            name='name',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movedamageclass',
            name='name',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='moveflag',
            name='name',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movemetaailment',
            name='name',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movemetacategory',
            name='name',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movetarget',
            name='name',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='nature',
            name='name',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='stat',
            name='name',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='type',
            name='name',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='version',
            name='name',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='versiongroup',
            name='name',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movemeta',
            name='ailment_chance',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movemeta',
            name='crit_rate',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movemeta',
            name='flinch_chance',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movemeta',
            name='max_hits',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movemeta',
            name='max_turns',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movemeta',
            name='min_hits',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movemeta',
            name='min_turns',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movemeta',
            name='stat_chance',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='movemeta',
            name='drain',
        ),
        migrations.RemoveField(
            model_name='movemeta',
            name='healing',
        ),
        migrations.AlterField(
            model_name='movemeta',
            name='ailment_chance',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movemeta',
            name='crit_rate',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movemeta',
            name='flinch_chance',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movemeta',
            name='max_hits',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movemeta',
            name='max_turns',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movemeta',
            name='min_hits',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movemeta',
            name='min_turns',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movemeta',
            name='stat_chance',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='movemeta',
            name='drain',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='movemeta',
            name='healing',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='stat',
            name='damage_class_id',
        ),
        migrations.AddField(
            model_name='stat',
            name='move_damage_class',
            field=models.ForeignKey(blank=True, to='pokemon_v2.MoveDamageClass', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='type',
            name='move_damage_class',
            field=models.ForeignKey(blank=True, to='pokemon_v2.MoveDamageClass', null=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='AbilityChange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ability', models.ForeignKey(blank=True, to='pokemon_v2.Ability', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AbilityChangeDescription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('effect', models.CharField(max_length=1000)),
                ('ability_change', models.ForeignKey(blank=True, to='pokemon_v2.AbilityChange', null=True)),
                ('language', models.ForeignKey(blank=True, to='pokemon_v2.Language', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EvolutionChain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('baby_evolution_item', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EvolutionTrigger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EvolutionTriggerName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('evolution_trigger', models.ForeignKey(blank=True, to='pokemon_v2.EvolutionTrigger', null=True)),
                ('language', models.ForeignKey(blank=True, to='pokemon_v2.Language', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.IntegerField()),
                ('experience', models.IntegerField()),
                ('growth_rate', models.ForeignKey(blank=True, to='pokemon_v2.GrowthRate', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pokedex',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('region_id', models.IntegerField(null=True, blank=True)),
                ('is_main_series', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PokedexDescription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(default='', max_length=1000)),
                ('name', models.CharField(max_length=100)),
                ('language', models.ForeignKey(blank=True, to='pokemon_v2.Language', null=True)),
                ('pokedex', models.ForeignKey(blank=True, to='pokemon_v2.Pokedex', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PokedexVersionGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pokedex', models.ForeignKey(blank=True, to='pokemon_v2.Pokedex', null=True)),
                ('version_group', models.ForeignKey(blank=True, to='pokemon_v2.VersionGroup', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pokemon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('order', models.IntegerField()),
                ('height', models.IntegerField()),
                ('weight', models.IntegerField()),
                ('base_experience', models.IntegerField()),
                ('is_default', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PokemonAbility',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_hidden', models.BooleanField(default=False)),
                ('slot', models.IntegerField()),
                ('ability', models.ForeignKey(blank=True, to='pokemon_v2.Ability', null=True)),
                ('pokemon', models.ForeignKey(blank=True, to='pokemon_v2.Pokemon', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PokemonColor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PokemonColorName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('language', models.ForeignKey(blank=True, to='pokemon_v2.Language', null=True)),
                ('pokemon_color', models.ForeignKey(blank=True, to='pokemon_v2.PokemonColor', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PokemonDexNumber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pokedex_number', models.IntegerField()),
                ('pokedex', models.ForeignKey(blank=True, to='pokemon_v2.Pokedex', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PokemonEggGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('egg_group', models.ForeignKey(blank=True, to='pokemon_v2.EggGroup', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PokemonEvolution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item', models.IntegerField()),
                ('min_level', models.IntegerField()),
                ('location_id', models.IntegerField()),
                ('held_item', models.IntegerField()),
                ('time_of_day', models.CharField(max_length=10)),
                ('min_happiness', models.IntegerField()),
                ('minimum_beauty', models.IntegerField()),
                ('min_affection', models.IntegerField()),
                ('relative_physical_stats', models.IntegerField()),
                ('needs_overworld_rain', models.BooleanField(default=False)),
                ('turn_upside_down', models.BooleanField(default=False)),
                ('evolution_trigger', models.ForeignKey(blank=True, to='pokemon_v2.EvolutionTrigger', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PokemonForm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('order', models.IntegerField()),
                ('form_identifier', models.CharField(max_length=30)),
                ('is_default', models.BooleanField(default=False)),
                ('is_battle_only', models.BooleanField(default=False)),
                ('is_mega_form_order', models.BooleanField(default=False)),
                ('introduces_in_version_group', models.ForeignKey(blank=True, to='pokemon_v2.VersionGroup', null=True)),
                ('pokemon', models.ForeignKey(blank=True, to='pokemon_v2.Pokemon', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PokemonFormGeneration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('game_index', models.IntegerField()),
                ('generation', models.ForeignKey(blank=True, to='pokemon_v2.Generation', null=True)),
                ('pokemon_form', models.ForeignKey(blank=True, to='pokemon_v2.PokemonForm', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PokemonFormName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('pokemon_name', models.CharField(max_length=30)),
                ('language', models.ForeignKey(blank=True, to='pokemon_v2.Language', null=True)),
                ('pokemon_form', models.ForeignKey(blank=True, to='pokemon_v2.PokemonForm', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PokemonGameIndex',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('game_index', models.IntegerField()),
                ('pokemon', models.ForeignKey(blank=True, to='pokemon_v2.Pokemon', null=True)),
                ('version', models.ForeignKey(blank=True, to='pokemon_v2.Version', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PokemonHabitat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PokemonHabitatName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('language', models.ForeignKey(blank=True, to='pokemon_v2.Language', null=True)),
                ('pokemon_habitat', models.ForeignKey(blank=True, to='pokemon_v2.PokemonHabitat', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PokemonItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item_id', models.IntegerField()),
                ('rarity', models.IntegerField()),
                ('pokemon', models.ForeignKey(blank=True, to='pokemon_v2.Pokemon', null=True)),
                ('version', models.ForeignKey(blank=True, to='pokemon_v2.Version', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PokemonMove',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField()),
                ('level', models.IntegerField()),
                ('move', models.ForeignKey(blank=True, to='pokemon_v2.Move', null=True)),
                ('pokemon', models.ForeignKey(blank=True, to='pokemon_v2.Pokemon', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PokemonMoveMethod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PokemonMoveMethodName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(default='', max_length=1000)),
                ('name', models.CharField(max_length=100)),
                ('language', models.ForeignKey(blank=True, to='pokemon_v2.Language', null=True)),
                ('pokemon_move_method', models.ForeignKey(blank=True, to='pokemon_v2.PokemonMoveMethod', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PokemonShape',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PokemonShapeName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('awesome_name', models.CharField(max_length=30)),
                ('language', models.ForeignKey(blank=True, to='pokemon_v2.Language', null=True)),
                ('pokemon_shape', models.ForeignKey(blank=True, to='pokemon_v2.PokemonShape', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PokemonSpecies',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('order', models.IntegerField()),
                ('gender_rate', models.IntegerField()),
                ('capture_rate', models.IntegerField()),
                ('base_happiness', models.IntegerField()),
                ('is_baby', models.BooleanField()),
                ('hatch_counter', models.IntegerField()),
                ('has_gender_differences', models.BooleanField()),
                ('forms_switchable', models.BooleanField()),
                ('evolution_chain', models.ForeignKey(blank=True, to='pokemon_v2.EvolutionChain', null=True)),
                ('evolves_from_species', models.ForeignKey(blank=True, to='pokemon_v2.PokemonSpecies', null=True)),
                ('generation', models.ForeignKey(blank=True, to='pokemon_v2.Generation', null=True)),
                ('growth_rate', models.ForeignKey(blank=True, to='pokemon_v2.GrowthRate', null=True)),
                ('pokemon_color', models.ForeignKey(blank=True, to='pokemon_v2.PokemonColor', null=True)),
                ('pokemon_habitat', models.ForeignKey(blank=True, to='pokemon_v2.PokemonHabitat', null=True)),
                ('pokemon_shape', models.ForeignKey(blank=True, to='pokemon_v2.PokemonShape', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PokemonSpeciesDescription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(default='', max_length=1000)),
                ('language', models.ForeignKey(blank=True, to='pokemon_v2.Language', null=True)),
                ('pokemon_species', models.ForeignKey(blank=True, to='pokemon_v2.PokemonSpecies', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PokemonSpeciesFlavorText',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('flavor_text', models.CharField(max_length=500)),
                ('language', models.ForeignKey(blank=True, to='pokemon_v2.Language', null=True)),
                ('pokemon_species', models.ForeignKey(blank=True, to='pokemon_v2.PokemonSpecies', null=True)),
                ('version', models.ForeignKey(blank=True, to='pokemon_v2.Version', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PokemonSpeciesName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('genus', models.CharField(max_length=30)),
                ('language', models.ForeignKey(blank=True, to='pokemon_v2.Language', null=True)),
                ('pokemon_species', models.ForeignKey(blank=True, to='pokemon_v2.PokemonSpecies', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PokemonStat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('base_stat', models.IntegerField()),
                ('effort', models.IntegerField()),
                ('pokemon', models.ForeignKey(blank=True, to='pokemon_v2.Pokemon', null=True)),
                ('stat', models.ForeignKey(blank=True, to='pokemon_v2.Stat', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PokemonType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slot', models.IntegerField()),
                ('pokemon', models.ForeignKey(blank=True, to='pokemon_v2.Pokemon', null=True)),
                ('type', models.ForeignKey(blank=True, to='pokemon_v2.Type', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='pokemonmove',
            name='pokemon_move_method',
            field=models.ForeignKey(blank=True, to='pokemon_v2.PokemonMoveMethod', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pokemonmove',
            name='version_group',
            field=models.ForeignKey(blank=True, to='pokemon_v2.VersionGroup', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pokemonevolution',
            name='evolved_species',
            field=models.ForeignKey(related_name='evolved_species', blank=True, to='pokemon_v2.PokemonSpecies', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pokemonevolution',
            name='gender',
            field=models.ForeignKey(blank=True, to='pokemon_v2.Gender', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pokemonevolution',
            name='known_move',
            field=models.ForeignKey(blank=True, to='pokemon_v2.Move', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pokemonevolution',
            name='known_move_type',
            field=models.ForeignKey(related_name='known_move', blank=True, to='pokemon_v2.Type', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pokemonevolution',
            name='party_species',
            field=models.ForeignKey(related_name='party_species', blank=True, to='pokemon_v2.PokemonSpecies', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pokemonevolution',
            name='party_type',
            field=models.ForeignKey(related_name='party_type', blank=True, to='pokemon_v2.Type', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pokemonevolution',
            name='trade_species',
            field=models.ForeignKey(related_name='trade_species', blank=True, to='pokemon_v2.PokemonSpecies', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pokemonegggroup',
            name='pokemon_species',
            field=models.ForeignKey(blank=True, to='pokemon_v2.PokemonSpecies', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pokemondexnumber',
            name='pokemon_species',
            field=models.ForeignKey(blank=True, to='pokemon_v2.PokemonSpecies', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pokemon',
            name='pokemon_species',
            field=models.ForeignKey(blank=True, to='pokemon_v2.PokemonSpecies', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokemonspecies',
            name='forms_switchable',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokemonspecies',
            name='has_gender_differences',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokemonspecies',
            name='is_baby',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.RenameField(
            model_name='evolutionchain',
            old_name='baby_evolution_item',
            new_name='baby_evolution_item_id',
        ),
        migrations.AlterField(
            model_name='evolutionchain',
            name='baby_evolution_item_id',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='abilityflavortext',
            name='flavor_text',
            field=models.CharField(max_length=500),
            preserve_default=True,
        ),
        migrations.RenameField(
            model_name='pokemonevolution',
            old_name='minimum_beauty',
            new_name='min_beauty',
        ),
        migrations.RenameField(
            model_name='pokemonevolution',
            old_name='item',
            new_name='evolution_item_id',
        ),
        migrations.RenameField(
            model_name='pokemonevolution',
            old_name='held_item',
            new_name='held_item_id',
        ),
        migrations.AlterField(
            model_name='pokemonevolution',
            name='evolution_item_id',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokemonevolution',
            name='held_item_id',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokemonevolution',
            name='location_id',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokemonevolution',
            name='min_affection',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokemonevolution',
            name='min_beauty',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokemonevolution',
            name='min_happiness',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokemonevolution',
            name='relative_physical_stats',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokemonevolution',
            name='min_level',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokemonevolution',
            name='time_of_day',
            field=models.CharField(max_length=10, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.RenameField(
            model_name='pokemonform',
            old_name='is_mega_form_order',
            new_name='is_mega',
        ),
        migrations.AddField(
            model_name='pokemonform',
            name='form_order',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.RenameField(
            model_name='pokemonform',
            old_name='introduces_in_version_group',
            new_name='introduced_in_version_group',
        ),
        migrations.AlterField(
            model_name='language',
            name='order',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='order',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokemonform',
            name='order',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokemonmove',
            name='order',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pokemonspecies',
            name='order',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='versiongroup',
            name='order',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('machine_number', models.IntegerField()),
                ('item_id', models.IntegerField()),
                ('growth_rate', models.ForeignKey(blank=True, to='pokemon_v2.GrowthRate', null=True)),
                ('move', models.ForeignKey(blank=True, to='pokemon_v2.Move', null=True)),
                ('version_group', models.ForeignKey(blank=True, to='pokemon_v2.VersionGroup', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
