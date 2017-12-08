# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0012_thatswhyitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='vision_pages',
            field=models.ManyToManyField(verbose_name="Standpunt pagina's", to='jdpages.VisionPage', blank=True),
        ),
        migrations.AlterField(
            model_name='organisationpage',
            name='organisation_part_pages',
            field=models.ManyToManyField(verbose_name='Organisatie onderdelen', to='jdpages.OrganisationPartPage', blank=True),
        ),
        migrations.AlterField(
            model_name='visionspage',
            name='vision_pages',
            field=models.ManyToManyField(verbose_name="Standpunt pagina's", to='jdpages.VisionPage', blank=True),
        ),
    ]
