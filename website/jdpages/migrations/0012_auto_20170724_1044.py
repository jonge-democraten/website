# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0011_auto_20170724_1040'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='header_subtitle',
            field=models.CharField(default='', max_length=500, blank=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='header_title',
            field=models.CharField(default='', max_length=300, blank=True),
        ),
    ]
