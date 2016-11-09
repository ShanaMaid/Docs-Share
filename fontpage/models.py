from __future__ import unicode_literals

from django.db import models


class Roletable(models.Model):
    r_id = models.AutoField(db_column='R_Id', primary_key=True)  
    r_type = models.CharField(db_column='R_type', max_length=10, blank=True, null=True)  

    class Meta:
        db_table = 'RoleTable'


class Usergroup(models.Model):
    g_id = models.AutoField(db_column='G_Id', primary_key=True)  # Field name made lowercase.
    g_name = models.CharField(db_column='G_Name', max_length=10, blank=True, null=True)  # Field name made lowercase.
    sumperson=models.IntegerField(db_column='G_sumperson', blank=True, null=True,default=0)
    class Meta:
        db_table = 'UserGroup'


class Usertable(models.Model):
    u_id = models.AutoField(db_column='U_Id', primary_key=True)  # Field name made lowercase.
    g = models.ForeignKey(Usergroup, db_column='G_Id', blank=True, null=True)  # Field name made lowercase.
    r = models.ForeignKey(Roletable, db_column='R_Id', blank=True, null=True)  # Field name made lowercase.
    u_account = models.CharField(db_column='U_account', max_length=16, blank=True, null=True)  # Field name made lowercase.
    u_password = models.CharField(db_column='U_password', max_length=16, blank=True, null=True)  # Field name made lowercase.
    u_nickname = models.CharField(db_column='U_nickname', max_length=12, blank=True, null=True,default="nick")  # Field name made lowercase.
    u_score = models.IntegerField(db_column='U_score', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'UserTable'

class Article(models.Model):
    a_id = models.AutoField(db_column='A_Id', primary_key=True)  # Field name made lowercase.
    u = models.ForeignKey(Usertable, db_column='U_Id', blank=True, null=True)  # Field name made lowercase.
    a_title = models.CharField(db_column='A_title', max_length=20, blank=True, null=True)  # Field name made lowercase.
    a_url = models.TextField(db_column='A_URL', blank=True, null=True)  # Field name made lowercase.
    a_type = models.CharField(db_column='A_type', max_length=20, blank=True, null=True)  # Field name made lowercase.
    a_time = models.DateField(db_column='A_time', blank=True, null=True)  # Field name made lowercase.
    a_reading_amount = models.BigIntegerField(db_column='A_reading_amount', blank=True, null=True)  # Field name made lowercase.
    a_issee = models.IntegerField(db_column='A_isSee', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Article'
     
         