# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('jdpages', '0007_sidebarelements'),
    ]

    operations = [
        migrations.CreateModel(
            name='SidebarTwitter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=1000)),
                ('site', models.ForeignKey(to='sites.Site', editable=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='sidebarbanner',
            name='description',
            field=models.CharField(default='', help_text='This is shown as tooltip and alt text.', blank=True, max_length=1000),
            preserve_default=True,
        ),
    ]
