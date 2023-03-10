# Generated by Django 2.2.12 on 2020-12-04 13:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0010_auto_20201204_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='propertyinteraction',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='home',
            name='type',
            field=models.CharField(choices=[('TOWNHOUSE', 'Townhouse'), ('TERRACED', 'Terraced house'), ('BUNGALOW', 'Bungalow'), ('APARTMENT', 'Apartment'), ('DORMITORY', 'Dormitory'), ('OTHER', 'Other'), ('DUPLEX', 'Duplex'), ('MANSION', 'Mansion'), ('CONDOMINIUM', 'Condominium'), ('SINGLEFAMILY', 'Single family')], default='APARTMENT', max_length=20),
        ),
    ]
