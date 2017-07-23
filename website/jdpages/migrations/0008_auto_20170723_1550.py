# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0007_auto_20170723_1545'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sidebarlink',
            options={'ordering': ('_order',)},
        ),
        migrations.AddField(
            model_name='sidebarlink',
            name='_order',
            field=mezzanine.core.fields.OrderField(verbose_name='Order', null=True),
        ),
    ]
