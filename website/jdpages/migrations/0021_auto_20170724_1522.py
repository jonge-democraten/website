# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0020_auto_20170724_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vision',
            name='image',
            field=mezzanine.core.fields.FileField(default='', blank=True, max_length=300),
        ),
    ]
