# Generated by Django 2.2.12 on 2022-07-17 13:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0002_kenyatown'),
        ('profiles', '0062_auto_20220120_1405'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estate_name', models.CharField(max_length=25, null=True)),
                ('house_name', models.CharField(max_length=25, null=True)),
                ('town', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_town', to='location.KenyaTown')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_address', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'User Address',
            },
        ),
    ]
