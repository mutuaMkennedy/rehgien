# Generated by Django 2.2.12 on 2021-01-08 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0038_auto_20210108_2018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='home',
            name='type',
            field=models.CharField(choices=[('TERRACED', 'Terraced house'), ('MANSION', 'Mansion'), ('TOWNHOUSE', 'Townhouse'), ('BUNGALOW', 'Bungalow'), ('DUPLEX', 'Duplex'), ('SINGLEFAMILY', 'Single family'), ('OTHER', 'Other'), ('CONDOMINIUM', 'Condominium'), ('DORMITORY', 'Dormitory'), ('APARTMENT', 'Apartment')], default='APARTMENT', max_length=20),
        ),
    ]
