from django.db import models

# Create your models here.
# Bookborrow: 借阅号，读者号，库存编号，借出日期，归还日期

class bookborrow(models.Model):
    brid = models.CharField(db_column='brid', max_length=15, null=False, default='', primary_key=True)
    rid = models.CharField(db_column='rid', max_length=30, null=False, default='')
    bbid = models.CharField(db_column='bbid', max_length=30, null=False, default='')
    brrowdate = models.CharField(db_column='brrowdate', max_length=30, null=True)
    returndate = models.CharField(db_column='returndate', max_length=12, null=True)

    class Meta:
        managed = True
        db_table = "bookborrow"