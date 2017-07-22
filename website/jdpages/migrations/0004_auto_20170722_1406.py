# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0003_auto_20170715_1604'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sidebar',
            name='site',
        ),
        migrations.DeleteModel(
            name='SidebarBannerWidget',
        ),
        migrations.RemoveField(
            model_name='sidebarblogcategorywidget',
            name='blog_category',
        ),
        migrations.RemoveField(
            model_name='sidebarblogcategorywidget',
            name='sidebar',
        ),
        migrations.RemoveField(
            model_name='sidebarblogcategorywidget',
            name='site',
        ),
        migrations.RemoveField(
            model_name='sidebartwitterwidget',
            name='sidebar',
        ),
        migrations.RemoveField(
            model_name='sidebartwitterwidget',
            name='site',
        ),
        migrations.DeleteModel(
            name='Sidebar',
        ),
        migrations.DeleteModel(
            name='SidebarBlogCategoryWidget',
        ),
        migrations.DeleteModel(
            name='SidebarTwitterWidget',
        ),
    ]
