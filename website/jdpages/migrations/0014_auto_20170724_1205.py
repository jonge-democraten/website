# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20150527_1555'),
        ('jdpages', '0013_auto_20170724_1202'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homepage',
            name='action_banner',
        ),
        migrations.AddField(
            model_name='actionbanner',
            name='page',
            field=models.ForeignKey(to='pages.Page', null=True),
        ),
        migrations.AddField(
            model_name='actionbanner',
            name='visible',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='sidebaragenda',
            name='page',
            field=models.ForeignKey(to='pages.Page', null=True),
        ),
        migrations.AlterField(
            model_name='sidebarlink',
            name='page',
            field=models.ForeignKey(to='pages.Page', null=True),
        ),
        migrations.AlterField(
            model_name='sidebarrichtext',
            name='page',
            field=models.ForeignKey(to='pages.Page', null=True),
        ),
        migrations.AlterField(
            model_name='sidebarsocial',
            name='page',
            field=models.ForeignKey(to='pages.Page', null=True),
        ),
        migrations.AlterField(
            model_name='sidebartwitter',
            name='page',
            field=models.ForeignKey(to='pages.Page', null=True),
        ),
    ]
