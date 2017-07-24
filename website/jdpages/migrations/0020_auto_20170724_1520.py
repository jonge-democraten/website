# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0019_auto_20170724_1518'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vision',
            options={'verbose_name': 'Vision'},
        ),
        migrations.AlterModelOptions(
            name='visionpage',
            options={'verbose_name': 'VisionsPage', 'ordering': ('_order',)},
        ),
        migrations.AlterField(
            model_name='vision',
            name='title',
            field=models.CharField(default='', max_length=300, blank=True),
        ),
    ]
