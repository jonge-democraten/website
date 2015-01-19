# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


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
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('site', models.ForeignKey(to='sites.Site', editable=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SidebarElement',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('object_id', models.PositiveIntegerField(verbose_name='related object id', null=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', null=True, blank=True)),
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
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('_order', models.IntegerField(verbose_name='Order', null=True)),
                ('title', models.CharField(default='', max_length=1000)),
                ('max_items', models.PositiveIntegerField(default=3)),
                ('sidebar', models.ForeignKey(to='jdpages.Sidebar')),
                ('sidebar_element', models.ForeignKey(to='jdpages.SidebarElement', null=True)),
                ('site', models.ForeignKey(to='sites.Site', editable=False)),
            ],
            options={
                'verbose_name': 'Sidebar element widget',
                'ordering': ('_order',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SocialMediaButton',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('type', models.CharField(max_length=2, choices=[('FB', 'Facebook'), ('LI', 'LinkedIn'), ('TW', 'Twitter'), ('YT', 'YouTube')])),
                ('url', models.URLField(max_length=1000, help_text='http://www.example.com')),
                ('site', models.ForeignKey(to='sites.Site', editable=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SocialMediaButtonGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=200, help_text='The name is only used in the admin.')),
                ('site', models.ForeignKey(to='sites.Site', editable=False)),
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
    ]
