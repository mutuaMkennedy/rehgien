# Generated by Django 2.2.12 on 2021-01-18 11:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RehgienPartner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('business_category', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=13)),
                ('approval_status', models.CharField(choices=[('APPROVED', 'approved'), ('PENDING', 'pending'), ('REJECTED', 'rejected')], default='PENDING', max_length=15)),
                ('request_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partnership_requestor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'RehgienPartner',
            },
        ),
    ]