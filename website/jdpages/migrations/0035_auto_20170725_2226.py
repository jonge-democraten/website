# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0034_auto_20170725_0045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='vision_pages',
            field=models.ManyToManyField(to='jdpages.VisionPage', blank=True, null=True),
        ),
    ]
