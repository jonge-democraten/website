# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0024_visionpage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visionpage',
            name='vision',
            field=models.ForeignKey(blank=True, null=True, to='jdpages.Vision'),
        ),
    ]
