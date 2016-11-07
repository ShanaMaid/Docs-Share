# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-07 10:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('a_id', models.AutoField(db_column='A_Id', primary_key=True, serialize=False)),
                ('a_title', models.CharField(blank=True, db_column='A_title', max_length=20, null=True)),
                ('a_url', models.TextField(blank=True, db_column='A_URL', null=True)),
                ('a_type', models.CharField(blank=True, db_column='A_type', max_length=20, null=True)),
                ('a_time', models.DateField(blank=True, db_column='A_time', null=True)),
                ('a_reading_amount', models.BigIntegerField(blank=True, db_column='A_reading_amount', null=True)),
                ('a_issee', models.IntegerField(blank=True, db_column='A_isSee', null=True)),
            ],
            options={
                'db_table': 'Article',
            },
        ),
        migrations.CreateModel(
            name='Roletable',
            fields=[
                ('r_id', models.AutoField(db_column='R_Id', primary_key=True, serialize=False)),
                ('r_type', models.CharField(blank=True, db_column='R_type', max_length=10, null=True)),
            ],
            options={
                'db_table': 'RoleTable',
            },
        ),
        migrations.CreateModel(
            name='Usergroup',
            fields=[
                ('g_id', models.AutoField(db_column='G_Id', primary_key=True, serialize=False)),
                ('g_name', models.CharField(blank=True, db_column='G_Name', max_length=10, null=True)),
            ],
            options={
                'db_table': 'UserGroup',
            },
        ),
        migrations.CreateModel(
            name='Usertable',
            fields=[
                ('u_id', models.AutoField(db_column='U_Id', primary_key=True, serialize=False)),
                ('u_account', models.CharField(blank=True, db_column='U_account', max_length=16, null=True)),
                ('u_password', models.CharField(blank=True, db_column='U_password', max_length=16, null=True)),
                ('u_nickname', models.CharField(blank=True, db_column='U_nickname', max_length=12, null=True)),
                ('u_score', models.IntegerField(blank=True, db_column='U_score', null=True)),
                ('g', models.ForeignKey(blank=True, db_column='G_Id', null=True, on_delete=django.db.models.deletion.CASCADE, to='fontpage.Usergroup')),
                ('r', models.ForeignKey(blank=True, db_column='R_Id', null=True, on_delete=django.db.models.deletion.CASCADE, to='fontpage.Roletable')),
            ],
            options={
                'db_table': 'UserTable',
            },
        ),
        migrations.AddField(
            model_name='article',
            name='u',
            field=models.ForeignKey(blank=True, db_column='U_Id', null=True, on_delete=django.db.models.deletion.CASCADE, to='fontpage.Usertable'),
        ),
    ]
