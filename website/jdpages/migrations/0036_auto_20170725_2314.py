# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0035_auto_20170725_2226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='vision_pages',
            field=models.ManyToManyField(blank=True, to='jdpages.VisionPage'),
        ),
    ]
