# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0014_auto_20170724_1205'),
    ]

    operations = [
        migrations.AddField(
            model_name='actionbanner',
            name='button_title',
            field=models.CharField(max_length=500, default='', blank=True),
        ),
        migrations.AddField(
            model_name='actionbanner',
            name='button_url',
            field=models.CharField(max_length=500, default='', blank=True),
        ),
    ]
