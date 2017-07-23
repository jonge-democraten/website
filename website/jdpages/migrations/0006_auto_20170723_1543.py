# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0005_auto_20170723_1528'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sidebaragenda',
            options={'verbose_name': 'Sidebar Agenda Item'},
        ),
        migrations.AlterModelOptions(
            name='sidebarlinks',
            options={'verbose_name': 'Sidebar Links Item'},
        ),
        migrations.AlterModelOptions(
            name='sidebarrichtext',
            options={'verbose_name': 'Sidebar RichText Item'},
        ),
        migrations.AlterModelOptions(
            name='sidebarsocial',
            options={'verbose_name': 'Sidebar Social Media Item'},
        ),
        migrations.AlterModelOptions(
            name='sidebartwitter',
            options={'verbose_name': 'Sidebar Twitter Item'},
        ),
        migrations.AddField(
            model_name='sidebaragenda',
            name='visible',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='sidebarlinks',
            name='visible',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='sidebarrichtext',
            name='visible',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='sidebarsocial',
            name='visible',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='sidebartwitter',
            name='visible',
            field=models.BooleanField(default=True),
        ),
    ]
