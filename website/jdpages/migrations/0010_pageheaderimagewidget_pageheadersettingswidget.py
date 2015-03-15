# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('pages', '__first__'),
        ('jdpages', '0009_documentlisting_blank_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageHeaderImageWidget',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=1000, blank=True)),
                ('image', mezzanine.core.fields.FileField(max_length=200)),
                ('page', models.ForeignKey(null=True, to='pages.Page')),
                ('site', models.ForeignKey(to='sites.Site', editable=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PageHeaderSettingsWidget',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('type', models.CharField(choices=[('PA', 'Parent header'), ('NO', 'No header'), ('FB', 'Single image'), ('RA', 'Random image')], default='PA', max_length=2)),
                ('page', models.OneToOneField(null=True, to='pages.Page')),
                ('site', models.ForeignKey(to='sites.Site', editable=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
