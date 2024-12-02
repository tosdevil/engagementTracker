from django.urls import path
from . import views
from .views import CustomLoginView

from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('logout/', LogoutView.as_view(next_page = 'home'), name = 'logout'),
    path('', CustomLoginView.as_view(), name = 'login')
]