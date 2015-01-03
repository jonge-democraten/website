# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('sites', '0001_initial'),
        ('pages', '__first__'),
        ('jdpages', '0002_jdhomepage'),
    ]

    operations = [
        migrations.CreateModel(
            name='ColumnElement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=1000, default='', blank=True)),
                ('object_id', models.PositiveIntegerField(null=True, verbose_name='related object id')),
                ('max_items', models.PositiveIntegerField(default=3)),
            ],
            options={
                'verbose_name': 'Column element',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BlogCategoryElement',
            fields=[
                ('columnelement_ptr', models.OneToOneField(parent_link=True, auto_created=True, serialize=False, to='jdpages.ColumnElement', primary_key=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('jdpages.columnelement',),
        ),
        migrations.CreateModel(
            name='ColumnElementWidget',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('_order', models.IntegerField(null=True, verbose_name='Order')),
                ('horizontal_position', models.CharField(max_length=20, choices=[('Left', 'Left'), ('Right', 'Right')], default='Right')),
                ('column_element', models.ForeignKey(to='jdpages.ColumnElement', null=True)),
                ('page', models.ForeignKey(to='pages.Page', null=True)),
                ('site', models.ForeignKey(to='sites.Site', editable=False)),
            ],
            options={
                'verbose_name': 'Column element widget',
                'ordering': ('_order',),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='columnelement',
            name='content_type',
            field=models.ForeignKey(null=True, to='contenttypes.ContentType', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='columnelement',
            name='site',
            field=models.ForeignKey(to='sites.Site', editable=False),
            preserve_default=True,
        ),
        migrations.AlterModelOptions(
            name='jdhomepage',
            options={'ordering': ('_order',), 'verbose_name': 'JD Homepage'},
        ),
        migrations.AlterModelOptions(
            name='jdpage',
            options={'ordering': ('_order',), 'verbose_name': 'JD Page'},
        ),
    ]
