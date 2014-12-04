# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ResourceView'
        db.create_table(u'hits_resourceview', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('count', self.gf('django.db.models.fields.IntegerField')(max_length=1000)),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'hits', ['ResourceView'])


    def backwards(self, orm):
        # Deleting model 'ResourceView'
        db.delete_table(u'hits_resourceview')


    models = {
        u'hits.resourceview': {
            'Meta': {'object_name': 'ResourceView'},
            'count': ('django.db.models.fields.IntegerField', [], {'max_length': '1000'}),
            'date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['hits']