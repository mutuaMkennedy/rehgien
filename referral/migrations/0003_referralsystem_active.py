# Generated by Django 2.2.12 on 2022-06-01 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referral', '0002_auto_20220601_1235'),
    ]

    operations = [
        migrations.AddField(
            model_name='referralsystem',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]