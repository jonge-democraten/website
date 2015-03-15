# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0005_altercolumnelement'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jdpage',
            name='page_ptr',
        ),
        migrations.DeleteModel(
            name='JDPage',
        ),
        migrations.RemoveField(
            model_name='documentlisting',
            name='header_image',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='header_image',
        ),
    ]
