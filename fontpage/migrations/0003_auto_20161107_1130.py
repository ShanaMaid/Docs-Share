# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-07 11:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fontpage', '0002_auto_20161107_1100'),
    ]

    operations = [
        migrations.AddField(
            model_name='usergroup',
            name='sumperson',
            field=models.IntegerField(db_column='G_sumperson', default=0),
        ),
        migrations.AlterField(
            model_name='usertable',
            name='u_nickname',
            field=models.CharField(db_column='U_nickname', default='nick', max_length=12),
        ),
    ]