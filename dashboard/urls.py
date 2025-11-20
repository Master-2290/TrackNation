# dashboard/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('official/', views.official_dashboard, name='official_dashboard'),
]
