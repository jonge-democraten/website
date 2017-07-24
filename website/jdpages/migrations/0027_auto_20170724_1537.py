# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0026_auto_20170724_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='visions',
            field=models.ManyToManyField(to='jdpages.VisionPage'),
        ),
    ]
