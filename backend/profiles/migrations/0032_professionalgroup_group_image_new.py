# Generated by Django 2.2.12 on 2021-02-11 13:58

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0031_auto_20210211_1511'),
    ]

    operations = [
        migrations.AddField(
            model_name='professionalgroup',
            name='group_image_new',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image'),
        ),
    ]