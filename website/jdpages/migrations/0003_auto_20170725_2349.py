# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import website.jdpages.models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20150527_1555'),
        ('blog', '0002_auto_20150527_1555'),
        ('sites', '0001_initial'),
        ('jdpages', '0002_auto_orderfield_verbose_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActionBanner',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('visible', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=500, default='', blank=True)),
                ('content', mezzanine.core.fields.RichTextField()),
                ('image', mezzanine.core.fields.FileField(max_length=300)),
                ('button_title', models.CharField(max_length=500, default='', blank=True)),
                ('button_url', models.CharField(max_length=500, default='', blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Footer',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
            ],
            options={
                'verbose_name': 'Footer',
                'verbose_name_plural': 'Footer',
            },
        ),
        migrations.CreateModel(
            name='FooterInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=100, default='', blank=True)),
                ('content', mezzanine.core.fields.RichTextField()),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FooterLink',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('_order', mezzanine.core.fields.OrderField(verbose_name='Order', null=True)),
                ('title', models.CharField(max_length=100, default='', blank=True)),
                ('url', models.CharField(max_length=500, default='', blank=True)),
            ],
            options={
                'ordering': ('_order',),
            },
        ),
        migrations.CreateModel(
            name='FooterLinks',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=100, default='', blank=True)),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PageHeaderImage',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=1000, default='', blank=True)),
                ('image', mezzanine.core.fields.FileField(max_length=200, validators=[website.jdpages.models.validate_header_image])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SidebarAgenda',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('visible', models.BooleanField(default=False)),
                ('type', models.CharField(max_length=2, choices=[('SI', 'Site'), ('AL', 'All'), ('MA', 'Main site'), ('SM', 'Main and site')])),
            ],
            options={
                'verbose_name': 'Sidebar Agenda Item',
            },
        ),
        migrations.CreateModel(
            name='SidebarLink',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('_order', mezzanine.core.fields.OrderField(verbose_name='Order', null=True)),
                ('visible', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=100, default='', blank=True)),
                ('url', models.CharField(max_length=500, default='', blank=True)),
            ],
            options={
                'ordering': ('_order',),
            },
        ),
        migrations.CreateModel(
            name='SidebarRichText',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('visible', models.BooleanField(default=False)),
                ('content', mezzanine.core.fields.RichTextField()),
            ],
            options={
                'verbose_name': 'Sidebar RichText Item',
            },
        ),
        migrations.CreateModel(
            name='SidebarSocial',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('visible', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Sidebar Social Media Item',
            },
        ),
        migrations.CreateModel(
            name='SidebarTwitter',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('visible', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Sidebar Twitter Item',
            },
        ),
        migrations.CreateModel(
            name='VisionPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, to='pages.Page', parent_link=True, primary_key=True, serialize=False)),
                ('content', mezzanine.core.fields.RichTextField(verbose_name='Content')),
                ('image', mezzanine.core.fields.FileField(max_length=300, default='', blank=True, validators=[website.jdpages.models.validate_vision_image])),
            ],
            options={
                'verbose_name': 'VisionPage',
                'ordering': ('_order',),
            },
            bases=('pages.page', models.Model),
        ),
        migrations.CreateModel(
            name='VisionsPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, to='pages.Page', parent_link=True, primary_key=True, serialize=False)),
                ('content', mezzanine.core.fields.RichTextField(verbose_name='Content')),
                ('vision_pages', models.ManyToManyField(to='jdpages.VisionPage')),
            ],
            options={
                'verbose_name': 'VisionsPage',
                'ordering': ('_order',),
            },
            bases=('pages.page', models.Model),
        ),
        migrations.RemoveField(
            model_name='columnelement',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='columnelement',
            name='site',
        ),
        migrations.RemoveField(
            model_name='columnelementwidget',
            name='column_element',
        ),
        migrations.RemoveField(
            model_name='columnelementwidget',
            name='page',
        ),
        migrations.RemoveField(
            model_name='columnelementwidget',
            name='site',
        ),
        migrations.RemoveField(
            model_name='eventcolumnelement',
            name='site',
        ),
        migrations.RemoveField(
            model_name='pageheaderimagewidget',
            name='page',
        ),
        migrations.RemoveField(
            model_name='pageheaderimagewidget',
            name='site',
        ),
        migrations.RemoveField(
            model_name='sidebar',
            name='site',
        ),
        migrations.DeleteModel(
            name='SidebarBannerWidget',
        ),
        migrations.RemoveField(
            model_name='sidebarblogcategorywidget',
            name='blog_category',
        ),
        migrations.RemoveField(
            model_name='sidebarblogcategorywidget',
            name='sidebar',
        ),
        migrations.RemoveField(
            model_name='sidebarblogcategorywidget',
            name='site',
        ),
        migrations.RemoveField(
            model_name='sidebartabswidget',
            name='sidebar',
        ),
        migrations.RemoveField(
            model_name='sidebartabswidget',
            name='site',
        ),
        migrations.RemoveField(
            model_name='sidebartwitterwidget',
            name='sidebar',
        ),
        migrations.RemoveField(
            model_name='sidebartwitterwidget',
            name='site',
        ),
        migrations.RemoveField(
            model_name='socialmediabutton',
            name='sidebar',
        ),
        migrations.RemoveField(
            model_name='socialmediabutton',
            name='site',
        ),
        migrations.AddField(
            model_name='homepage',
            name='header_subtitle',
            field=models.CharField(max_length=500, default='', blank=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='header_title',
            field=models.CharField(max_length=300, default='', blank=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='news_category',
            field=models.ForeignKey(to='blog.BlogCategory', null=True, blank=True),
        ),
        migrations.DeleteModel(
            name='ColumnElement',
        ),
        migrations.DeleteModel(
            name='ColumnElementWidget',
        ),
        migrations.DeleteModel(
            name='EventColumnElement',
        ),
        migrations.DeleteModel(
            name='PageHeaderImageWidget',
        ),
        migrations.DeleteModel(
            name='Sidebar',
        ),
        migrations.DeleteModel(
            name='SidebarBlogCategoryWidget',
        ),
        migrations.DeleteModel(
            name='SidebarTabsWidget',
        ),
        migrations.DeleteModel(
            name='SidebarTwitterWidget',
        ),
        migrations.DeleteModel(
            name='SocialMediaButton',
        ),
        migrations.AddField(
            model_name='sidebartwitter',
            name='page',
            field=models.ForeignKey(to='pages.Page', null=True),
        ),
        migrations.AddField(
            model_name='sidebartwitter',
            name='site',
            field=models.ForeignKey(editable=False, to='sites.Site'),
        ),
        migrations.AddField(
            model_name='sidebarsocial',
            name='page',
            field=models.ForeignKey(to='pages.Page', null=True),
        ),
        migrations.AddField(
            model_name='sidebarsocial',
            name='site',
            field=models.ForeignKey(editable=False, to='sites.Site'),
        ),
        migrations.AddField(
            model_name='sidebarrichtext',
            name='page',
            field=models.ForeignKey(to='pages.Page', null=True),
        ),
        migrations.AddField(
            model_name='sidebarrichtext',
            name='site',
            field=models.ForeignKey(editable=False, to='sites.Site'),
        ),
        migrations.AddField(
            model_name='sidebarlink',
            name='page',
            field=models.ForeignKey(to='pages.Page', null=True),
        ),
        migrations.AddField(
            model_name='sidebarlink',
            name='site',
            field=models.ForeignKey(editable=False, to='sites.Site'),
        ),
        migrations.AddField(
            model_name='sidebaragenda',
            name='page',
            field=models.ForeignKey(to='pages.Page', null=True),
        ),
        migrations.AddField(
            model_name='sidebaragenda',
            name='site',
            field=models.ForeignKey(editable=False, to='sites.Site'),
        ),
        migrations.AddField(
            model_name='pageheaderimage',
            name='page',
            field=models.ForeignKey(to='pages.Page', null=True),
        ),
        migrations.AddField(
            model_name='pageheaderimage',
            name='site',
            field=models.ForeignKey(editable=False, to='sites.Site'),
        ),
        migrations.AddField(
            model_name='footerlink',
            name='footer_links',
            field=models.ForeignKey(to='jdpages.FooterLinks', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='footerlink',
            name='site',
            field=models.ForeignKey(editable=False, to='sites.Site'),
        ),
        migrations.AddField(
            model_name='footer',
            name='info_right',
            field=models.OneToOneField(auto_created=True, to='jdpages.FooterInfo'),
        ),
        migrations.AddField(
            model_name='footer',
            name='links_left',
            field=models.OneToOneField(auto_created=True, to='jdpages.FooterLinks', related_name='links_left'),
        ),
        migrations.AddField(
            model_name='footer',
            name='links_middle',
            field=models.OneToOneField(auto_created=True, to='jdpages.FooterLinks', related_name='links_right'),
        ),
        migrations.AddField(
            model_name='footer',
            name='site',
            field=models.ForeignKey(editable=False, to='sites.Site'),
        ),
        migrations.AddField(
            model_name='actionbanner',
            name='page',
            field=models.ForeignKey(to='pages.Page', null=True),
        ),
        migrations.AddField(
            model_name='actionbanner',
            name='site',
            field=models.ForeignKey(editable=False, to='sites.Site'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='vision_pages',
            field=models.ManyToManyField(to='jdpages.VisionPage', blank=True),
        ),
    ]
