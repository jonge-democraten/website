# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '__first__'),
        ('jdpages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JDHomePage',
            fields=[
                ('page_ptr', models.OneToOneField(to='pages.Page', auto_created=True, parent_link=True, primary_key=True, serialize=False)),
                ('content', mezzanine.core.fields.RichTextField(verbose_name='Content')),
                ('header_image', models.CharField(max_length=1000, default='', blank=True)),
            ],
            options={
                'ordering': ('_order',),
            },
            bases=('pages.page', models.Model),
        ),
    ]
