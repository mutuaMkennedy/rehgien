# Generated by Django 2.2.12 on 2022-01-20 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('markets', '0013_auto_20220120_1443'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='project_status',
            field=models.CharField(choices=[('ACTIVE', 'accepted'), ('COMPLETED', 'completed'), ('CANCELLED', 'cancelled')], default='ACTIVE', max_length=20, null=True),
        ),
    ]