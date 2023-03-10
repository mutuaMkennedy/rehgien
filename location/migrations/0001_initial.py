# Generated by Django 2.2.12 on 2020-11-21 15:58

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Districts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_0', models.BigIntegerField()),
                ('iso', models.CharField(max_length=3)),
                ('name_0', models.CharField(max_length=75)),
                ('id_1', models.BigIntegerField()),
                ('name_1', models.CharField(max_length=75)),
                ('id_2', models.BigIntegerField()),
                ('name_2', models.CharField(max_length=75)),
                ('type_2', models.CharField(max_length=50)),
                ('engtype_2', models.CharField(max_length=50)),
                ('nl_name_2', models.CharField(max_length=75)),
                ('varname_2', models.CharField(max_length=150)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
            options={
                'verbose_name_plural': 'Districts',
            },
        ),
        migrations.CreateModel(
            name='Divisions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_0', models.BigIntegerField()),
                ('iso', models.CharField(max_length=3)),
                ('name_0', models.CharField(max_length=75)),
                ('id_1', models.BigIntegerField()),
                ('name_1', models.CharField(max_length=75)),
                ('id_2', models.BigIntegerField()),
                ('name_2', models.CharField(max_length=75)),
                ('id_3', models.BigIntegerField()),
                ('name_3', models.CharField(max_length=75)),
                ('type_3', models.CharField(max_length=50)),
                ('engtype_3', models.CharField(max_length=50)),
                ('nl_name_3', models.CharField(max_length=75)),
                ('varname_3', models.CharField(max_length=100)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
            options={
                'verbose_name_plural': 'Divisions',
            },
        ),
        migrations.CreateModel(
            name='KenyaNationalPolytechnics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('descriptio', models.CharField(max_length=80)),
                ('geom', django.contrib.gis.db.models.fields.MultiPointField(srid=4326)),
            ],
            options={
                'verbose_name_plural': 'KenyaNationalPolytechnics',
            },
        ),
        migrations.CreateModel(
            name='KenyaPrimarySchools',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fid', models.BigIntegerField()),
                ('name_of_sc', models.CharField(max_length=80)),
                ('level_field', models.CharField(max_length=80)),
                ('status', models.CharField(max_length=80)),
                ('type1', models.CharField(max_length=80)),
                ('type2', models.CharField(max_length=80)),
                ('type3', models.CharField(max_length=80)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('geom', django.contrib.gis.db.models.fields.MultiPointField(srid=4326)),
            ],
            options={
                'verbose_name_plural': 'KenyaPrimarySchools',
            },
        ),
        migrations.CreateModel(
            name='PrivateColleges',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('descriptio', models.CharField(max_length=80)),
                ('geom', django.contrib.gis.db.models.fields.MultiPointField(srid=4326)),
            ],
            options={
                'verbose_name_plural': 'PrivateColleges',
            },
        ),
        migrations.CreateModel(
            name='PrivateUniversities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('descriptio', models.CharField(max_length=80)),
                ('geom', django.contrib.gis.db.models.fields.MultiPointField(srid=4326)),
            ],
            options={
                'verbose_name_plural': 'PrivateUniversities',
            },
        ),
        migrations.CreateModel(
            name='PublicColleges',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('descriptio', models.CharField(max_length=80)),
                ('geom', django.contrib.gis.db.models.fields.MultiPointField(srid=4326)),
            ],
            options={
                'verbose_name_plural': 'PublicColleges',
            },
        ),
        migrations.CreateModel(
            name='SecondarySchools',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institute', models.CharField(max_length=40)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('district', models.CharField(max_length=20)),
                ('division', models.CharField(max_length=30)),
                ('geom', django.contrib.gis.db.models.fields.MultiPointField(srid=4326)),
            ],
            options={
                'verbose_name_plural': 'SecondarySchools',
            },
        ),
        migrations.CreateModel(
            name='TeachersTrainingColleges',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('descriptio', models.CharField(max_length=80)),
                ('geom', django.contrib.gis.db.models.fields.MultiPointField(srid=4326)),
            ],
            options={
                'verbose_name_plural': 'TeachersTrainingColleges',
            },
        ),
        migrations.CreateModel(
            name='Universities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('descriptio', models.CharField(max_length=80)),
                ('geom', django.contrib.gis.db.models.fields.MultiPointField(srid=4326)),
            ],
            options={
                'verbose_name_plural': 'Universities',
            },
        ),
        migrations.CreateModel(
            name='UniversitiesColleges',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('descriptio', models.CharField(max_length=80)),
                ('geom', django.contrib.gis.db.models.fields.MultiPointField(srid=4326)),
            ],
            options={
                'verbose_name_plural': 'UniversitiesColleges',
            },
        ),
    ]
