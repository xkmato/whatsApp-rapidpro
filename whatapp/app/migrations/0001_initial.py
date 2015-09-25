# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('direction', models.CharField(max_length=1, choices=[(b'Incoming', b'I'), (b'Outgoing', b'O')])),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default=b'Q', max_length=1, choices=[(b'Queued', b'Q'), (b'Sent', b'S')])),
                ('rapidpro_id', models.CharField(max_length=40, null=True, blank=True)),
            ],
        ),
    ]
