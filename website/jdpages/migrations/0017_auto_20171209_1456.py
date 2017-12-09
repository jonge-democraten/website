# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0016_auto_20171209_1419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisationmember',
            name='content',
            field=mezzanine.core.fields.RichTextField(default='', blank=True),
        ),
    ]
