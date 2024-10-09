# Generated by Django 5.0.1 on 2024-02-06 18:25

import ckeditor.fields
import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0090_timetablecards_timetablecarl_timetablecont_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendancemenu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('urls', models.CharField(max_length=700)),
                ('icon', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='leavemanagement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('Description', ckeditor.fields.RichTextField()),
            ],
        ),
        migrations.CreateModel(
            name='leavestype',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leavetype', models.CharField(max_length=500)),
                ('Noofleaves', models.CharField(max_length=500)),
                ('leavecategory', models.CharField(max_length=500)),
            ],
        ),
        migrations.AlterField(
            model_name='teachers',
            name='dob',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 6, 18, 25, 0, 778742)),
        ),
        migrations.CreateModel(
            name='leave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Reason', ckeditor.fields.RichTextField()),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('today', models.DateTimeField(default=datetime.datetime(2024, 2, 6, 18, 25, 0, 798970))),
                ('is_status', models.CharField(default='0', max_length=100)),
                ('user_type', models.CharField(default='0', max_length=100)),
                ('days_difference', models.IntegerField(blank=True, null=True)),
                ('read', models.BooleanField(default=False)),
                ('read1', models.BooleanField(default=False)),
                ('admin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('Leave_Type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='learning.leavestype')),
            ],
        ),
        migrations.CreateModel(
            name='teachermenu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=255)),
                ('icon', models.CharField(max_length=100)),
                ('parent_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='learning.teachermenu')),
            ],
        ),
    ]
