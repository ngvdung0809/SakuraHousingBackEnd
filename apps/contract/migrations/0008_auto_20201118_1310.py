# Generated by Django 3.1.1 on 2020-11-18 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0007_auto_20201115_1041'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hd2dichvus',
            name='don_gia',
        ),
        migrations.AlterField(
            model_name='hd2dichvus',
            name='dinh_muc',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]