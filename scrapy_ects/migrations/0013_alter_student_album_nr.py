# Generated by Django 3.2.5 on 2021-12-02 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapy_ects', '0012_alter_student_current_sem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='album_nr',
            field=models.IntegerField(null=True),
        ),
    ]
