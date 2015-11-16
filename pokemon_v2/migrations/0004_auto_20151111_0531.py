# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_v2', '0003_berryflavormap'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemFlingEffectEffectText',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(default='', max_length=1000)),
                ('item_fling_effect', models.ForeignKey(related_name='itemflingeffecteffecttext', blank=True, to='pokemon_v2.ItemFlingEffect', null=True)),
                ('language', models.ForeignKey(related_name='itemflingeffecteffecttext_language', blank=True, to='pokemon_v2.Language', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='itemflingeffectdescription',
            name='item_fling_effect',
        ),
        migrations.RemoveField(
            model_name='itemflingeffectdescription',
            name='language',
        ),
        migrations.DeleteModel(
            name='ItemFlingEffectDescription',
        ),
    ]
