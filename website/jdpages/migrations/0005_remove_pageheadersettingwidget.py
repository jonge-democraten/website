# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0004_auto_20150422_2350'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pageheadersettingswidget',
            name='page',
        ),
        migrations.RemoveField(
            model_name='pageheadersettingswidget',
            name='site',
        ),
        migrations.DeleteModel(
            name='PageHeaderSettingsWidget',
        ),
        migrations.AlterModelOptions(
            name='blogcategorypage',
            options={'verbose_name': 'Blog category page', 'ordering': ('_order',), 'verbose_name_plural': 'Blog category pages'},
        ),
    ]
