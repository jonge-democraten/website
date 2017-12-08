# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0006_auto_20170922_1652'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='socialmediaurls',
            options={'verbose_name_plural': 'Social media urls', 'verbose_name': 'Social media urls'},
        ),
        migrations.AlterModelOptions(
            name='visionpage',
            options={'verbose_name_plural': 'Standpunt paginas', 'verbose_name': 'Standpunt pagina', 'ordering': ('_order',)},
        ),
        migrations.AlterModelOptions(
            name='visionspage',
            options={'verbose_name_plural': 'Standpunten paginas', 'verbose_name': 'Standpunten pagina', 'ordering': ('_order',)},
        ),
        migrations.AlterField(
            model_name='homepage',
            name='vision_pages',
            field=models.ManyToManyField(to='jdpages.VisionPage', blank=True, verbose_name='Standpunt paginas'),
        ),
    ]
