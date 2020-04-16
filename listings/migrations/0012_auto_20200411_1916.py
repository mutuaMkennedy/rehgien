# Generated by Django 2.1.3 on 2020-04-11 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0011_auto_20200411_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propertyforsale',
            name='type',
            field=models.CharField(choices=[('MANSION', 'Mansion'), ('TERRACED', 'Terraced house'), ('DORMITORY', 'Dormitory'), ('BUNGALOW', 'Bungalow'), ('CONDOMINIUM', 'Condominium'), ('SINGLEFAMILIY', 'Single family'), ('OTHER', 'Other'), ('APARTMENT', 'Apartment'), ('TOWNHOUSE', 'Townhouse'), ('DUPLEX', 'Duplex')], default='APARTMENT', max_length=20),
        ),
        migrations.AlterField(
            model_name='rentalproperty',
            name='type',
            field=models.CharField(choices=[('MANSION', 'Mansion'), ('TERRACED', 'Terraced house'), ('DORMITORY', 'Dormitory'), ('BUNGALOW', 'Bungalow'), ('CONDOMINIUM', 'Condominium'), ('SINGLEFAMILIY', 'Single family'), ('OTHER', 'Other'), ('APARTMENT', 'Apartment'), ('TOWNHOUSE', 'Townhouse'), ('DUPLEX', 'Duplex')], default='APARTMENT', max_length=20),
        ),
    ]
