# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('jdpages', '0011_organisationpartmember'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganisationMember',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=200)),
                ('role', models.CharField(default='', max_length=200)),
                ('content', mezzanine.core.fields.RichTextField()),
                ('image', mezzanine.core.fields.FileField(default='', max_length=300, blank=True)),
                ('organisation_parts', models.ManyToManyField(to='jdpages.OrganisationPartPage', blank=True)),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
            ],
            options={
                'verbose_name_plural': 'Organisatie lid',
                'verbose_name': 'Organisatie lid',
            },
        ),
        migrations.RemoveField(
            model_name='organisationpartmember',
            name='organisation_parts',
        ),
        migrations.RemoveField(
            model_name='organisationpartmember',
            name='site',
        ),
        migrations.DeleteModel(
            name='OrganisationPartMember',
        ),
    ]
