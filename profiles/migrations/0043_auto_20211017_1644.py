# Generated by Django 2.2.12 on 2021-10-17 13:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0042_servicesearchhistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatchMaker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('professional_service', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='matchmaking_service', to='profiles.ProfessionalService')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionOptions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Option name', max_length=100, null=True)),
            ],
            options={
                'verbose_name_plural': 'Question Options',
            },
        ),
        migrations.AlterModelOptions(
            name='servicesearchhistory',
            options={'verbose_name_plural': 'Service Search History'},
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step', models.PositiveIntegerField(default=0, help_text='The step where the question will appear')),
                ('title', models.CharField(help_text='A short title of question e.g. Number of rooms, Cleaning Type', max_length=100)),
                ('question', models.TextField(help_text='The full question e.g. How many rooms are you painting?')),
                ('question_type', models.CharField(choices=[('MULTIPLE_CHOICE', 'Multiple Choice'), ('SINGLE_CHOICE', 'Single Choice'), ('TEXT_INPUT', 'Text Input')], default='TEXT_INPUT', max_length=100)),
                ('matchMaker', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='matchmaker_question', to='profiles.MatchMaker')),
                ('question_options', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='question_option', to='profiles.QuestionOptions')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_answer', models.CharField(max_length=150)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('option_answer', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='option_answer', to='profiles.QuestionOptions')),
                ('question', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='question_answer', to='profiles.Question')),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_answer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]