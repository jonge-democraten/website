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
            name='JDColumnItem',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('object_id', models.PositiveIntegerField(null=True, verbose_name='related object id')),
                ('content_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True)),
                ('site', models.ForeignKey(default=1, to='sites.Site')),
            ],
            options={
                'verbose_name': 'JD Column Item',
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
        migrations.AddField(
            model_name='jdhomepage',
            name='column_items_left',
            field=models.ManyToManyField(blank=True, to='jdpages.JDColumnItem', null=True, related_name='column_items_left'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='jdhomepage',
            name='column_items_right',
            field=models.ManyToManyField(blank=True, to='jdpages.JDColumnItem', null=True, related_name='column_items_right'),
            preserve_default=True,
        ),
    ]
