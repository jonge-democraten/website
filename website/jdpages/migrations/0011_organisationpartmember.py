# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('jdpages', '0010_auto_20171004_1610'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganisationPartMember',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=200)),
                ('role', models.CharField(default='', max_length=200)),
                ('content', mezzanine.core.fields.RichTextField()),
                ('image', mezzanine.core.fields.FileField(max_length=300, blank=True, default='')),
                ('organisation_parts', models.ManyToManyField(to='jdpages.OrganisationPartPage', blank=True)),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
            ],
            options={
                'verbose_name': 'Organisatie-onderdeel lid',
                'verbose_name_plural': 'Organisatie-onderdeel lid',
            },
        ),
    ]
