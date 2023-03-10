# Generated by Django 2.2.12 on 2021-10-03 17:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0038_auto_20211003_0515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resetpasswordotp',
            name='phone',
            field=models.CharField(blank=True, max_length=17, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+254xxxxxxxxx'. Up to 14 digits allowed.", regex='^\\+?1?\\d{9,14}$')]),
        ),
    ]
