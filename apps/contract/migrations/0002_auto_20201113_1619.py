# Generated by Django 3.1.1 on 2020-11-13 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dichvus',
            name='code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='dichvus',
            name='don_vi',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]