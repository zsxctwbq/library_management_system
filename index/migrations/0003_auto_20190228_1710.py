# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-02-28 09:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0002_publisher'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, unique=True, verbose_name='姓名')),
            ],
            options={
                'verbose_name_plural': '作者',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, unique=True, verbose_name='书名')),
            ],
            options={
                'verbose_name_plural': '图书',
            },
        ),
        migrations.AddField(
            model_name='publisher',
            name='addr',
            field=models.CharField(max_length=128, null=True, verbose_name='地址'),
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='index.Publisher', verbose_name='出版社'),
        ),
        migrations.AddField(
            model_name='author',
            name='book',
            field=models.ManyToManyField(to='index.Book'),
        ),
    ]
