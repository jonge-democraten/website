# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('blog', '__first__'),
        ('jdpages', '0006_removejdpage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sidebar',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('active', models.BooleanField(default=True)),
                ('site', models.ForeignKey(to='sites.Site', editable=False)),
            ],
            options={
                'verbose_name_plural': 'Sidebar',
                'verbose_name': 'Sidebar',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SidebarBannerWidget',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=200, default='')),
                ('active', models.BooleanField(default=True)),
                ('image', mezzanine.core.fields.FileField(max_length=200)),
                ('url', models.URLField(help_text='http://www.example.com')),
                ('description', models.CharField(max_length=200, default='', blank=True, help_text='This is shown as tooltip and alt text.')),
            ],
            options={
                'verbose_name': 'Global sidebar banner',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SidebarBlogCategoryWidget',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
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
            name='SidebarTwitterWidget',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
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
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('_order', models.IntegerField(null=True, verbose_name='Order')),
                ('type', models.CharField(max_length=2, choices=[('FB', 'Facebook'), ('LI', 'LinkedIn'), ('TW', 'Twitter'), ('YT', 'YouTube')])),
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
        migrations.AlterModelOptions(
            name='columnelementwidget',
            options={'verbose_name': 'Column widget', 'ordering': ('_order',)},
        ),
    ]
