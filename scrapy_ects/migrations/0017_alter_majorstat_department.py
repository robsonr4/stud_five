# Generated by Django 3.2.5 on 2021-12-02 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapy_ects', '0016_alter_majorstat_current_ects'),
    ]

    operations = [
        migrations.AlterField(
            model_name='majorstat',
            name='department',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
