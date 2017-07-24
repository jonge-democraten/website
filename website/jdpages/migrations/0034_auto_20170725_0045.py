# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mezzanine.core.fields
import website.jdpages.models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20150527_1555'),
        ('sites', '0001_initial'),
        ('jdpages', '0033_auto_20170724_1903'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageHeaderImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=1000, default='')),
                ('image', mezzanine.core.fields.FileField(validators=[website.jdpages.models.validate_header_image], max_length=200)),
                ('page', models.ForeignKey(to='pages.Page', null=True)),
                ('site', models.ForeignKey(to='sites.Site', editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='pageheaderimagewidget',
            name='page',
        ),
        migrations.RemoveField(
            model_name='pageheaderimagewidget',
            name='site',
        ),
        migrations.DeleteModel(
            name='PageHeaderImageWidget',
        ),
    ]
