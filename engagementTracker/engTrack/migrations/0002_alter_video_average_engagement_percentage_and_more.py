# Generated by Django 5.1.3 on 2024-12-01 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engTrack', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='average_engagement_percentage',
            field=models.IntegerField(default='0', null=True, verbose_name='Средний процент вовлеченности'),
        ),
        migrations.AlterField(
            model_name='video',
            name='video_length',
            field=models.IntegerField(blank=True, null=True, verbose_name='Длина видео'),
        ),
        migrations.AlterField(
            model_name='video',
            name='video_processing_percentage',
            field=models.IntegerField(blank=True, null=True, verbose_name='Обработка видео (готовность в процентах)'),
        ),
        migrations.AlterField(
            model_name='video',
            name='video_upload_date',
            field=models.DateField(verbose_name='Дата публикации видео'),
        ),
    ]