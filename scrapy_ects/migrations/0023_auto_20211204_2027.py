# Generated by Django 3.2.5 on 2021-12-04 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapy_ects', '0022_auto_20211204_1923'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='spec',
            options={'verbose_name': 'Spec', 'verbose_name_plural': 'Specs'},
        ),
        migrations.RenameField(
            model_name='majorassignment',
            old_name='major',
            new_name='major_course_stat',
        ),
        migrations.RenameField(
            model_name='majortest',
            old_name='major',
            new_name='major_course_stat',
        ),
        migrations.RenameField(
            model_name='specassignment',
            old_name='spec',
            new_name='spec_course_stat',
        ),
        migrations.RenameField(
            model_name='spectest',
            old_name='spec',
            new_name='spec_course_stat',
        ),
        migrations.AddField(
            model_name='majorassignment',
            name='more_info',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='majortest',
            name='more_info',
            field=models.TextField(default='e'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='specassignment',
            name='more_info',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='spectest',
            name='more_info',
            field=models.TextField(default='e'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='majorassignment',
            name='max_points',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='majorassignment',
            name='points',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='specassignment',
            name='max_points',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='specassignment',
            name='points',
            field=models.FloatField(blank=True),
        ),
        migrations.AddConstraint(
            model_name='speccourse',
            constraint=models.UniqueConstraint(fields=('name', 'spec'), name='unique_spec_course'),
        ),
    ]
