# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0002_blogcategory_required'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BlogPage',
            new_name='BlogCategoryPage',
        ),
        migrations.AlterModelOptions(
            name='blogcategorypage',
            options={'verbose_name_plural': 'Blog Category Pages', 'verbose_name': 'Blog Category Page', 'ordering': ('_order',)},
        ),
    ]
