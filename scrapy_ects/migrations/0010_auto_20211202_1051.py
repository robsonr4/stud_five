# Generated by Django 3.2.5 on 2021-12-02 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapy_ects', '0009_auto_20211202_1046'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='major',
            name='department',
        ),
        migrations.AddField(
            model_name='majorstat',
            name='department',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]