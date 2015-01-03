# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('contenttypes', '0001_initial'),
        ('jdpages', '0002_jdhomepage'),
    ]

    operations = [
        migrations.CreateModel(
            name='ColumnElementWidget',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(default='', max_length=1000, blank=True)),
                ('object_id', models.PositiveIntegerField(null=True, verbose_name='related object id')),
                ('max_items', models.PositiveIntegerField(default=3)),
            ],
            options={
                'verbose_name': 'Column element widget',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BlogCategoryElement',
            fields=[
                ('columnelementwidget_ptr', models.OneToOneField(serialize=False, primary_key=True, auto_created=True, to='jdpages.ColumnElementWidget', parent_link=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('jdpages.columnelementwidget',),
        ),
        migrations.AddField(
            model_name='columnelementwidget',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='columnelementwidget',
            name='site',
            field=models.ForeignKey(to='sites.Site', editable=False),
            preserve_default=True,
        ),
        migrations.AlterModelOptions(
            name='jdhomepage',
            options={'verbose_name': 'JD Homepage', 'ordering': ('_order',)},
        ),
        migrations.AlterModelOptions(
            name='jdpage',
            options={'verbose_name': 'JD Page', 'ordering': ('_order',)},
        ),
        migrations.AddField(
            model_name='jdhomepage',
            name='column_elements_left',
            field=models.ManyToManyField(to='jdpages.ColumnElementWidget', null=True, related_name='column_elements_left', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='jdhomepage',
            name='column_elements_right',
            field=models.ManyToManyField(to='jdpages.ColumnElementWidget', null=True, related_name='column_elements_right', blank=True),
            preserve_default=True,
        ),
    ]
