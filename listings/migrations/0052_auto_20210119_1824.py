# Generated by Django 2.2.12 on 2021-01-19 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0051_auto_20210119_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='home',
            name='type',
            field=models.CharField(choices=[('DUPLEX', 'Duplex'), ('MANSION', 'Mansion'), ('BUNGALOW', 'Bungalow'), ('DORMITORY', 'Dormitory'), ('OTHER', 'Other'), ('TOWNHOUSE', 'Townhouse'), ('TERRACED', 'Terraced house'), ('APARTMENT', 'Apartment'), ('SINGLEFAMILY', 'Single family'), ('CONDOMINIUM', 'Condominium')], default='APARTMENT', max_length=20),
        ),
    ]
