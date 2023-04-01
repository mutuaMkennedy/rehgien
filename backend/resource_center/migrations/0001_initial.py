# Generated by Django 2.2.12 on 2021-01-08 17:12

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=125)),
                ('text', ckeditor.fields.RichTextField()),
                ('publishdate', models.DateTimeField(auto_now_add=True)),
                ('likes', models.ManyToManyField(related_name='blog_post_likes', to=settings.AUTH_USER_MODEL)),
                ('publisher', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('reads', models.ManyToManyField(related_name='blog_post_reads', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]