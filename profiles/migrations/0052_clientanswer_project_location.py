# Generated by Django 2.2.12 on 2021-10-18 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0002_kenyatown'),
        ('profiles', '0051_auto_20211018_1303'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientanswer',
            name='project_location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='project_location', to='location.KenyaTown'),
        ),
    ]