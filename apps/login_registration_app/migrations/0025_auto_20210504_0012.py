# Generated by Django 2.2.4 on 2021-05-04 04:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_registration_app', '0024_auto_20210504_0010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birthday',
            field=models.DateField(default=datetime.datetime(2021, 5, 4, 0, 12, 32, 952834)),
        ),
    ]
