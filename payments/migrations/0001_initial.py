# Generated by Django 2.2.12 on 2022-03-10 11:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('markets', '0018_auto_20220128_0056'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionReceipt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(default=None)),
                ('transaction_status', models.CharField(choices=[('ESCROW', 'escrow'), ('SETTLED', 'settled'), ('REFUNDED', 'refunded')], default='ESCROW', max_length=25)),
                ('payment_method', models.CharField(choices=[('MPESA', 'mpesa'), ('CARD', 'card')], default='MPESA', max_length=25)),
                ('description', models.TextField()),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='markets.Project')),
                ('recepient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transaction_receipt_payment_recepient', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transaction_receipt_payment_sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Transaction receipts',
            },
        ),
    ]