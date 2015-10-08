# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import website.jdpages.models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('pages', '__first__'),
        ('sites', '0001_initial'),
        ('blog', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogCategoryPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, serialize=False, auto_created=True, to='pages.Page', primary_key=True)),
                ('content', mezzanine.core.fields.RichTextField(verbose_name='Content')),
                ('show_excerpt', models.BooleanField(help_text='Show only the first paragraph of a blog post.', default=False)),
                ('blog_category', models.ForeignKey(to='blog.BlogCategory')),
            ],
            options={
                'verbose_name': 'Blog category page',
                'ordering': ('_order',),
                'verbose_name_plural': 'Blog category pages',
            },
            bases=('pages.page', models.Model),
        ),
        migrations.CreateModel(
            name='ColumnElement',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=1000, default='', blank=True)),
                ('object_id', models.PositiveIntegerField(verbose_name='related object id', null=True)),
                ('subtype', models.CharField(max_length=2, default='', choices=[('CP', 'Compact')], blank=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', null=True, blank=True)),
                ('site', models.ForeignKey(to='sites.Site', editable=False)),
            ],
            options={
                'verbose_name': 'Column element',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ColumnElementWidget',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('_order', models.IntegerField(verbose_name='Order', null=True)),
                ('title', models.CharField(max_length=1000, default='', blank=True)),
                ('max_items', models.PositiveIntegerField(default=3)),
                ('horizontal_position', models.CharField(default='Right', choices=[('Left', 'Left'), ('Right', 'Right')], max_length=20)),
                ('column_element', models.ForeignKey(to='jdpages.ColumnElement', null=True)),
            ],
            options={
                'verbose_name': 'Column widget',
                'ordering': ('_order',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('_order', models.IntegerField(verbose_name='Order', null=True)),
                ('document', mezzanine.core.fields.FileField(verbose_name='Document', max_length=200)),
                ('description', models.CharField(verbose_name='Description', max_length=1000, blank=True)),
            ],
            options={
                'verbose_name': 'Document',
                'ordering': ('_order',),
                'verbose_name_plural': 'Documents',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DocumentListing',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, serialize=False, auto_created=True, to='pages.Page', primary_key=True)),
                ('content', mezzanine.core.fields.RichTextField(verbose_name='Content')),
            ],
            options={
                'verbose_name': 'Document Listing',
                'ordering': ('_order',),
                'verbose_name_plural': 'Document Listings',
            },
            bases=('pages.page', models.Model),
        ),
        migrations.CreateModel(
            name='EventColumnElement',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('type', models.CharField(choices=[('SI', 'Site'), ('AL', 'All'), ('MA', 'Main site'), ('SM', 'Main and site')], max_length=2)),
                ('site', models.ForeignKey(to='sites.Site', editable=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, serialize=False, auto_created=True, to='pages.Page', primary_key=True)),
                ('content', mezzanine.core.fields.RichTextField(verbose_name='Content')),
            ],
            options={
                'verbose_name': 'Homepage',
                'ordering': ('_order',),
            },
            bases=('pages.page', models.Model),
        ),
        migrations.CreateModel(
            name='PageHeaderImageWidget',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=1000, default='', blank=True)),
                ('image', mezzanine.core.fields.FileField(validators=[website.jdpages.models.validate_header_image], max_length=200)),
                ('page', models.ForeignKey(to='pages.Page', null=True)),
                ('site', models.ForeignKey(to='sites.Site', editable=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sidebar',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('site', models.ForeignKey(to='sites.Site', editable=False)),
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
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(default='', max_length=200)),
                ('active', models.BooleanField(default=True)),
                ('image', mezzanine.core.fields.FileField(max_length=200)),
                ('url', models.URLField(help_text='http://www.example.com')),
                ('description', models.CharField(help_text='This is shown as tooltip and alt text.', max_length=200, default='', blank=True)),
            ],
            options={
                'verbose_name': 'Global sidebar banner',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SidebarBlogCategoryWidget',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(default='', max_length=200)),
                ('blog_category', models.ForeignKey(to='blog.BlogCategory', null=True)),
                ('sidebar', models.ForeignKey(to='jdpages.Sidebar')),
                ('site', models.ForeignKey(to='sites.Site', editable=False)),
            ],
            options={
                'verbose_name': 'Sidebar blogcategory',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SidebarTabsWidget',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('active', models.BooleanField(default=True)),
                ('sidebar', models.OneToOneField(to='jdpages.Sidebar')),
                ('site', models.ForeignKey(to='sites.Site', editable=False)),
            ],
            options={
                'verbose_name': 'Sidebar tabs widget',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SidebarTwitterWidget',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('active', models.BooleanField(default=False)),
                ('sidebar', models.OneToOneField(to='jdpages.Sidebar')),
                ('site', models.ForeignKey(to='sites.Site', editable=False)),
            ],
            options={
                'verbose_name': 'Sidebar twitter widget',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SocialMediaButton',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('_order', models.IntegerField(verbose_name='Order', null=True)),
                ('type', models.CharField(choices=[('FB', 'Facebook'), ('LI', 'LinkedIn'), ('TW', 'Twitter'), ('YT', 'YouTube')], max_length=2)),
                ('url', models.URLField()),
                ('sidebar', models.ForeignKey(to='jdpages.Sidebar')),
                ('site', models.ForeignKey(to='sites.Site', editable=False)),
            ],
            options={
                'verbose_name': 'Social media button',
                'ordering': ('_order',),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='document',
            name='document_listing',
            field=models.ForeignKey(to='jdpages.DocumentListing', related_name='documents'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='columnelementwidget',
            name='page',
            field=models.ForeignKey(to='pages.Page', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='columnelementwidget',
            name='site',
            field=models.ForeignKey(to='sites.Site', editable=False),
            preserve_default=True,
        ),
    ]
