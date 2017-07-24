# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0017_vision_visionpage'),
    ]

    operations = [
        migrations.AddField(
            model_name='visionpage',
            name='visions',
            field=models.ManyToManyField(to='jdpages.Vision'),
        ),
    ]
