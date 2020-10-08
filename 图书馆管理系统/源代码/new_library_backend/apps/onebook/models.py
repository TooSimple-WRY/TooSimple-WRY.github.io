from django.db import models

# Create your models here.
# Onebook: 编号，书号，书架，位置，借阅状态

class onebook(models.Model):
    bbid = models.CharField(db_column='bbid', max_length=15, null=False, default='', primary_key=True)
    bid = models.CharField(db_column='bid', max_length=30, null=False, default='')
    sheft = models.CharField(db_column='sheft', max_length=60, null=True)
    place = models.CharField(db_column='place', max_length=60, null=True)
    statu = models.CharField(db_column='statu', max_length=20, null=True)

    class Meta:
        managed = True
        db_table = "onebook"