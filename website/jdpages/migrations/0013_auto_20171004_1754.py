# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0012_auto_20171004_1750'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisationmember',
            name='facebook_url',
            field=models.URLField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='organisationmember',
            name='twitter_url',
            field=models.URLField(blank=True, default=''),
        ),
    ]
