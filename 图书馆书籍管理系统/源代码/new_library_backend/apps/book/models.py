from django.db import models

# Create your models here.
# Book: 书号，书名，作者，出版公司，出版日期，图片，分类，简介

class book(models.Model):
    bid = models.CharField(db_column='bid', max_length=15, null=False, default='', primary_key=True)
    bname = models.CharField(db_column='bname', max_length=30, null=True)
    bauthor = models.CharField(db_column='bauthor', max_length=30, null=True)
    bcompany = models.CharField(db_column='bcompany', max_length=30, null=True)
    btime = models.CharField(db_column='btime', max_length=12, null=True)
    bimage = models.CharField(db_column='bimage', max_length=255, null=True)
    bsort = models.CharField(db_column='bsort', max_length=15, null=True)
    bcontent = models.CharField(db_column='bcontent', max_length=600, null=True)

    class Meta:
        managed = True
        db_table = "book"