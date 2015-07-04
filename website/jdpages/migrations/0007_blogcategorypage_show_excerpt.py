# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0006_columnelement_subtype'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogcategorypage',
            name='show_excerpt',
            field=models.BooleanField(default=False, help_text='Show only the first paragraph of a blog post.'),
            preserve_default=True,
        ),
    ]
