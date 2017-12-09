# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0014_organisationmember_email'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogcategorypage',
            options={'ordering': ('_order',), 'verbose_name': 'Blog categorie pagina', 'verbose_name_plural': "Blog categorie pagina's"},
        ),
        migrations.AlterModelOptions(
            name='homepage',
            options={'ordering': ('_order',), 'verbose_name': 'Home pagina', 'verbose_name_plural': "Home pagina's"},
        ),
        migrations.AlterModelOptions(
            name='organisationpage',
            options={'ordering': ('_order',), 'verbose_name': 'Organisatie pagina', 'verbose_name_plural': "Organisatie pagina's"},
        ),
        migrations.AlterModelOptions(
            name='organisationpartpage',
            options={'ordering': ('_order',), 'verbose_name': 'Organisatie-onderdeel pagina', 'verbose_name_plural': "Organisatie-onderdeel pagina's"},
        ),
        migrations.AlterModelOptions(
            name='visionpage',
            options={'ordering': ('_order',), 'verbose_name': 'Standpunt pagina', 'verbose_name_plural': "Standpunt pagina's"},
        ),
        migrations.AlterModelOptions(
            name='visionspage',
            options={'ordering': ('_order',), 'verbose_name': 'Standpunten pagina', 'verbose_name_plural': "Standpunten pagina's"},
        ),
        migrations.AlterModelOptions(
            name='wordlidpage',
            options={'ordering': ('_order',), 'verbose_name': 'Word lid pagina', 'verbose_name_plural': "Standpunt pagina's"},
        ),
    ]
