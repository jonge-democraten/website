# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20150527_1555'),
        ('jdpages', '0006_auto_20170723_1543'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sidebarlinks',
            name='page',
        ),
        migrations.RemoveField(
            model_name='sidebarlinks',
            name='site',
        ),
        migrations.RemoveField(
            model_name='sidebarlink',
            name='sidebar',
        ),
        migrations.AddField(
            model_name='sidebarlink',
            name='page',
            field=models.ForeignKey(to='pages.Page', default=-1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sidebarlink',
            name='visible',
            field=models.BooleanField(default=True),
        ),
        migrations.DeleteModel(
            name='SidebarLinks',
        ),
    ]
