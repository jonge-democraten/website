# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0002_auto_orderfield_verbose_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='columnelement',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='columnelement',
            name='site',
        ),
        migrations.RemoveField(
            model_name='columnelementwidget',
            name='column_element',
        ),
        migrations.RemoveField(
            model_name='columnelementwidget',
            name='page',
        ),
        migrations.RemoveField(
            model_name='columnelementwidget',
            name='site',
        ),
        migrations.RemoveField(
            model_name='sidebartabswidget',
            name='sidebar',
        ),
        migrations.RemoveField(
            model_name='sidebartabswidget',
            name='site',
        ),
        migrations.RemoveField(
            model_name='socialmediabutton',
            name='sidebar',
        ),
        migrations.RemoveField(
            model_name='socialmediabutton',
            name='site',
        ),
        migrations.DeleteModel(
            name='ColumnElement',
        ),
        migrations.DeleteModel(
            name='ColumnElementWidget',
        ),
        migrations.DeleteModel(
            name='SidebarTabsWidget',
        ),
        migrations.DeleteModel(
            name='SocialMediaButton',
        ),
    ]
