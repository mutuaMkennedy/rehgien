# Generated by Django 2.2.12 on 2022-07-27 17:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('markets', '0023_auto_20220717_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='order_item',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_item', to='profiles.PortfolioItem'),
        ),
    ]
