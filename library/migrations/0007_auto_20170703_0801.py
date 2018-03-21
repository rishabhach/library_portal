# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-03 02:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0006_book_book_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='student',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='library.Student'),
        ),
    ]
