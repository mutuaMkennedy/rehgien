# Generated by Django 2.2.12 on 2020-12-23 10:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0012_auto_20201222_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='likes',
            field=models.ManyToManyField(null=True, related_name='liked_review', to=settings.AUTH_USER_MODEL),
        ),
    ]
