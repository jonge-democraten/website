# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0015_auto_20171209_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisationpartmember',
            name='role',
            field=models.CharField(max_length=200, blank=True, default=''),
        ),
    ]
