# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0003_auto_20150422_2349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='columnelementwidget',
            name='page',
            field=models.ForeignKey(null=True, to='pages.Page'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pageheaderimagewidget',
            name='page',
            field=models.ForeignKey(null=True, to='pages.Page'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pageheadersettingswidget',
            name='page',
            field=models.OneToOneField(null=True, to='pages.Page'),
            preserve_default=True,
        ),
    ]
