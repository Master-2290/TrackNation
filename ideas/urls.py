# ideas/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.idea_list, name='idea_list'),
    path('submit/', views.submit_idea, name='submit_idea'),
    path('<int:idea_id>/', views.idea_detail, name='idea_detail'),
    path('<int:idea_id>/vote/', views.vote_idea, name='vote_idea'),
    path('<int:idea_id>/status/', views.update_idea_status,
         name='update_idea_status'),
    path('police-stations/', views.police_station_list,
         name='police_station_list'),
    path('hospitals/', views.hospital_list, name='hospital_list'),
]
