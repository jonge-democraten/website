# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0028_auto_20170724_1547'),
    ]

    operations = [
        migrations.RenameField(
            model_name='homepage',
            old_name='visions',
            new_name='vision_pages',
        ),
    ]
