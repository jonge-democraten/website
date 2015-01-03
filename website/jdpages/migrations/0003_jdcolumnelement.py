# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('sites', '0001_initial'),
        ('jdpages', '0002_jdhomepage'),
    ]

    operations = [
        migrations.CreateModel(
            name='JDColumnElement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(blank=True, default='', max_length=1000)),
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
                ('jdcolumnelement_ptr', models.OneToOneField(auto_created=True, to='jdpages.JDColumnElement', serialize=False, primary_key=True, parent_link=True)),
            ],
            options={
            },
            bases=('jdpages.jdcolumnelement',),
        ),
        migrations.AddField(
            model_name='jdcolumnelement',
            name='content_type',
            field=models.ForeignKey(null=True, to='contenttypes.ContentType', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='jdcolumnelement',
            name='site',
            field=models.ForeignKey(default=1, to='sites.Site'),
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
        migrations.AddField(
            model_name='jdhomepage',
            name='column_elements_left',
            field=models.ManyToManyField(blank=True, null=True, related_name='column_elements_left', to='jdpages.JDColumnElement'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='jdhomepage',
            name='column_elements_right',
            field=models.ManyToManyField(blank=True, null=True, related_name='column_elements_right', to='jdpages.JDColumnElement'),
            preserve_default=True,
        ),
    ]
