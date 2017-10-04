# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('jdpages', '0013_auto_20171004_1754'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganisationPartMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(default='', max_length=200)),
            ],
            options={
                'verbose_name': 'Organisatie functie',
                'verbose_name_plural': 'Organisatie functie',
            },
        ),
        migrations.RemoveField(
            model_name='organisationmember',
            name='organisation_parts',
        ),
        migrations.RemoveField(
            model_name='organisationmember',
            name='role',
        ),
        migrations.AddField(
            model_name='organisationpartmember',
            name='member',
            field=models.ForeignKey(to='jdpages.OrganisationMember'),
        ),
        migrations.AddField(
            model_name='organisationpartmember',
            name='organisation_parts',
            field=models.ManyToManyField(blank=True, to='jdpages.OrganisationPartPage'),
        ),
        migrations.AddField(
            model_name='organisationpartmember',
            name='site',
            field=models.ForeignKey(editable=False, to='sites.Site'),
        ),
    ]
