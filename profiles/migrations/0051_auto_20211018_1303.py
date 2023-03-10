# Generated by Django 2.2.12 on 2021-10-18 10:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0050_auto_20211018_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientanswer',
            name='option_answer',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='option_answer', to='profiles.QuestionOptions'),
        ),
        migrations.AlterField(
            model_name='clientanswer',
            name='text_answer',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='proanswer',
            name='option_answer',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pro_option_answer', to='profiles.QuestionOptions'),
        ),
        migrations.AlterField(
            model_name='proanswer',
            name='text_answer',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
