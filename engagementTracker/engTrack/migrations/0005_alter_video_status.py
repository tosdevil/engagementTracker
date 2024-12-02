# Generated by Django 5.1.3 on 2024-12-01 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engTrack', '0004_alter_video_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='status',
            field=models.CharField(choices=[('processing', 'Processing'), ('done', 'Done'), ('canceled', 'Canceled'), ('pending', 'Pending')], default='pending', max_length=10),
        ),
    ]