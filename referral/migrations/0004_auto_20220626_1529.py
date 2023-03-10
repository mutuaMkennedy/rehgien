# Generated by Django 2.2.12 on 2022-06-26 15:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referral', '0003_referralsystem_active'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='referralsystem',
            options={'verbose_name_plural': 'Referral System'},
        ),
        migrations.AddField(
            model_name='recruiter',
            name='phone_number',
            field=models.CharField(max_length=17, null=True, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+254xxxxxxxxx'. Up to 14 digits allowed.", regex='^\\+?1?\\d{9,14}$')]),
        ),
    ]
