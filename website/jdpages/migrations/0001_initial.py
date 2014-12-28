# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='JDPage',
            fields=[
                ('page_ptr', models.OneToOneField(primary_key=True, auto_created=True, parent_link=True, to='pages.Page', serialize=False)),
                ('content', mezzanine.core.fields.RichTextField(verbose_name='Content')),
                ('header_image', models.CharField(blank=True, max_length=1000, default='')),
            ],
            options={
                'ordering': ('_order',),
            },
            bases=('pages.page', models.Model),
        ),
    ]
