# projects/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.project_list, name='project_list'),
    path('<int:idea_id>/convert/', views.convert_to_project,
         name='convert_to_project'),
]
