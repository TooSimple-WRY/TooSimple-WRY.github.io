from django.db import models


# Create your models here.
# Admin: 工号，密码，姓名

class administrator(models.Model):
    aid = models.CharField(db_column='aid', max_length=10, null=False, default='', primary_key=True)
    apsd = models.CharField(db_column='apsd', max_length=6, null=True)
    aname = models.CharField(db_column='aname', max_length=6, null=False, default='')

    class Meta:
        managed = True
        db_table = "admin"
