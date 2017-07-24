# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0027_auto_20170724_1537'),
    ]

    operations = [
        migrations.RenameField(
            model_name='visionspage',
            old_name='visions',
            new_name='vision_pages',
        ),
    ]
