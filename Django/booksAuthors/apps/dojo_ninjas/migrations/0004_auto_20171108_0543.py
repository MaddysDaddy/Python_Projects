# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-08 05:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dojo_ninjas', '0003_auto_20171108_0541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='desc',
            field=models.TextField(default='', max_length=1000),
        ),
    ]