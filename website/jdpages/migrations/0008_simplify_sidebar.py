# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0007_sidebar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sidebar',
            name='active',
        ),
        migrations.RemoveField(
            model_name='sidebar',
            name='name',
        ),
    ]
