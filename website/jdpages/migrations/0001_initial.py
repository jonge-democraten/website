# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import website.jdpages.models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '__first__'),
        ('sites', '0001_initial'),
        ('contenttypes', '0001_initial'),
        ('blog', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='ColumnElement',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(blank=True, default='', max_length=1000)),
                ('object_id', models.PositiveIntegerField(null=True, verbose_name='related object id')),
                ('content_type', models.ForeignKey(blank=True, null=True, to='contenttypes.ContentType')),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
            ],
            options={
                'verbose_name': 'Column element',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ColumnElementWidget',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('_order', models.IntegerField(null=True, verbose_name='Order')),
                ('title', models.CharField(blank=True, default='', max_length=1000)),
                ('max_items', models.PositiveIntegerField(default=3)),
                ('horizontal_position', models.CharField(choices=[('Left', 'Left'), ('Right', 'Right')], max_length=20, default='Right')),
                ('column_element', models.ForeignKey(null=True, to='jdpages.ColumnElement')),
            ],
            options={
                'ordering': ('_order',),
                'verbose_name': 'Column widget',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('_order', models.IntegerField(null=True, verbose_name='Order')),
                ('document', mezzanine.core.fields.FileField(verbose_name='Document', max_length=200)),
                ('description', models.CharField(verbose_name='Description', blank=True, max_length=1000)),
            ],
            options={
                'ordering': ('_order',),
                'verbose_name': 'Document',
                'verbose_name_plural': 'Documents',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DocumentListing',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, primary_key=True, to='pages.Page', auto_created=True, serialize=False)),
                ('content', mezzanine.core.fields.RichTextField(verbose_name='Content')),
            ],
            options={
                'ordering': ('_order',),
                'verbose_name': 'Document Listing',
                'verbose_name_plural': 'Document Listings',
            },
            bases=('pages.page', models.Model),
        ),
        migrations.CreateModel(
            name='EventColumnElement',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('type', models.CharField(choices=[('SI', 'Site'), ('MA', 'Main'), ('SM', 'Main and site')], max_length=2)),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, primary_key=True, to='pages.Page', auto_created=True, serialize=False)),
                ('content', mezzanine.core.fields.RichTextField(verbose_name='Content')),
            ],
            options={
                'ordering': ('_order',),
                'verbose_name': 'Homepage',
            },
            bases=('pages.page', models.Model),
        ),
        migrations.CreateModel(
            name='PageHeaderImageWidget',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(blank=True, default='', max_length=1000)),
                ('image', mezzanine.core.fields.FileField(max_length=200, validators=[website.jdpages.models.validate_header_image])),
                ('page', models.ForeignKey(null=True, to='pages.Page')),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PageHeaderSettingsWidget',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('type', models.CharField(choices=[('PA', 'Parent header'), ('NO', 'No header'), ('FB', 'Single image'), ('RA', 'Random image')], max_length=2, default='PA')),
                ('page', models.OneToOneField(null=True, to='pages.Page')),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sidebar',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
            ],
            options={
                'verbose_name': 'Sidebar',
                'verbose_name_plural': 'Sidebar',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SidebarBannerWidget',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('title', models.CharField(default='', max_length=200)),
                ('active', models.BooleanField(default=True)),
                ('image', mezzanine.core.fields.FileField(max_length=200)),
                ('url', models.URLField(help_text='http://www.example.com')),
                ('description', models.CharField(blank=True, default='', max_length=200, help_text='This is shown as tooltip and alt text.')),
            ],
            options={
                'verbose_name': 'Global sidebar banner',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SidebarBlogCategoryWidget',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('title', models.CharField(default='', max_length=200)),
                ('blog_category', models.ForeignKey(null=True, to='blog.BlogCategory')),
                ('sidebar', models.ForeignKey(to='jdpages.Sidebar')),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
            ],
            options={
                'verbose_name': 'Sidebar blogcategory',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SidebarTabsWidget',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('active', models.BooleanField(default=True)),
                ('sidebar', models.OneToOneField(to='jdpages.Sidebar')),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
            ],
            options={
                'verbose_name': 'Sidebar tabs widget',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SidebarTwitterWidget',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('active', models.BooleanField(default=False)),
                ('sidebar', models.OneToOneField(to='jdpages.Sidebar')),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
            ],
            options={
                'verbose_name': 'Sidebar twitter widget',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SocialMediaButton',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('_order', models.IntegerField(null=True, verbose_name='Order')),
                ('type', models.CharField(choices=[('FB', 'Facebook'), ('LI', 'LinkedIn'), ('TW', 'Twitter'), ('YT', 'YouTube')], max_length=2)),
                ('url', models.URLField()),
                ('sidebar', models.ForeignKey(to='jdpages.Sidebar')),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
            ],
            options={
                'ordering': ('_order',),
                'verbose_name': 'Social media button',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='document',
            name='document_listing',
            field=models.ForeignKey(related_name='documents', to='jdpages.DocumentListing'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='columnelementwidget',
            name='page',
            field=models.ForeignKey(null=True, to='pages.Page'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='columnelementwidget',
            name='site',
            field=models.ForeignKey(editable=False, to='sites.Site'),
            preserve_default=True,
        ),
    ]
