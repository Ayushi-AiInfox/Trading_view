# Generated by Django 5.1.4 on 2024-12-10 05:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.CharField(default=datetime.datetime(2024, 12, 10, 5, 54, 51, 410935), max_length=200),
        ),
        migrations.AlterField(
            model_name='user',
            name='updated_at',
            field=models.CharField(default=datetime.datetime(2024, 12, 10, 5, 54, 51, 410920), max_length=200),
        ),
    ]