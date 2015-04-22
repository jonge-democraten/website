# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='blog_category',
            field=models.ForeignKey(default=1, to='blog.BlogCategory'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='eventcolumnelement',
            name='type',
            field=models.CharField(choices=[('SI', 'Site'), ('AL', 'All'), ('SM', 'Main and site')], max_length=2),
            preserve_default=True,
        ),
    ]
