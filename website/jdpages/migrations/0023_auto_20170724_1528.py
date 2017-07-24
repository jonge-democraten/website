# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0022_homepage_visions'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='VisionPage',
            new_name='VisionsPage',
        ),
    ]
