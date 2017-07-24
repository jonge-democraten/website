# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20150527_1555'),
        ('sites', '0001_initial'),
        ('jdpages', '0016_homepage_news_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vision',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('title', mezzanine.core.fields.RichTextField()),
                ('image', mezzanine.core.fields.FileField(max_length=300)),
                ('content', mezzanine.core.fields.RichTextField()),
                ('site', models.ForeignKey(to='sites.Site', editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VisionPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, to='pages.Page', auto_created=True, serialize=False, primary_key=True)),
                ('content', mezzanine.core.fields.RichTextField(verbose_name='Content')),
            ],
            options={
                'verbose_name': 'VisionPage',
                'ordering': ('_order',),
            },
            bases=('pages.page', models.Model),
        ),
    ]
