# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0010_auto_20170723_1638'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventcolumnelement',
            name='site',
        ),
        migrations.DeleteModel(
            name='EventColumnElement',
        ),
    ]
