# Generated by Django 2.2.12 on 2020-11-28 17:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_auto_20201128_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='teammateconnection',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
