# Generated by Django 2.2.12 on 2021-02-24 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0056_auto_20210224_0305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='home',
            name='virtual_tour_url',
            field=models.URLField(blank=True, default=None, null=True),
        ),
    ]