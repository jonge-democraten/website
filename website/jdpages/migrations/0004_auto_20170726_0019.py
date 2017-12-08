# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0003_auto_20170725_2349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visionspage',
            name='vision_pages',
            field=models.ManyToManyField(blank=True, to='jdpages.VisionPage'),
        ),
    ]
