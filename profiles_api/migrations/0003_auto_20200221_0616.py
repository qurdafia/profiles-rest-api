# Generated by Django 2.2 on 2020-02-21 06:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles_api', '0002_userprofile_reg_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='reg_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 2, 21, 6, 16, 16, 243262)),
        ),
    ]
