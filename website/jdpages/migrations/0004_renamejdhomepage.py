# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0003_columnelementwidget'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='JDHomePage',
            new_name='HomePage',
        ),
        migrations.AlterModelOptions(
            name='homepage',
            options={'ordering': ('_order',), 'verbose_name': 'Homepage'},
        ),
    ]
