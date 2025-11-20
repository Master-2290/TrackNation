# ideas/admin.py
from django.contrib import admin
from .models import Hospital, Idea, PoliceStation, Vote, Project, Comment

# Configuration simple de l'affichage


class IdeaAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'district', 'status', 'created_at')
    list_filter = ('status', 'district')
    search_fields = ('title', 'description')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status', 'progress')
    list_filter = ('status',)


# Enregistrement des modèles
admin.site.register(Idea, IdeaAdmin)
admin.site.register(Vote)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Comment)
admin.site.register(PoliceStation)
admin.site.register(Hospital)
admin.site.site_header = "TrackNation Administration"
admin.site.site_title = "TrackNation Admin Portal"
admin.site.index_title = "Bienvenue dans le portail d'administration de TrackNation"
