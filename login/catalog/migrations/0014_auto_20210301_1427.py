# Generated by Django 3.1.1 on 2021-03-01 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0013_auto_20210301_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='class_id',
            field=models.IntegerField(primary_key=True, serialize=False, unique=True),
        ),
    ]
