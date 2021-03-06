# Generated by Django 3.2.5 on 2022-01-14 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapy_ects', '0029_auto_20220114_1845'),
    ]

    operations = [
        migrations.AddField(
            model_name='majorassignment',
            name='has_date',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='majorassignment',
            name='the_date',
            field=models.DateTimeField(blank=True, default=None),
        ),
        migrations.AddField(
            model_name='specassignment',
            name='has_date',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='specassignment',
            name='the_date',
            field=models.DateTimeField(blank=True, default=None),
        ),
    ]
