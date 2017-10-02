# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0007_auto_20170922_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='sidebarrichtext',
            name='title',
            field=models.CharField(max_length=100, default='', blank=True),
        ),
    ]
