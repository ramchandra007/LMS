# Generated by Django 4.2.4 on 2024-04-15 12:10

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0194_schools_plan_id_alter_leave_today_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave',
            name='today',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 15, 12, 10, 27, 372337)),
        ),
        migrations.AlterField(
            model_name='schools',
            name='plan_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='learning.pricingplan'),
        ),
        migrations.AlterField(
            model_name='teacher_shifts',
            name='half_daytime',
            field=models.TimeField(verbose_name=datetime.datetime(2024, 4, 15, 12, 10, 27, 354054)),
        ),
        migrations.AlterField(
            model_name='teacher_shifts',
            name='in_time',
            field=models.TimeField(verbose_name=datetime.datetime(2024, 4, 15, 12, 10, 27, 354054)),
        ),
        migrations.AlterField(
            model_name='teacher_shifts',
            name='late_mark_time',
            field=models.TimeField(verbose_name=datetime.datetime(2024, 4, 15, 12, 10, 27, 354054)),
        ),
        migrations.AlterField(
            model_name='teacher_shifts',
            name='out_time',
            field=models.TimeField(verbose_name=datetime.datetime(2024, 4, 15, 12, 10, 27, 354054)),
        ),
        migrations.AlterField(
            model_name='teachers',
            name='dob',
            field=models.DateField(default=datetime.datetime(2024, 4, 15, 12, 10, 27, 351747)),
        ),
    ]
