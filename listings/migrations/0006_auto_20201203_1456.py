# Generated by Django 2.2.12 on 2020-12-03 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0005_auto_20201202_0157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='home',
            name='type',
            field=models.CharField(choices=[('TOWNHOUSE', 'Townhouse'), ('APARTMENT', 'Apartment'), ('DORMITORY', 'Dormitory'), ('BUNGALOW', 'Bungalow'), ('CONDOMINIUM', 'Condominium'), ('SINGLEFAMILY', 'Single family'), ('TERRACED', 'Terraced house'), ('DUPLEX', 'Duplex'), ('MANSION', 'Mansion'), ('OTHER', 'Other')], default='APARTMENT', max_length=20),
        ),
        migrations.AlterField(
            model_name='home',
            name='virtual_tour_url',
            field=models.URLField(default=None),
        ),
    ]
