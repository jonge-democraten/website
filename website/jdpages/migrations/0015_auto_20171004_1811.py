# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jdpages', '0014_auto_20171004_1802'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organisationpartmember',
            name='organisation_parts',
        ),
        migrations.AddField(
            model_name='organisationpartmember',
            name='organisation_part',
            field=models.ForeignKey(to='jdpages.OrganisationPartPage', blank=True, null=True),
        ),
    ]
