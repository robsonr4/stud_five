# Generated by Django 3.2.5 on 2022-01-14 18:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrapy_ects', '0028_auto_20220114_1842'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='majorassignment',
            name='has_date',
        ),
        migrations.RemoveField(
            model_name='majorassignment',
            name='the_date',
        ),
        migrations.RemoveField(
            model_name='specassignment',
            name='has_date',
        ),
        migrations.RemoveField(
            model_name='specassignment',
            name='the_date',
        ),
    ]
