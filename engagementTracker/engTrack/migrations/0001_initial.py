# Generated by Django 5.1.3 on 2024-12-01 20:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_name', models.CharField(max_length=250, verbose_name='Название видео')),
                ('video_processing_percentage', models.IntegerField(verbose_name='Обработка видео (готовность в процентах)')),
                ('video_upload_date', models.DateField()),
                ('video_length', models.IntegerField()),
                ('average_engagement_percentage', models.IntegerField(verbose_name='')),
                ('video_author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VideoStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timing', models.IntegerField(verbose_name='Тайминг')),
                ('timecode', models.TimeField()),
                ('total_faces', models.IntegerField(verbose_name='Кол-во лиц')),
                ('engaged_faces', models.IntegerField(verbose_name='Кол-во увлеченных лиц')),
                ('engagement_percentage', models.IntegerField(verbose_name='Процент вовлеченности')),
                ('video_source', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='engTrack.video')),
            ],
        ),
    ]
