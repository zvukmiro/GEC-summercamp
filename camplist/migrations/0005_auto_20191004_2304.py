# Generated by Django 2.1.5 on 2019-10-04 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camplist', '0004_auto_20190823_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campprice',
            name='price_in_dollars',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='child',
            name='grade_in_fall',
            field=models.CharField(max_length=1),
        ),
    ]
