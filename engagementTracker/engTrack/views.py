from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Video
import cv2
import time, os
import numpy as np
from fer import FER
from django.db import transaction
from .models import Video, VideoStats
from django.views.generic.detail import DetailView

# Create your views here.

face_cascade = cv2.CascadeClassifier(r'./haarcascade_frontalface_default.xml')
fname = r'./haarcascade_frontalface_default.xml'
print(os.path.isfile(fname))
print(cv2.data.haarcascades)


def index(request):
    data = {
        'title': 'Список дел',
        'tasks': ['dolbaeb','hello','1233'],
        'task': {
            'author': 'Zheka146',
            'task_caption': 'ааа'
        }
    }

    return render(request, 'engTrack/index.html', data)

@login_required(login_url='/')
def dashboard(request):
    videos = Video.objects.all().order_by('-id')
    return render(request, 'engTrack/dashboard.html', {'videos': videos})

def upload_video(request):
    if request.method == 'POST':
        video_file = request.FILES['video_file']
        video = Video.objects.create(
            video_name=video_file.name,
            video_file = f'media/videos/{video_file.name}',
            video_author=request.user
        )
        video_path = f'media/videos/{video_file.name}'
        with open(video_path, 'wb+') as destination:
            for chunk in video_file.chunks():
                destination.write(chunk)
        process_video(video.id)  # Запускаем обработку
        return redirect('dashboard')
    return render(request, 'engTrack/upload_video.html') 

def process_video(video_id):
    """
    Обрабатывает видео с указанным ID, создаёт записи в VideoStats
    и обновляет статус в таблице Video.
    """
    try:
        # Получаем видео из базы данных
        video = Video.objects.get(id=video_id)
        video_path = f"media/videos/{video.video_name}"  # Предполагается, что видео сохранено в media/videos/
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            raise ValueError("Невозможно открыть видео")

        # Получаем параметры видео
        fps = int(cap.get(cv2.CAP_PROP_FPS))  # Частота кадров
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        video.video_length = total_frames
        video.status = "processing"
        video.video_processing_percentage = 0
        video.save()

        # Инициализация анализатора эмоций с MTCNN
        emotion_detector = FER(mtcnn=True)

        processed_frames = 0
        engagement_ratios = []
        processing_times = []

        # Переходим к обработке
        while cap.isOpened():
            # Перемещаемся на кадр, соответствующий следующей секунде
            cap.set(cv2.CAP_PROP_POS_FRAMES, processed_frames * fps)
            ret, frame = cap.read()
            if not ret:
                break

            processed_frames += 1

            frame_start_time = time.time()

            # Анализируем эмоции на текущем кадре
            emotion_results = emotion_detector.detect_emotions(frame)
            engaged_faces = sum(
                1 for result in emotion_results
                if result['emotions'] and max(result['emotions'], key=result['emotions'].get) in ['happy', 'surprise', 'neutral']
            )

            # Вычисляем процент вовлеченности
            engagement_ratio = (engaged_faces / len(emotion_results)) * 100 if emotion_results else 0
            engagement_ratios.append(engagement_ratio)

            # Время текущего кадра
            current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000  # В секундах

            # Сохраняем данные в базу
            VideoStats.objects.create(
                video_source=video,
                timing=processed_frames,
                timecode=time.strftime("%H:%M:%S", time.gmtime(current_time)),
                total_faces=len(emotion_results),
                engaged_faces=engaged_faces,
                engagement_percentage=int(engagement_ratio)
            )

            # Обновляем прогресс
            progress_percentage = (processed_frames / (total_frames / fps)) * 100
            video.video_processing_percentage = int(progress_percentage)
            video.save()

            # Замеряем время обработки
            frame_end_time = time.time()
            processing_time = frame_end_time - frame_start_time
            processing_times.append(processing_time)

        # После завершения обработки
        cap.release()
        video.status = "done"
        video.average_engagement_percentage = int(np.mean(engagement_ratios) if engagement_ratios else 0)
        video.save()

    except Exception as e:
        # В случае ошибки обновляем статус видео
        video.status = "canceled"
        video.save()
        raise e
    
class VideoView(DetailView):
    model = Video
    context_object_name = 'videoview'
    template_name = 'engTrack/video_stats.html'
    def get_context_data(self, **kwargs):
      context = super(VideoView, self).get_context_data(**kwargs)
      context['videostats_list'] = VideoStats.objects.all()
      return context