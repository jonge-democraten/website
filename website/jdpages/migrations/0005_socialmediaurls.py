# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('jdpages', '0004_auto_20170726_0019'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialMediaUrls',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('facebook_url', models.URLField(max_length=300, default='', blank=True)),
                ('twitter_url', models.URLField(max_length=300, default='', blank=True)),
                ('youtube_url', models.URLField(max_length=300, default='', blank=True)),
                ('linkedin_url', models.URLField(max_length=300, default='', blank=True)),
                ('instagram_url', models.URLField(max_length=300, default='', blank=True)),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
