# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '__first__'),
        ('jdpages', '0002_jdhomepage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('_order', models.IntegerField(verbose_name='Order', null=True)),
                ('document', mezzanine.core.fields.FileField(max_length=200, verbose_name='Document')),
                ('description', models.CharField(max_length=1000, verbose_name='Description')),
            ],
            options={
                'ordering': ('_order',),
                'verbose_name_plural': 'Documents',
                'verbose_name': 'Document',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DocumentListing',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, to='pages.Page', parent_link=True, serialize=False, primary_key=True)),
                ('content', mezzanine.core.fields.RichTextField(verbose_name='Content')),
                ('header_image', models.CharField(blank=True, max_length=1000, default='')),
            ],
            options={
                'ordering': ('_order',),
                'verbose_name_plural': 'Document Listings',
                'verbose_name': 'Document Listing',
            },
            bases=('pages.page', models.Model),
        ),
        migrations.AddField(
            model_name='document',
            name='document_listing',
            field=models.ForeignKey(to='jdpages.DocumentListing', related_name='documents'),
            preserve_default=True,
        ),
    ]
