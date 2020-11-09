# Generated by Django 2.2.12 on 2020-10-03 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0016_auto_20200927_1902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propertyforsale',
            name='type',
            field=models.CharField(choices=[('DUPLEX', 'Duplex'), ('DORMITORY', 'Dormitory'), ('TERRACED', 'Terraced house'), ('CONDOMINIUM', 'Condominium'), ('OTHER', 'Other'), ('APARTMENT', 'Apartment'), ('SINGLEFAMILY', 'Single family'), ('BUNGALOW', 'Bungalow'), ('TOWNHOUSE', 'Townhouse'), ('MANSION', 'Mansion')], default='APARTMENT', max_length=20),
        ),
        migrations.AlterField(
            model_name='rentalproperty',
            name='type',
            field=models.CharField(choices=[('DUPLEX', 'Duplex'), ('DORMITORY', 'Dormitory'), ('TERRACED', 'Terraced house'), ('CONDOMINIUM', 'Condominium'), ('OTHER', 'Other'), ('APARTMENT', 'Apartment'), ('SINGLEFAMILY', 'Single family'), ('BUNGALOW', 'Bungalow'), ('TOWNHOUSE', 'Townhouse'), ('MANSION', 'Mansion')], default='APARTMENT', max_length=20),
        ),
    ]