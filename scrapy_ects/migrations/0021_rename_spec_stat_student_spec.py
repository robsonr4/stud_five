# Generated by Django 3.2.5 on 2021-12-04 19:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrapy_ects', '0020_auto_20211204_1846'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='spec_stat',
            new_name='spec',
        ),
    ]
