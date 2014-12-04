# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MovePokemon'
        db.create_table(u'pokemon_movepokemon', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('pokemon', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='move', null=True, to=orm['pokemon.Pokemon'])),
            ('move', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='pokemon', null=True, to=orm['pokemon.Move'])),
            ('learn_type', self.gf('django.db.models.fields.CharField')(default='level up', max_length=15)),
            ('level', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=6, null=True, blank=True)),
        ))
        db.send_create_signal(u'pokemon', ['MovePokemon'])

        # Deleting field 'Move.learn_type'
        db.delete_column(u'pokemon_move', 'learn_type')

        # Deleting field 'Move.learn_id'
        db.delete_column(u'pokemon_move', 'learn_id')

        # Removing M2M table for field moves on 'Pokemon'
        db.delete_table(db.shorten_name(u'pokemon_pokemon_moves'))


    def backwards(self, orm):
        # Deleting model 'MovePokemon'
        db.delete_table(u'pokemon_movepokemon')

        # Adding field 'Move.learn_type'
        db.add_column(u'pokemon_move', 'learn_type',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=10),
                      keep_default=False)

        # Adding field 'Move.learn_id'
        db.add_column(u'pokemon_move', 'learn_id',
                      self.gf('django.db.models.fields.IntegerField')(default=0, max_length=6),
                      keep_default=False)

        # Adding M2M table for field moves on 'Pokemon'
        m2m_table_name = db.shorten_name(u'pokemon_pokemon_moves')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pokemon', models.ForeignKey(orm[u'pokemon.pokemon'], null=False)),
            ('move', models.ForeignKey(orm[u'pokemon.move'], null=False))
        ))
        db.create_unique(m2m_table_name, ['pokemon_id', 'move_id'])


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
            'game': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['pokemon.Game']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'pokemon.egggroup': {
            'Meta': {'object_name': 'EggGroup'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'pokemon.evolution': {
            'Meta': {'object_name': 'Evolution'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'detail': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'frm': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'frm_evol_pokemon'", 'null': 'True', 'to': u"orm['pokemon.Pokemon']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '3'}),
            'method': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '10'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'to': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'to_evol_pokemon'", 'null': 'True', 'to': u"orm['pokemon.Pokemon']"})
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
            'etype': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['pokemon.Type']", 'null': 'True', 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'power': ('django.db.models.fields.IntegerField', [], {'max_length': '6'}),
            'pp': ('django.db.models.fields.IntegerField', [], {'max_length': '5'})
        },
        u'pokemon.movepokemon': {
            'Meta': {'object_name': 'MovePokemon'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'learn_type': ('django.db.models.fields.CharField', [], {'default': "'level up'", 'max_length': '15'}),
            'level': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'move': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pokemon'", 'null': 'True', 'to': u"orm['pokemon.Move']"}),
            'pokemon': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'move'", 'null': 'True', 'to': u"orm['pokemon.Pokemon']"})
        },
        u'pokemon.pokemon': {
            'Meta': {'object_name': 'Pokemon'},
            'abilities': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['pokemon.Ability']", 'null': 'True', 'blank': 'True'}),
            'attack': ('django.db.models.fields.IntegerField', [], {'max_length': '4'}),
            'catch_rate': ('django.db.models.fields.IntegerField', [], {'max_length': '4'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'defense': ('django.db.models.fields.IntegerField', [], {'max_length': '4'}),
            'descriptions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['pokemon.Description']", 'null': 'True', 'blank': 'True'}),
            'egg_cycles': ('django.db.models.fields.IntegerField', [], {'max_length': '6'}),
            'egg_group': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['pokemon.EggGroup']", 'null': 'True', 'blank': 'True'}),
            'ev_yield': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'exp': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'growth_rate': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'happiness': ('django.db.models.fields.IntegerField', [], {'max_length': '4'}),
            'height': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'hp': ('django.db.models.fields.IntegerField', [], {'max_length': '4'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'male_female_ratio': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'pkdx_id': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'blank': 'True'}),
            'sp_atk': ('django.db.models.fields.IntegerField', [], {'max_length': '4'}),
            'sp_def': ('django.db.models.fields.IntegerField', [], {'max_length': '4'}),
            'species': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'speed': ('django.db.models.fields.IntegerField', [], {'max_length': '4'}),
            'sprites': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['pokemon.Sprite']", 'null': 'True', 'blank': 'True'}),
            'total': ('django.db.models.fields.IntegerField', [], {'max_length': '6'}),
            'types': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['pokemon.Type']", 'null': 'True', 'blank': 'True'}),
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
            'ineffective': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'ineffective_rel_+'", 'null': 'True', 'to': u"orm['pokemon.Type']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'no_effect': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'no_effect_rel_+'", 'null': 'True', 'to': u"orm['pokemon.Type']"}),
            'resistance': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'resistance_rel_+'", 'null': 'True', 'to': u"orm['pokemon.Type']"}),
            'super_effective': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'super_effective_rel_+'", 'null': 'True', 'to': u"orm['pokemon.Type']"}),
            'weakness': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'weakness_rel_+'", 'null': 'True', 'to': u"orm['pokemon.Type']"})
        }
    }

    complete_apps = ['pokemon']