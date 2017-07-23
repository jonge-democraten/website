# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20150527_1555'),
        ('sites', '0001_initial'),
        ('jdpages', '0004_auto_20170722_1406'),
    ]

    operations = [
        migrations.CreateModel(
            name='SidebarAgenda',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('type', models.CharField(choices=[('SI', 'Site'), ('AL', 'All'), ('MA', 'Main site'), ('SM', 'Main and site')], max_length=2)),
                ('page', models.ForeignKey(to='pages.Page')),
                ('site', models.ForeignKey(to='sites.Site', editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SidebarLink',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('url', models.URLField(blank=True, default='')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SidebarLinks',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('page', models.ForeignKey(to='pages.Page')),
                ('site', models.ForeignKey(to='sites.Site', editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SidebarRichText',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('content', mezzanine.core.fields.RichTextField()),
                ('page', models.ForeignKey(to='pages.Page')),
                ('site', models.ForeignKey(to='sites.Site', editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SidebarSocial',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('page', models.ForeignKey(to='pages.Page')),
                ('site', models.ForeignKey(to='sites.Site', editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SidebarTwitter',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('page', models.ForeignKey(to='pages.Page')),
                ('site', models.ForeignKey(to='sites.Site', editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='sidebarlink',
            name='sidebar',
            field=models.ForeignKey(to='jdpages.SidebarLinks'),
        ),
        migrations.AddField(
            model_name='sidebarlink',
            name='site',
            field=models.ForeignKey(to='sites.Site', editable=False),
        ),
    ]
