# Generated by Django 3.1.1 on 2020-11-18 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicetransactions',
            name='ngay_thanh_toan_tt',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='servicetransactions',
            name='so_tien',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]