# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0025_auto_20170724_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visionspage',
            name='visions',
            field=models.ManyToManyField(to='jdpages.VisionPage'),
        ),
    ]
