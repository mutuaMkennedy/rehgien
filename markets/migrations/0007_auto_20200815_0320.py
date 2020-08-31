# Generated by Django 2.2.12 on 2020-08-15 00:20

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('markets', '0006_auto_20200815_0206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agentleadrequest',
            name='property_type',
            field=models.CharField(choices=[('OTHER', 'Other'), ('TOWNHOUSE', 'Townhouse'), ('DORMITORY', 'Dormitory'), ('DUPLEX', 'Duplex'), ('SINGLEFAMILY', 'Single family'), ('CONDOMINIUM', 'Condominium'), ('LAND', 'Land'), ('APARTMENT', 'Apartment'), ('MANSION', 'Mansion'), ('BUNGALOW', 'Bungalow'), ('TERRACED', 'Terraced house')], max_length=20),
        ),
        migrations.AlterField(
            model_name='agentpropertyrequest',
            name='property_type',
            field=models.CharField(choices=[('OTHER', 'Other'), ('TOWNHOUSE', 'Townhouse'), ('DORMITORY', 'Dormitory'), ('DUPLEX', 'Duplex'), ('SINGLEFAMILY', 'Single family'), ('CONDOMINIUM', 'Condominium'), ('LAND', 'Land'), ('APARTMENT', 'Apartment'), ('MANSION', 'Mansion'), ('BUNGALOW', 'Bungalow'), ('TERRACED', 'Terraced house')], max_length=20),
        ),
        migrations.AlterField(
            model_name='propertyrequestlead',
            name='general_features',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('FURNISHED', 'Furnished'), ('SERVICED', 'Serviced')], max_length=18),
        ),
        migrations.AlterField(
            model_name='propertyrequestlead',
            name='parking_choices',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('CARP', 'Carport'), ('GATTACH', 'Garage-Attached'), ('GDETACH', 'Garage-Detached'), ('OFFS', 'Off-street'), ('ONST', 'On-street'), ('NON', 'None')], max_length=34),
        ),
        migrations.AlterField(
            model_name='propertyrequestlead',
            name='property_type',
            field=models.CharField(choices=[('OTHER', 'Other'), ('TOWNHOUSE', 'Townhouse'), ('DORMITORY', 'Dormitory'), ('DUPLEX', 'Duplex'), ('SINGLEFAMILY', 'Single family'), ('CONDOMINIUM', 'Condominium'), ('LAND', 'Land'), ('APARTMENT', 'Apartment'), ('MANSION', 'Mansion'), ('BUNGALOW', 'Bungalow'), ('TERRACED', 'Terraced house')], max_length=20),
        ),
    ]
