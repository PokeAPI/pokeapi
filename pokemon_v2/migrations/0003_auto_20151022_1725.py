# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0002_auto_20151016_0523'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemAttributeDescription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(default='', max_length=1000)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ItemAttributeMap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item', models.ForeignKey(related_name='itemattributemap', blank=True, to='pokemon_v2.Item', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RenameModel(
            old_name='ItemFlag',
            new_name='ItemAttribute',
        ),
        migrations.RemoveField(
            model_name='itemflagdescription',
            name='item_flag',
        ),
        migrations.RemoveField(
            model_name='itemflagdescription',
            name='language',
        ),
        migrations.DeleteModel(
            name='ItemFlagDescription',
        ),
        migrations.RemoveField(
            model_name='itemflagmap',
            name='item',
        ),
        migrations.RemoveField(
            model_name='itemflagmap',
            name='item_flag',
        ),
        migrations.DeleteModel(
            name='ItemFlagMap',
        ),
        migrations.AddField(
            model_name='itemattributemap',
            name='item_attribute',
            field=models.ForeignKey(blank=True, to='pokemon_v2.ItemAttribute', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='itemattributedescription',
            name='item_flag',
            field=models.ForeignKey(blank=True, to='pokemon_v2.ItemAttribute', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='itemattributedescription',
            name='language',
            field=models.ForeignKey(related_name='itemattributedescription_language', blank=True, to='pokemon_v2.Language', null=True),
            preserve_default=True,
        ),
    ]
