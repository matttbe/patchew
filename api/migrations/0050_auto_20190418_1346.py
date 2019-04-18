# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-18 13:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.encoder
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0049_populate_message_flags'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='properties',
            field=jsonfield.fields.JSONField(default={}, dump_kwargs={'cls': jsonfield.encoder.JSONEncoder, 'separators': (',', ':')}, load_kwargs={}),
        ),
        migrations.AddField(
            model_name='project',
            name='properties',
            field=jsonfield.fields.JSONField(default={}, dump_kwargs={'cls': jsonfield.encoder.JSONEncoder, 'separators': (',', ':')}, load_kwargs={}),
        ),
        migrations.AlterField(
            model_name='messageproperty',
            name='message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Message'),
        ),
    ]
