# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import website.jdpages.models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20150527_1555'),
        ('jdpages', '0008_sidebarrichtext_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganisationPartPage',
            fields=[
                ('page_ptr', models.OneToOneField(primary_key=True, parent_link=True, auto_created=True, to='pages.Page', serialize=False)),
                ('content', mezzanine.core.fields.RichTextField(verbose_name='Content')),
                ('image', mezzanine.core.fields.FileField(max_length=300, blank=True, validators=[website.jdpages.models.validate_organisation_image], default='')),
            ],
            options={
                'verbose_name': 'Organisatie Onderdeel pagina',
                'ordering': ('_order',),
                'verbose_name_plural': 'Organisatie Onderdeel paginas',
            },
            bases=('pages.page', models.Model),
        ),
    ]
