# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20150527_1555'),
        ('jdpages', '0010_auto_20171019_1357'),
    ]

    operations = [
        migrations.CreateModel(
            name='WordLidPage',
            fields=[
                ('page_ptr', models.OneToOneField(serialize=False, parent_link=True, auto_created=True, primary_key=True, to='pages.Page')),
                ('content', mezzanine.core.fields.RichTextField(verbose_name='Content')),
            ],
            options={
                'verbose_name': 'WordLidPage',
                'ordering': ('_order',),
            },
            bases=('pages.page', models.Model),
        ),
    ]
