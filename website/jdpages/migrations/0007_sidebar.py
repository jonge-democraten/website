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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=200)),
                ('active', models.BooleanField(default=True)),
                ('site', models.ForeignKey(to='sites.Site', editable=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SidebarBanner',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=1000, default='')),
                ('image', mezzanine.core.fields.FileField(max_length=200)),
                ('url', models.URLField(max_length=1000, help_text='http://www.example.com')),
                ('description', models.CharField(blank=True, max_length=1000, help_text='This is shown as tooltip and alt text.', default='')),
                ('site', models.ForeignKey(to='sites.Site', editable=False)),
            ],
            options={
                'verbose_name': 'Sidebar Banner',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SidebarElement',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('object_id', models.PositiveIntegerField(verbose_name='related object id', null=True)),
                ('content_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True)),
                ('site', models.ForeignKey(to='sites.Site', editable=False)),
            ],
            options={
                'verbose_name': 'Sidebar element',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SidebarElementWidget',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('_order', models.IntegerField(verbose_name='Order', null=True)),
                ('title', models.CharField(max_length=1000, default='')),
                ('max_items', models.PositiveIntegerField(default=3)),
                ('sidebar', models.ForeignKey(to='jdpages.Sidebar')),
                ('sidebar_element', models.ForeignKey(null=True, to='jdpages.SidebarElement')),
                ('site', models.ForeignKey(to='sites.Site', editable=False)),
            ],
            options={
                'verbose_name': 'Sidebar widget',
                'ordering': ('_order',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SidebarTwitter',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=1000, default='')),
                ('site', models.ForeignKey(to='sites.Site', editable=False)),
            ],
            options={
                'verbose_name': 'Sidebar Twitter',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SocialMediaButton',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('type', models.CharField(max_length=2, choices=[('FB', 'Facebook'), ('LI', 'LinkedIn'), ('TW', 'Twitter'), ('YT', 'YouTube')])),
                ('url', models.URLField(max_length=1000, help_text='http://www.example.com')),
                ('site', models.ForeignKey(to='sites.Site', editable=False)),
            ],
            options={
                'verbose_name': 'Sidebar Media Button',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SocialMediaButtonGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=200, help_text='The name is only used in the admin.')),
                ('site', models.ForeignKey(to='sites.Site', editable=False)),
            ],
            options={
                'verbose_name': 'Social Media Button Group',
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
            options={'verbose_name': 'Column widget', 'ordering': ('_order',)},
        ),
    ]
