# Generated by Django 5.0.1 on 2024-01-05 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0007_menuitem_icon_menuitem_parent_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='dashboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('des1', models.CharField(max_length=100)),
                ('des2', models.CharField(max_length=100)),
            ],
        ),
    ]
