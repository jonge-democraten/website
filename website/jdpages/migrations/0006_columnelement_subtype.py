# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0005_remove_pageheadersettingwidget'),
    ]

    operations = [
        migrations.AddField(
            model_name='columnelement',
            name='subtype',
            field=models.CharField(max_length=2, blank=True, default='', choices=[('CP', 'Compact')]),
            preserve_default=True,
        ),
    ]
