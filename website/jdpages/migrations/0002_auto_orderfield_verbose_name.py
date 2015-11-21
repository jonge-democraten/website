# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='columnelementwidget',
            name='_order',
            field=mezzanine.core.fields.OrderField(null=True, verbose_name='Order'),
        ),
        migrations.AlterField(
            model_name='document',
            name='_order',
            field=mezzanine.core.fields.OrderField(null=True, verbose_name='Order'),
        ),
        migrations.AlterField(
            model_name='socialmediabutton',
            name='_order',
            field=mezzanine.core.fields.OrderField(null=True, verbose_name='Order'),
        ),
    ]
