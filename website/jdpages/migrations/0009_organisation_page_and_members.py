# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mezzanine.core.fields
import website.jdpages.models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('pages', '0003_auto_20150527_1555'),
        ('jdpages', '0008_sidebarrichtext_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganisationMember',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(default='', max_length=200)),
                ('content', mezzanine.core.fields.RichTextField()),
                ('image', mezzanine.core.fields.FileField(default='', blank=True, max_length=300)),
                ('facebook_url', models.URLField(default='', blank=True)),
                ('twitter_url', models.URLField(default='', blank=True)),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
            ],
            options={
                'verbose_name': 'Organisatie lid',
                'verbose_name_plural': 'Organisatie leden',
            },
        ),
        migrations.CreateModel(
            name='OrganisationPage',
            fields=[
                ('page_ptr', models.OneToOneField(primary_key=True, parent_link=True, to='pages.Page', auto_created=True, serialize=False)),
                ('content', mezzanine.core.fields.RichTextField(verbose_name='Content')),
            ],
            options={
                'verbose_name': 'Organisatie pagina',
                'ordering': ('_order',),
                'verbose_name_plural': 'Organisatie paginas',
            },
            bases=('pages.page', models.Model),
        ),
        migrations.CreateModel(
            name='OrganisationPartMember',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('role', models.CharField(default='', max_length=200)),
                ('member', models.ForeignKey(to='jdpages.OrganisationMember')),
            ],
            options={
                'verbose_name': 'Organisatie functie',
                'verbose_name_plural': 'Organisatie functies',
            },
        ),
        migrations.CreateModel(
            name='OrganisationPartPage',
            fields=[
                ('page_ptr', models.OneToOneField(primary_key=True, parent_link=True, to='pages.Page', auto_created=True, serialize=False)),
                ('content', mezzanine.core.fields.RichTextField(verbose_name='Content')),
                ('image', mezzanine.core.fields.FileField(default='', blank=True, validators=[website.jdpages.models.validate_organisation_image], max_length=300)),
            ],
            options={
                'verbose_name': 'Organisatie-onderdeel pagina',
                'ordering': ('_order',),
                'verbose_name_plural': 'Organisatie-onderdeel paginas',
            },
            bases=('pages.page', models.Model),
        ),
        migrations.AddField(
            model_name='organisationpartmember',
            name='organisation_part',
            field=models.ForeignKey(null=True, to='jdpages.OrganisationPartPage', blank=True),
        ),
        migrations.AddField(
            model_name='organisationpartmember',
            name='site',
            field=models.ForeignKey(editable=False, to='sites.Site'),
        ),
        migrations.AddField(
            model_name='organisationpage',
            name='organisation_part_pages',
            field=models.ManyToManyField(blank=True, to='jdpages.OrganisationPartPage'),
        ),
    ]
