from django.db import models

# Create your models here.
# Reader: 学号，姓名，性别，身份，电话，邮箱，密码

class reader(models.Model):
    rsex_choices = (('男','男'),('女','女'))
    rid = models.CharField(db_column='rid', max_length=255, null=False, default='', primary_key=True)
    rname = models.CharField(db_column='rname', max_length=255, null=False, default='')
    rsex = models.CharField(db_column='rsex', max_length=255, choices=rsex_choices)
    rtype = models.CharField(db_column='rtype', max_length=255, null=True)
    rtel = models.CharField(db_column='rtel', max_length=255, null=True)
    remail = models.CharField(db_column='remail', max_length=255, null=True)
    rpsd = models.CharField(db_column='rpsd', max_length=255, null=True)

    class Meta:
        managed = True
        db_table = "reader"