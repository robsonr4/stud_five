# Generated by Django 3.2.5 on 2021-12-02 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapy_ects', '0014_major_unique_major'),
    ]

    operations = [
        migrations.AlterField(
            model_name='major',
            name='duration_in_sem',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]