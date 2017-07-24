# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('jdpages', '0031_auto_20170724_1817'),
    ]

    operations = [
        migrations.CreateModel(
            name='Footer',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FooterInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', blank=True, max_length=100)),
                ('content', mezzanine.core.fields.RichTextField()),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FooterLink',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('_order', mezzanine.core.fields.OrderField(null=True, verbose_name='Order')),
                ('title', models.CharField(default='', blank=True, max_length=100)),
                ('url', models.CharField(default='', blank=True, max_length=500)),
            ],
            options={
                'ordering': ('_order',),
            },
        ),
        migrations.CreateModel(
            name='FooterLinks',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', blank=True, max_length=100)),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='footerlink',
            name='footer_links',
            field=models.ForeignKey(blank=True, to='jdpages.FooterLinks', null=True),
        ),
        migrations.AddField(
            model_name='footerlink',
            name='site',
            field=models.ForeignKey(editable=False, to='sites.Site'),
        ),
        migrations.AddField(
            model_name='footer',
            name='info_right',
            field=models.OneToOneField(auto_created=True, to='jdpages.FooterInfo'),
        ),
        migrations.AddField(
            model_name='footer',
            name='links_left',
            field=models.OneToOneField(auto_created=True, to='jdpages.FooterLinks', related_name='links_left'),
        ),
        migrations.AddField(
            model_name='footer',
            name='links_middle',
            field=models.OneToOneField(auto_created=True, to='jdpages.FooterLinks', related_name='links_right'),
        ),
        migrations.AddField(
            model_name='footer',
            name='site',
            field=models.ForeignKey(editable=False, to='sites.Site'),
        ),
    ]
