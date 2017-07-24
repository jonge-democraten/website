# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20150527_1555'),
        ('jdpages', '0015_auto_20170724_1334'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='news_category',
            field=models.ForeignKey(to='blog.BlogCategory', blank=True, null=True),
        ),
    ]
