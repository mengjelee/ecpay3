# Generated by Django 2.0.6 on 2021-02-27 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0011_auto_20210227_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='trade_time',
            field=models.CharField(default='no record', max_length=100),
        ),
    ]
