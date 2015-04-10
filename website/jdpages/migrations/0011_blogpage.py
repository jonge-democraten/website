# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import website.jdpages.models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '__first__'),
        ('blog', '__first__'),
        ('jdpages', '0010_pageheaderimagewidget_pageheadersettingswidget'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPage',
            fields=[
                ('page_ptr', models.OneToOneField(primary_key=True, to='pages.Page', parent_link=True, serialize=False, auto_created=True)),
                ('content', mezzanine.core.fields.RichTextField(verbose_name='Content')),
                ('blog_categories', models.ManyToManyField(to='blog.BlogCategory', null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Blog Pages',
                'ordering': ('_order',),
                'verbose_name': 'Blog Page',
            },
            bases=('pages.page', models.Model),
        ),
        migrations.AlterField(
            model_name='pageheaderimagewidget',
            name='image',
            field=mezzanine.core.fields.FileField(max_length=200, validators=[website.jdpages.models.validate_header_image]),
            preserve_default=True,
        ),
    ]
