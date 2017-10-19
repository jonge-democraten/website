# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0009_organisation_page_and_members'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogcategorypage',
            options={'verbose_name': 'Blog categorie pagina', 'verbose_name_plural': 'Blog categorie paginas', 'ordering': ('_order',)},
        ),
        migrations.AlterModelOptions(
            name='homepage',
            options={'verbose_name': 'Home pagina', 'verbose_name_plural': 'Home paginas', 'ordering': ('_order',)},
        ),
    ]
