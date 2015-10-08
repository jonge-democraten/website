# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0007_blogcategorypage_show_excerpt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventcolumnelement',
            name='type',
            field=models.CharField(max_length=2, choices=[('SI', 'Site'), ('AL', 'All'), ('MA', 'Main site'), ('SM', 'Main and site')]),
            preserve_default=True,
        ),
    ]
