# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0021_auto_20170724_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='visions',
            field=models.ManyToManyField(to='jdpages.Vision'),
        ),
    ]
