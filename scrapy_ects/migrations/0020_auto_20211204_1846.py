# Generated by Django 3.2.5 on 2021-12-04 18:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrapy_ects', '0019_auto_20211204_0758'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Specialization',
            new_name='Spec',
        ),
        migrations.AlterModelOptions(
            name='spec',
            options={'verbose_name': 'Spec', 'verbose_name_plural': 'Specializations'},
        ),
    ]
