# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '__first__'),
        ('jdpages', '0011_blogpage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpage',
            name='blog_categories',
        ),
        migrations.AddField(
            model_name='blogpage',
            name='blog_category',
            field=models.ForeignKey(blank=True, to='blog.BlogCategory', null=True),
            preserve_default=True,
        ),
    ]
