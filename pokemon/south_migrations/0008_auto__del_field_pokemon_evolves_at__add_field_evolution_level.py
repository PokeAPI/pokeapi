# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Pokemon.evolves_at'
        db.delete_column(u'pokemon_pokemon', 'evolves_at')

        # Adding field 'Evolution.level'
        db.add_column(u'pokemon_evolution', 'level',
                      self.gf('django.db.models.fields.IntegerField')(default=0, max_length=3),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Pokemon.evolves_at'
        db.add_column(u'pokemon_pokemon', 'evolves_at',
                      self.gf('django.db.models.fields.IntegerField')(default=0, max_length=4),
                      keep_default=False)

        # Deleting field 'Evolution.level'
        db.delete_column(u'pokemon_evolution', 'level')


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
            'learn_id': ('django.db.models.fields.IntegerField', [], {'max_length': '6'}),
            'learn_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'power': ('django.db.models.fields.IntegerField', [], {'max_length': '6'}),
            'pp': ('django.db.models.fields.IntegerField', [], {'max_length': '5'})
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
            'evolutions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['pokemon.Evolution']", 'null': 'True', 'blank': 'True'}),
            'exp': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'growth_rate': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'happiness': ('django.db.models.fields.IntegerField', [], {'max_length': '4'}),
            'height': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'hp': ('django.db.models.fields.IntegerField', [], {'max_length': '4'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'male_female_ratio': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'moves': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['pokemon.Move']", 'null': 'True', 'blank': 'True'}),
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