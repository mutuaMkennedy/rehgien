# Generated by Django 2.2.12 on 2020-08-12 23:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('markets', '0003_auto_20200811_0204'),
    ]

    operations = [
        migrations.AddField(
            model_name='otherservicelead',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='proffesionalrequestlead',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='propertyrequestlead',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='otherservicelead',
            name='timeline',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='proffesionalrequestlead',
            name='timeline',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='propertyrequestlead',
            name='property_type',
            field=models.CharField(choices=[('SINGLEFAMILY', 'Single family'), ('DORMITORY', 'Dormitory'), ('LAND', 'Land'), ('TOWNHOUSE', 'Townhouse'), ('MANSION', 'Mansion'), ('BUNGALOW', 'Bungalow'), ('TERRACED', 'Terraced house'), ('CONDOMINIUM', 'Condominium'), ('DUPLEX', 'Duplex'), ('APARTMENT', 'Apartment'), ('OTHER', 'Other')], max_length=20),
        ),
        migrations.AlterField(
            model_name='propertyrequestlead',
            name='timeline',
            field=models.DateField(),
        ),
    ]
