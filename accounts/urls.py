"""Определяет схемы URL для учетных записей."""

from django.urls import path, include

from . import views


app_name = 'accounts'
urlpatterns = [
    # Включить URL авторизации по умолчанию.
    path('', include('django.contrib.auth.urls')),
    # Страница регистрации.
    path('register/', views.register, name='register'),
]