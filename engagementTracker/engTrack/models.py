from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

class Video(models.Model):
    STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('done', 'Done'),
        ('canceled','Canceled'),
        ('pending','Pending')
    ]
    
    video_name = models.CharField('Название видео', max_length=250)
    video_file = models.FileField(upload_to='videos/')
    video_author = models.ForeignKey(User, on_delete = models.CASCADE, null = True, blank = True)
    video_processing_percentage = models.IntegerField('Обработка видео (готовность в процентах)', null = True, blank = True)
    video_upload_date = models.DateField('Дата публикации видео', default=now)
    video_length = models.IntegerField('Длина видео', null = True, blank = True)
    average_engagement_percentage = models.IntegerField("Средний процент вовлеченности", null = True, default='0')
    status = models.CharField(
        max_length=10,  # Длина строки
        choices=STATUS_CHOICES,  # Возможные варианты
        default='pending'  # Значение по умолчанию
    )


    def __str__(self):
        return self.video_name
    
    def get_absolute_url(self):
        return f"/videos/"
    
class VideoStats(models.Model):
    video_source = models.ForeignKey(Video, on_delete = models.CASCADE, null = True, blank = True)
    timing = models.IntegerField('Тайминг')
    timecode = models.TimeField()
    total_faces = models.IntegerField('Кол-во лиц')
    engaged_faces = models.IntegerField('Кол-во увлеченных лиц')
    engagement_percentage = models.IntegerField('Процент вовлеченности')

    def save(self, *args, **kwargs):
        if self.total_faces > 0:
            self.engagement_percentage = int((self.engaged_faces / self.total_faces) * 100)
        else:
            self.engagement_percentage = 0
        super().save(*args, **kwargs)
