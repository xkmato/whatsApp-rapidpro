# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_message_urn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='urn',
            field=models.CharField(max_length=40),
        ),
    ]
