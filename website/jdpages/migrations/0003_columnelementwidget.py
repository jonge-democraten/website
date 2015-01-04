# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('pages', '__first__'),
        ('sites', '0001_initial'),
        ('jdpages', '0002_jdhomepage'),
    ]

    operations = [
        migrations.CreateModel(
            name='ColumnElement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.CharField(blank=True, default='', max_length=1000)),
                ('object_id', models.PositiveIntegerField(verbose_name='related object id', null=True)),
                ('max_items', models.PositiveIntegerField(default=3)),
                ('content_type', models.ForeignKey(blank=True, null=True, to='contenttypes.ContentType')),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
            ],
            options={
                'verbose_name': 'Column element',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ColumnElementWidget',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('_order', models.IntegerField(verbose_name='Order', null=True)),
                ('horizontal_position', models.CharField(default='Right', choices=[('Left', 'Left'), ('Right', 'Right')], max_length=20)),
                ('column_element', models.ForeignKey(to='jdpages.ColumnElement', null=True)),
                ('page', models.ForeignKey(to='pages.Page', null=True)),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
            ],
            options={
                'verbose_name': 'Column element widget',
                'ordering': ('_order',),
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='jdhomepage',
            options={'verbose_name': 'JD Homepage', 'ordering': ('_order',)},
        ),
        migrations.AlterModelOptions(
            name='jdpage',
            options={'verbose_name': 'JD Page', 'ordering': ('_order',)},
        ),
    ]
