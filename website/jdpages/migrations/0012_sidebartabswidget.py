# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('jdpages', '0011_headerimagevalidator'),
    ]

    operations = [
        migrations.CreateModel(
            name='SidebarTabsWidget',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('active', models.BooleanField(default=True)),
                ('sidebar', models.OneToOneField(to='jdpages.Sidebar')),
                ('site', models.ForeignKey(to='sites.Site', editable=False)),
            ],
            options={
                'verbose_name': 'Sidebar tabs widget',
            },
            bases=(models.Model,),
        ),
    ]
