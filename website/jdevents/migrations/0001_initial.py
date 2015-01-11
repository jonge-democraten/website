# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('keywords_string', models.CharField(blank=True, max_length=500, editable=False)),
                ('title', models.CharField(verbose_name='Title', max_length=500)),
                ('slug', models.CharField(verbose_name='URL', help_text='Leave blank to have the URL auto-generated from the title.', blank=True, max_length=2000, null=True)),
                ('_meta_title', models.CharField(verbose_name='Title', help_text='Optional title to be used in the HTML title tag. If left blank, the main title field will be used.', blank=True, max_length=500, null=True)),
                ('description', models.TextField(verbose_name='Description', blank=True)),
                ('gen_description', models.BooleanField(verbose_name='Generate description', help_text='If checked, the description will be automatically generated from content. Uncheck if you want to manually set a custom description.', default=True)),
                ('created', models.DateTimeField(editable=False, null=True)),
                ('updated', models.DateTimeField(editable=False, null=True)),
                ('status', models.IntegerField(verbose_name='Status', help_text='With Draft chosen, will only be shown for admin users on the site.', choices=[(1, 'Draft'), (2, 'Published')], default=2)),
                ('publish_date', models.DateTimeField(verbose_name='Published from', help_text="With Published chosen, won't be shown until this time", blank=True, null=True)),
                ('expiry_date', models.DateTimeField(verbose_name='Expires on', help_text="With Published chosen, won't be shown after this time", blank=True, null=True)),
                ('short_url', models.URLField(blank=True, null=True)),
                ('in_sitemap', models.BooleanField(verbose_name='Show in sitemap', default=True)),
                ('content', mezzanine.core.fields.RichTextField(verbose_name='Content')),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Occurence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('extra_information', models.CharField(blank=True, max_length=255, null=True)),
                ('event', models.ForeignKey(to='events.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
