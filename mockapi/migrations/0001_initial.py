# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-24 22:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MockAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=400)),
                ('req_body', models.TextField(default='')),
                ('req_method', models.CharField(default='GET', max_length=20)),
                ('ans_body', models.TextField(default='')),
                ('ans_status', models.IntegerField(default=200)),
                ('query_params', models.TextField(default='')),
                ('use_up', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]