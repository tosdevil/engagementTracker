from django.urls import path
from . import views
from .views import VideoView

urlpatterns = [
    path('', views.index, name = 'home'),
    path('dashboard/', views.dashboard, name = 'dashboard'),
    path('dashboard/upload', views.upload_video, name = 'upload'),
    path('dashboard/video/<int:pk>/', VideoView.as_view(), name = 'video_details')
]