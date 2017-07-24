# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import website.jdpages.models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20150527_1555'),
        ('jdpages', '0030_auto_20170724_1604'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='document_listing',
        ),
        migrations.RemoveField(
            model_name='documentlisting',
            name='page_ptr',
        ),
        migrations.AlterField(
            model_name='visionpage',
            name='image',
            field=mezzanine.core.fields.FileField(max_length=300, blank=True, default='', validators=[website.jdpages.models.validate_vision_image]),
        ),
        migrations.DeleteModel(
            name='Document',
        ),
        migrations.DeleteModel(
            name='DocumentListing',
        ),
    ]
