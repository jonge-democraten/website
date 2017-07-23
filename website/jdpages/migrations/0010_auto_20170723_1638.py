# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0009_auto_20170723_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='sidebarlink',
            name='title',
            field=models.CharField(blank=True, max_length=100, default=''),
        ),
        migrations.AlterField(
            model_name='sidebarlink',
            name='url',
            field=models.CharField(blank=True, max_length=500, default=''),
        ),
    ]
