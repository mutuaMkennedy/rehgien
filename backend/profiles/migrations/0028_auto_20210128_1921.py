# Generated by Django 2.2.12 on 2021-01-28 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0027_auto_20210128_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessprofile',
            name='service_areas',
            field=models.ManyToManyField(blank=True, related_name='service_areas', to='location.KenyaTown'),
        ),
    ]