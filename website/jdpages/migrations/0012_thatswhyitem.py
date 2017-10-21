# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20150527_1555'),
        ('sites', '0001_initial'),
        ('jdpages', '0011_wordlidpage'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThatsWhyItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('_order', mezzanine.core.fields.OrderField(verbose_name='Order', null=True)),
                ('visible', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=100, default='', blank=True)),
                ('page', models.ForeignKey(to='pages.Page', null=True)),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
            ],
            options={
                'verbose_name': "That's why item",
                'verbose_name_plural': "That's why items",
                'ordering': ('_order',),
            },
        ),
    ]
