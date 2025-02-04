# Generated by Django 5.0.1 on 2024-03-19 11:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0168_alter_leave_today_alter_meeting_datetime_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Meeting',
        ),
        migrations.AlterField(
            model_name='leave',
            name='today',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 19, 11, 48, 9, 879174)),
        ),
        migrations.AlterField(
            model_name='teacher_shifts',
            name='half_daytime',
            field=models.TimeField(verbose_name=datetime.datetime(2024, 3, 19, 11, 48, 9, 859227)),
        ),
        migrations.AlterField(
            model_name='teacher_shifts',
            name='in_time',
            field=models.TimeField(verbose_name=datetime.datetime(2024, 3, 19, 11, 48, 9, 859227)),
        ),
        migrations.AlterField(
            model_name='teacher_shifts',
            name='late_mark_time',
            field=models.TimeField(verbose_name=datetime.datetime(2024, 3, 19, 11, 48, 9, 859227)),
        ),
        migrations.AlterField(
            model_name='teacher_shifts',
            name='out_time',
            field=models.TimeField(verbose_name=datetime.datetime(2024, 3, 19, 11, 48, 9, 859227)),
        ),
        migrations.AlterField(
            model_name='teachers',
            name='dob',
            field=models.DateField(default=datetime.datetime(2024, 3, 19, 11, 48, 9, 858230)),
        ),
    ]
