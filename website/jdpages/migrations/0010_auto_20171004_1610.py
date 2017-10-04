# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20150527_1555'),
        ('jdpages', '0009_organisationpartpage'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganisationPage',
            fields=[
                ('page_ptr', models.OneToOneField(primary_key=True, to='pages.Page', parent_link=True, serialize=False, auto_created=True)),
                ('content', mezzanine.core.fields.RichTextField(verbose_name='Content')),
            ],
            options={
                'ordering': ('_order',),
                'verbose_name': 'Organisatie pagina',
                'verbose_name_plural': 'Organisatie paginas',
            },
            bases=('pages.page', models.Model),
        ),
        migrations.AlterModelOptions(
            name='organisationpartpage',
            options={'ordering': ('_order',), 'verbose_name': 'Organisatie-onderdeel pagina', 'verbose_name_plural': 'Organisatie-onderdeel paginas'},
        ),
        migrations.AddField(
            model_name='organisationpage',
            name='organisation_part_pages',
            field=models.ManyToManyField(to='jdpages.OrganisationPartPage', blank=True),
        ),
    ]
