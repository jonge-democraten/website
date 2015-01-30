# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0008_simplify_sidebar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='description',
            field=models.CharField(max_length=1000, blank=True, verbose_name='Description'),
            preserve_default=True,
        ),
    ]
