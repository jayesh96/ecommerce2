# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20160829_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='id',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
    ]
