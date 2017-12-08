# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0013_auto_20171208_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisationmember',
            name='email',
            field=models.EmailField(max_length=254, default='', blank=True),
        ),
    ]
