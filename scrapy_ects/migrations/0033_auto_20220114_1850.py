# Generated by Django 3.2.5 on 2022-01-14 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapy_ects', '0032_auto_20220114_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='majorassignment',
            name='the_date',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='specassignment',
            name='the_date',
            field=models.DateTimeField(blank=True),
        ),
    ]
