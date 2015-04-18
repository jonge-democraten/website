# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mezzanine.core.fields
import website.jdpages.models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '__first__'),
        ('contenttypes', '0001_initial'),
        ('blog', '__first__'),
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPage',
            fields=[
                ('page_ptr', models.OneToOneField(to='pages.Page', parent_link=True, serialize=False, primary_key=True, auto_created=True)),
                ('content', mezzanine.core.fields.RichTextField(verbose_name='Content')),
                ('blog_category', models.ForeignKey(blank=True, null=True, to='blog.BlogCategory')),
            ],
            options={
                'verbose_name': 'Blog Page',
                'verbose_name_plural': 'Blog Pages',
                'ordering': ('_order',),
            },
            bases=('pages.page', models.Model),
        ),
        migrations.CreateModel(
            name='ColumnElement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(blank=True, max_length=1000, default='')),
                ('object_id', models.PositiveIntegerField(null=True, verbose_name='related object id')),
                ('content_type', models.ForeignKey(blank=True, null=True, to='contenttypes.ContentType')),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('_order', models.IntegerField(null=True, verbose_name='Order')),
                ('title', models.CharField(blank=True, max_length=1000, default='')),
                ('max_items', models.PositiveIntegerField(default=3)),
                ('horizontal_position', models.CharField(choices=[('Left', 'Left'), ('Right', 'Right')], max_length=20, default='Right')),
                ('column_element', models.ForeignKey(null=True, to='jdpages.ColumnElement')),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('_order', models.IntegerField(null=True, verbose_name='Order')),
                ('document', mezzanine.core.fields.FileField(verbose_name='Document', max_length=200)),
                ('description', models.CharField(blank=True, max_length=1000, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Document',
                'verbose_name_plural': 'Documents',
                'ordering': ('_order',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DocumentListing',
            fields=[
                ('page_ptr', models.OneToOneField(to='pages.Page', parent_link=True, serialize=False, primary_key=True, auto_created=True)),
                ('content', mezzanine.core.fields.RichTextField(verbose_name='Content')),
            ],
            options={
                'verbose_name': 'Document Listing',
                'verbose_name_plural': 'Document Listings',
                'ordering': ('_order',),
            },
            bases=('pages.page', models.Model),
        ),
        migrations.CreateModel(
            name='EventColumnElement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('type', models.CharField(choices=[('SI', 'Site'), ('MA', 'Main'), ('SM', 'Main and site')], max_length=2)),
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
                ('page_ptr', models.OneToOneField(to='pages.Page', parent_link=True, serialize=False, primary_key=True, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(blank=True, max_length=1000, default='')),
                ('image', mezzanine.core.fields.FileField(max_length=200, validators=[website.jdpages.models.validate_header_image])),
                ('page', models.ForeignKey(null=True, to='pages.Page')),
                ('site', models.ForeignKey(to='sites.Site', editable=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PageHeaderSettingsWidget',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('type', models.CharField(choices=[('PA', 'Parent header'), ('NO', 'No header'), ('FB', 'Single image'), ('RA', 'Random image')], max_length=2, default='PA')),
                ('page', models.OneToOneField(to='pages.Page', null=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=200, default='')),
                ('active', models.BooleanField(default=True)),
                ('image', mezzanine.core.fields.FileField(max_length=200)),
                ('url', models.URLField(help_text='http://www.example.com')),
                ('description', models.CharField(help_text='This is shown as tooltip and alt text.', blank=True, max_length=200, default='')),
            ],
            options={
                'verbose_name': 'Global sidebar banner',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SidebarBlogCategoryWidget',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=200, default='')),
                ('blog_category', models.ForeignKey(null=True, to='blog.BlogCategory')),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('_order', models.IntegerField(null=True, verbose_name='Order')),
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
            field=models.ForeignKey(null=True, to='pages.Page'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='columnelementwidget',
            name='site',
            field=models.ForeignKey(to='sites.Site', editable=False),
            preserve_default=True,
        ),
    ]
