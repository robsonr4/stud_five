# Generated by Django 3.2.5 on 2021-12-01 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapy_ects', '0002_auto_20211129_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='spec_course',
            field=models.ManyToManyField(blank=True, through='scrapy_ects.SpecCourseStat', to='scrapy_ects.SpecCourse'),
        ),
    ]
