# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0004_columnelementwidget'),
    ]

    operations = [
        migrations.AlterField(
            model_name='columnelementwidget',
            name='page',
            field=models.ForeignKey(to='pages.Page', null=True),
            preserve_default=True,
        ),
    ]
