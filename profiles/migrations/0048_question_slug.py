# Generated by Django 2.2.12 on 2021-10-18 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0047_auto_20211018_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='slug',
            field=models.SlugField(blank=True, max_length=250),
        ),
    ]
