# Generated by Django 2.2.12 on 2020-12-23 22:04

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('markets', '0003_auto_20201123_2009'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25)),
                ('description', models.TextField()),
                ('project_size', models.CharField(choices=[('LARGE', 'large'), ('MEDIUM', 'medium'), ('SMALL', 'small')], max_length=20)),
                ('project_duration', models.CharField(choices=[('1', 'less than a week'), ('2', 'less than 1 month'), ('4', '1 to 3 months'), ('5', '3 to 6 months'), ('6', 'more than 6 months')], max_length=20)),
                ('skill_areas', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=100), blank=True, null=True, size=None)),
                ('verified', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('location', models.CharField(max_length=50)),
                ('job_creation_date', models.DateTimeField(auto_now_add=True)),
                ('job_update_date', models.DateTimeField(auto_now=True)),
                ('job_poster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_poster', to=settings.AUTH_USER_MODEL)),
                ('job_viewers', models.ManyToManyField(blank=True, related_name='job_viewer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'JobPosts',
            },
        ),
        migrations.AlterField(
            model_name='agentleadrequest',
            name='property_type',
            field=models.CharField(choices=[('BUNGALOW', 'Bungalow'), ('MANSION', 'Mansion'), ('SINGLEFAMILY', 'Single family'), ('DUPLEX', 'Duplex'), ('LAND', 'Land'), ('TERRACED', 'Terraced house'), ('TOWNHOUSE', 'Townhouse'), ('APARTMENT', 'Apartment'), ('DORMITORY', 'Dormitory'), ('OTHER', 'Other'), ('CONDOMINIUM', 'Condominium')], max_length=20),
        ),
        migrations.AlterField(
            model_name='agentpropertyrequest',
            name='property_type',
            field=models.CharField(choices=[('BUNGALOW', 'Bungalow'), ('MANSION', 'Mansion'), ('SINGLEFAMILY', 'Single family'), ('DUPLEX', 'Duplex'), ('LAND', 'Land'), ('TERRACED', 'Terraced house'), ('TOWNHOUSE', 'Townhouse'), ('APARTMENT', 'Apartment'), ('DORMITORY', 'Dormitory'), ('OTHER', 'Other'), ('CONDOMINIUM', 'Condominium')], max_length=20),
        ),
        migrations.AlterField(
            model_name='propertyrequestlead',
            name='property_type',
            field=models.CharField(choices=[('BUNGALOW', 'Bungalow'), ('MANSION', 'Mansion'), ('SINGLEFAMILY', 'Single family'), ('DUPLEX', 'Duplex'), ('LAND', 'Land'), ('TERRACED', 'Terraced house'), ('TOWNHOUSE', 'Townhouse'), ('APARTMENT', 'Apartment'), ('DORMITORY', 'Dormitory'), ('OTHER', 'Other'), ('CONDOMINIUM', 'Condominium')], max_length=20),
        ),
        migrations.CreateModel(
            name='JobPostProposal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('job_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_post_proposals', to='markets.JobPost')),
            ],
            options={
                'verbose_name_plural': 'JobPostProposals',
            },
        ),
    ]