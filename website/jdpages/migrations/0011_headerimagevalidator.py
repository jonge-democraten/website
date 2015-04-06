# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mezzanine.core.fields
import website.jdpages.models


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0010_pageheaderimagewidget_pageheadersettingswidget'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pageheaderimagewidget',
            name='image',
            field=mezzanine.core.fields.FileField(max_length=200, validators=[website.jdpages.models.validate_header_image]),
            preserve_default=True,
        ),
    ]
