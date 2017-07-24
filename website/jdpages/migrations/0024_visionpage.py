# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20150527_1555'),
        ('jdpages', '0023_auto_20170724_1528'),
    ]

    operations = [
        migrations.CreateModel(
            name='VisionPage',
            fields=[
                ('page_ptr', models.OneToOneField(primary_key=True, serialize=False, auto_created=True, parent_link=True, to='pages.Page')),
                ('vision', models.ForeignKey(to='jdpages.Vision')),
            ],
            options={
                'verbose_name': 'VisionPage',
                'ordering': ('_order',),
            },
            bases=('pages.page',),
        ),
    ]
