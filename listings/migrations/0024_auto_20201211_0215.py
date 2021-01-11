# Generated by Django 2.2.12 on 2020-12-10 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0023_auto_20201211_0126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='home',
            name='type',
            field=models.CharField(choices=[('DORMITORY', 'Dormitory'), ('TOWNHOUSE', 'Townhouse'), ('APARTMENT', 'Apartment'), ('BUNGALOW', 'Bungalow'), ('CONDOMINIUM', 'Condominium'), ('TERRACED', 'Terraced house'), ('OTHER', 'Other'), ('SINGLEFAMILY', 'Single family'), ('MANSION', 'Mansion'), ('DUPLEX', 'Duplex')], default='APARTMENT', max_length=20),
        ),
        migrations.AlterField(
            model_name='savedsearch',
            name='search_url',
            field=models.TextField(default=None, null=True),
        ),
    ]