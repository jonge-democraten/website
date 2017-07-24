# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0018_visionpage_visions'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='visionpage',
            options={'verbose_name': 'Visions', 'ordering': ('_order',)},
        ),
    ]
