# Generated by Django 2.1.4 on 2020-04-09 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reader', '0002_auto_20200409_1027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reader',
            name='rname',
            field=models.CharField(db_column='rname', default='', max_length=255),
        ),
    ]
