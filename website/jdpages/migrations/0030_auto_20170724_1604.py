# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0029_auto_20170724_1548'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vision',
            name='site',
        ),
        migrations.RemoveField(
            model_name='visionpage',
            name='vision',
        ),
        migrations.AddField(
            model_name='visionpage',
            name='content',
            field=mezzanine.core.fields.RichTextField(default='default content', verbose_name='Content'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='visionpage',
            name='image',
            field=mezzanine.core.fields.FileField(blank=True, default='', max_length=300),
        ),
        migrations.DeleteModel(
            name='Vision',
        ),
    ]
