# Generated by Django 2.2.4 on 2021-05-01 06:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_registration_app', '0009_auto_20210501_0217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birthday',
            field=models.DateField(default=datetime.datetime(2021, 5, 1, 2, 24, 37, 149465)),
        ),
    ]
