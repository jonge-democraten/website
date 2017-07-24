# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('jdpages', '0012_auto_20170724_1044'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActionBanner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(default='', max_length=500, blank=True)),
                ('content', mezzanine.core.fields.RichTextField()),
                ('image', mezzanine.core.fields.FileField(max_length=300)),
                ('site', models.ForeignKey(to='sites.Site', editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='homepage',
            name='action_banner',
            field=models.OneToOneField(to='jdpages.ActionBanner', blank=True, null=True),
        ),
    ]
