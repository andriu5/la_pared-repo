# Generated by Django 2.2.4 on 2021-05-04 05:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_registration_app', '0032_auto_20210504_0105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birthday',
            field=models.DateField(default=datetime.datetime(2021, 5, 4, 1, 9, 36, 695240)),
        ),
    ]
