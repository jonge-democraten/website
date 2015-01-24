# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('sites', '0001_initial'),
        ('jdpages', '0006_removejdpage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sidebar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('active', models.BooleanField(default=True)),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SidebarBanner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=1000, default='')),
                ('image', mezzanine.core.fields.FileField(max_length=200)),
                ('url', models.URLField(max_length=1000, help_text='http://www.example.com')),
                ('description', models.CharField(max_length=1000, default='', help_text='This is shown as tooltip and alt text. ', blank=True)),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SidebarElement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('object_id', models.PositiveIntegerField(null=True, verbose_name='related object id')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', null=True, blank=True)),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
            ],
            options={
                'verbose_name': 'Sidebar element',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SidebarElementWidget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('_order', models.IntegerField(null=True, verbose_name='Order')),
                ('title', models.CharField(max_length=1000, default='')),
                ('max_items', models.PositiveIntegerField(default=3)),
                ('sidebar', models.ForeignKey(to='jdpages.Sidebar')),
                ('sidebar_element', models.ForeignKey(null=True, to='jdpages.SidebarElement')),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
            ],
            options={
                'ordering': ('_order',),
                'verbose_name': 'Sidebar widget',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SocialMediaButton',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('type', models.CharField(choices=[('FB', 'Facebook'), ('LI', 'LinkedIn'), ('TW', 'Twitter'), ('YT', 'YouTube')], max_length=2)),
                ('url', models.URLField(max_length=1000, help_text='http://www.example.com')),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SocialMediaButtonGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=200, help_text='The name is only used in the admin.')),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='socialmediabutton',
            name='social_media_group',
            field=models.ForeignKey(to='jdpages.SocialMediaButtonGroup'),
            preserve_default=True,
        ),
        migrations.AlterModelOptions(
            name='columnelementwidget',
            options={'ordering': ('_order',), 'verbose_name': 'Column widget'},
        ),
    ]
