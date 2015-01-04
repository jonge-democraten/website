# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '__first__'),
        ('sites', '0001_initial'),
        ('contenttypes', '0001_initial'),
        ('jdpages', '0003_documentlisting'),
    ]

    operations = [
        migrations.CreateModel(
            name='ColumnElement',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField(verbose_name='related object id', null=True)),
                ('content_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True)),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('_order', models.IntegerField(verbose_name='Order', null=True)),
                ('title', models.CharField(max_length=1000, default='', blank=True)),
                ('max_items', models.PositiveIntegerField(default=3)),
                ('horizontal_position', models.CharField(choices=[('Left', 'Left'), ('Right', 'Right')], default='Right', max_length=20)),
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
        migrations.RenameModel(
            old_name='JDHomePage',
            new_name='HomePage',
        ),
        migrations.AlterModelOptions(
            name='homepage',
            options={'ordering': ('_order',), 'verbose_name': 'Homepage'},
        ),
        migrations.AlterModelOptions(
            name='jdpage',
            options={'ordering': ('_order',), 'verbose_name': 'JD Page'},
        ),
    ]
