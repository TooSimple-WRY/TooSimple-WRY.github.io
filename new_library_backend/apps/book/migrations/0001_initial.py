# Generated by Django 2.1.4 on 2020-03-07 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='book',
            fields=[
                ('bid', models.CharField(db_column='bid', default='', max_length=15, primary_key=True, serialize=False)),
                ('bname', models.CharField(db_column='bname', max_length=30, null=True)),
                ('bauthor', models.CharField(db_column='bauthor', max_length=30, null=True)),
                ('bcompany', models.CharField(db_column='bcompany', max_length=30, null=True)),
                ('btime', models.CharField(db_column='btime', max_length=12, null=True)),
                ('bimage', models.CharField(db_column='bimage', max_length=255, null=True)),
                ('bsort', models.CharField(db_column='bsort', max_length=15, null=True)),
                ('bcontent', models.CharField(db_column='bcontent', max_length=600, null=True)),
            ],
            options={
                'db_table': 'book',
                'managed': True,
            },
        ),
    ]
