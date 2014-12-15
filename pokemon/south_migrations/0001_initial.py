# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Ability'
        db.create_table(u'pokemon_ability', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=200)),
        ))
        db.send_create_signal(u'pokemon', ['Ability'])

        # Adding model 'Type'
        db.create_table(u'pokemon_type', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'pokemon', ['Type'])

        # Adding M2M table for field weakness on 'Type'
        m2m_table_name = db.shorten_name(u'pokemon_type_weakness')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_type', models.ForeignKey(orm[u'pokemon.type'], null=False)),
            ('to_type', models.ForeignKey(orm[u'pokemon.type'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_type_id', 'to_type_id'])

        # Adding M2M table for field resistance on 'Type'
        m2m_table_name = db.shorten_name(u'pokemon_type_resistance')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_type', models.ForeignKey(orm[u'pokemon.type'], null=False)),
            ('to_type', models.ForeignKey(orm[u'pokemon.type'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_type_id', 'to_type_id'])

        # Adding M2M table for field super_effective on 'Type'
        m2m_table_name = db.shorten_name(u'pokemon_type_super_effective')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_type', models.ForeignKey(orm[u'pokemon.type'], null=False)),
            ('to_type', models.ForeignKey(orm[u'pokemon.type'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_type_id', 'to_type_id'])

        # Adding M2M table for field ineffective on 'Type'
        m2m_table_name = db.shorten_name(u'pokemon_type_ineffective')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_type', models.ForeignKey(orm[u'pokemon.type'], null=False)),
            ('to_type', models.ForeignKey(orm[u'pokemon.type'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_type_id', 'to_type_id'])

        # Adding M2M table for field no_effect on 'Type'
        m2m_table_name = db.shorten_name(u'pokemon_type_no_effect')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_type', models.ForeignKey(orm[u'pokemon.type'], null=False)),
            ('to_type', models.ForeignKey(orm[u'pokemon.type'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_type_id', 'to_type_id'])

        # Adding model 'EggGroup'
        db.create_table(u'pokemon_egggroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('cycles', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
        ))
        db.send_create_signal(u'pokemon', ['EggGroup'])

        # Adding model 'Game'
        db.create_table(u'pokemon_game', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('generation', self.gf('django.db.models.fields.IntegerField')(max_length=4)),
            ('release_year', self.gf('django.db.models.fields.IntegerField')(max_length=6)),
        ))
        db.send_create_signal(u'pokemon', ['Game'])

        # Adding model 'Description'
        db.create_table(u'pokemon_description', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=200)),
        ))
        db.send_create_signal(u'pokemon', ['Description'])

        # Adding M2M table for field game on 'Description'
        m2m_table_name = db.shorten_name(u'pokemon_description_game')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('description', models.ForeignKey(orm[u'pokemon.description'], null=False)),
            ('game', models.ForeignKey(orm[u'pokemon.game'], null=False))
        ))
        db.create_unique(m2m_table_name, ['description_id', 'game_id'])

        # Adding model 'Move'
        db.create_table(u'pokemon_move', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=200)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('power', self.gf('django.db.models.fields.IntegerField')(max_length=6)),
            ('accuracy', self.gf('django.db.models.fields.IntegerField')(max_length=6)),
            ('learn_type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('learn_id', self.gf('django.db.models.fields.IntegerField')(max_length=6)),
        ))
        db.send_create_signal(u'pokemon', ['Move'])

        # Adding M2M table for field etype on 'Move'
        m2m_table_name = db.shorten_name(u'pokemon_move_etype')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('move', models.ForeignKey(orm[u'pokemon.move'], null=False)),
            ('type', models.ForeignKey(orm[u'pokemon.type'], null=False))
        ))
        db.create_unique(m2m_table_name, ['move_id', 'type_id'])

        # Adding model 'Sprite'
        db.create_table(u'pokemon_sprite', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('image', self.gf('imagekit.models.fields.ProcessedImageField')(max_length=100)),
        ))
        db.send_create_signal(u'pokemon', ['Sprite'])

        # Adding model 'Pokemon'
        db.create_table(u'pokemon_pokemon', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('species', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('height', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('weight', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('ev_yield', self.gf('django.db.models.fields.IntegerField')(max_length=3)),
            ('catch_rate', self.gf('django.db.models.fields.IntegerField')(max_length=4)),
            ('happiness', self.gf('django.db.models.fields.IntegerField')(max_length=4)),
            ('exp', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
            ('growth_rate', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('male_female_ratio', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('hp', self.gf('django.db.models.fields.IntegerField')(max_length=4)),
            ('attack', self.gf('django.db.models.fields.IntegerField')(max_length=4)),
            ('defense', self.gf('django.db.models.fields.IntegerField')(max_length=4)),
            ('sp_atk', self.gf('django.db.models.fields.IntegerField')(max_length=4)),
            ('sp_def', self.gf('django.db.models.fields.IntegerField')(max_length=4)),
            ('speed', self.gf('django.db.models.fields.IntegerField')(max_length=4)),
            ('total', self.gf('django.db.models.fields.IntegerField')(max_length=6)),
            ('evolves_at', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=4)),
            ('evolves_to', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pokemon.Pokemon'], blank=True)),
            ('egg_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pokemon.EggGroup'], blank=True)),
        ))
        db.send_create_signal(u'pokemon', ['Pokemon'])

        # Adding M2M table for field abilities on 'Pokemon'
        m2m_table_name = db.shorten_name(u'pokemon_pokemon_abilities')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pokemon', models.ForeignKey(orm[u'pokemon.pokemon'], null=False)),
            ('ability', models.ForeignKey(orm[u'pokemon.ability'], null=False))
        ))
        db.create_unique(m2m_table_name, ['pokemon_id', 'ability_id'])

        # Adding M2M table for field types on 'Pokemon'
        m2m_table_name = db.shorten_name(u'pokemon_pokemon_types')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pokemon', models.ForeignKey(orm[u'pokemon.pokemon'], null=False)),
            ('type', models.ForeignKey(orm[u'pokemon.type'], null=False))
        ))
        db.create_unique(m2m_table_name, ['pokemon_id', 'type_id'])

        # Adding M2M table for field descriptions on 'Pokemon'
        m2m_table_name = db.shorten_name(u'pokemon_pokemon_descriptions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pokemon', models.ForeignKey(orm[u'pokemon.pokemon'], null=False)),
            ('description', models.ForeignKey(orm[u'pokemon.description'], null=False))
        ))
        db.create_unique(m2m_table_name, ['pokemon_id', 'description_id'])

        # Adding M2M table for field sprites on 'Pokemon'
        m2m_table_name = db.shorten_name(u'pokemon_pokemon_sprites')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pokemon', models.ForeignKey(orm[u'pokemon.pokemon'], null=False)),
            ('sprite', models.ForeignKey(orm[u'pokemon.sprite'], null=False))
        ))
        db.create_unique(m2m_table_name, ['pokemon_id', 'sprite_id'])

        # Adding M2M table for field moves on 'Pokemon'
        m2m_table_name = db.shorten_name(u'pokemon_pokemon_moves')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pokemon', models.ForeignKey(orm[u'pokemon.pokemon'], null=False)),
            ('move', models.ForeignKey(orm[u'pokemon.move'], null=False))
        ))
        db.create_unique(m2m_table_name, ['pokemon_id', 'move_id'])


    def backwards(self, orm):
        # Deleting model 'Ability'
        db.delete_table(u'pokemon_ability')

        # Deleting model 'Type'
        db.delete_table(u'pokemon_type')

        # Removing M2M table for field weakness on 'Type'
        db.delete_table(db.shorten_name(u'pokemon_type_weakness'))

        # Removing M2M table for field resistance on 'Type'
        db.delete_table(db.shorten_name(u'pokemon_type_resistance'))

        # Removing M2M table for field super_effective on 'Type'
        db.delete_table(db.shorten_name(u'pokemon_type_super_effective'))

        # Removing M2M table for field ineffective on 'Type'
        db.delete_table(db.shorten_name(u'pokemon_type_ineffective'))

        # Removing M2M table for field no_effect on 'Type'
        db.delete_table(db.shorten_name(u'pokemon_type_no_effect'))

        # Deleting model 'EggGroup'
        db.delete_table(u'pokemon_egggroup')

        # Deleting model 'Game'
        db.delete_table(u'pokemon_game')

        # Deleting model 'Description'
        db.delete_table(u'pokemon_description')

        # Removing M2M table for field game on 'Description'
        db.delete_table(db.shorten_name(u'pokemon_description_game'))

        # Deleting model 'Move'
        db.delete_table(u'pokemon_move')

        # Removing M2M table for field etype on 'Move'
        db.delete_table(db.shorten_name(u'pokemon_move_etype'))

        # Deleting model 'Sprite'
        db.delete_table(u'pokemon_sprite')

        # Deleting model 'Pokemon'
        db.delete_table(u'pokemon_pokemon')

        # Removing M2M table for field abilities on 'Pokemon'
        db.delete_table(db.shorten_name(u'pokemon_pokemon_abilities'))

        # Removing M2M table for field types on 'Pokemon'
        db.delete_table(db.shorten_name(u'pokemon_pokemon_types'))

        # Removing M2M table for field descriptions on 'Pokemon'
        db.delete_table(db.shorten_name(u'pokemon_pokemon_descriptions'))

        # Removing M2M table for field sprites on 'Pokemon'
        db.delete_table(db.shorten_name(u'pokemon_pokemon_sprites'))

        # Removing M2M table for field moves on 'Pokemon'
        db.delete_table(db.shorten_name(u'pokemon_pokemon_moves'))


    models = {
        u'pokemon.ability': {
            'Meta': {'object_name': 'Ability'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'pokemon.description': {
            'Meta': {'object_name': 'Description'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '200'}),
            'game': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['pokemon.Game']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'pokemon.egggroup': {
            'Meta': {'object_name': 'EggGroup'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'cycles': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'pokemon.game': {
            'Meta': {'object_name': 'Game'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'generation': ('django.db.models.fields.IntegerField', [], {'max_length': '4'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'release_year': ('django.db.models.fields.IntegerField', [], {'max_length': '6'})
        },
        u'pokemon.move': {
            'Meta': {'object_name': 'Move'},
            'accuracy': ('django.db.models.fields.IntegerField', [], {'max_length': '6'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '200'}),
            'etype': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['pokemon.Type']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'learn_id': ('django.db.models.fields.IntegerField', [], {'max_length': '6'}),
            'learn_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'power': ('django.db.models.fields.IntegerField', [], {'max_length': '6'})
        },
        u'pokemon.pokemon': {
            'Meta': {'object_name': 'Pokemon'},
            'abilities': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['pokemon.Ability']", 'symmetrical': 'False', 'blank': 'True'}),
            'attack': ('django.db.models.fields.IntegerField', [], {'max_length': '4'}),
            'catch_rate': ('django.db.models.fields.IntegerField', [], {'max_length': '4'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'defense': ('django.db.models.fields.IntegerField', [], {'max_length': '4'}),
            'descriptions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['pokemon.Description']", 'symmetrical': 'False', 'blank': 'True'}),
            'egg_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pokemon.EggGroup']", 'blank': 'True'}),
            'ev_yield': ('django.db.models.fields.IntegerField', [], {'max_length': '3'}),
            'evolves_at': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '4'}),
            'evolves_to': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pokemon.Pokemon']", 'blank': 'True'}),
            'exp': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'growth_rate': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'happiness': ('django.db.models.fields.IntegerField', [], {'max_length': '4'}),
            'height': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'hp': ('django.db.models.fields.IntegerField', [], {'max_length': '4'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'male_female_ratio': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'moves': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['pokemon.Move']", 'symmetrical': 'False', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'sp_atk': ('django.db.models.fields.IntegerField', [], {'max_length': '4'}),
            'sp_def': ('django.db.models.fields.IntegerField', [], {'max_length': '4'}),
            'species': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'speed': ('django.db.models.fields.IntegerField', [], {'max_length': '4'}),
            'sprites': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['pokemon.Sprite']", 'symmetrical': 'False', 'blank': 'True'}),
            'total': ('django.db.models.fields.IntegerField', [], {'max_length': '6'}),
            'types': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['pokemon.Type']", 'symmetrical': 'False', 'blank': 'True'}),
            'weight': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'pokemon.sprite': {
            'Meta': {'object_name': 'Sprite'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('imagekit.models.fields.ProcessedImageField', [], {'max_length': '100'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'pokemon.type': {
            'Meta': {'object_name': 'Type'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ineffective': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'ineffective_rel_+'", 'blank': 'True', 'to': u"orm['pokemon.Type']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'no_effect': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'no_effect_rel_+'", 'blank': 'True', 'to': u"orm['pokemon.Type']"}),
            'resistance': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'resistance_rel_+'", 'blank': 'True', 'to': u"orm['pokemon.Type']"}),
            'super_effective': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'super_effective_rel_+'", 'blank': 'True', 'to': u"orm['pokemon.Type']"}),
            'weakness': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'weakness_rel_+'", 'blank': 'True', 'to': u"orm['pokemon.Type']"})
        }
    }

    complete_apps = ['pokemon']