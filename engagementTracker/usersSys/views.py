from django.shortcuts import render, redirect
from django.contrib import messages
# from .forms import UserRegisterForm
from django.contrib.auth.views import LoginView

from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    template = 'users/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('dashboard')