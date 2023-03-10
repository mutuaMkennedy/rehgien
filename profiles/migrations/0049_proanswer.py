# Generated by Django 2.2.12 on 2021-10-18 09:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0048_question_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_answer', models.CharField(max_length=150)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('business_profile', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='match_answer', to='profiles.BusinessProfile')),
                ('option_answer', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pro_option_answer', to='profiles.QuestionOptions')),
                ('question', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='pro_question_answer', to='profiles.Question')),
            ],
        ),
    ]
