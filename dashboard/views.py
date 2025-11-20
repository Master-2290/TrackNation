from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from accounts.decorators import official_required
from ideas.models import Idea, Project, Vote

# Create your views here.
# dashboard/views.py


@official_required
def official_dashboard(request):
    """Affiche le tableau de bord de l'Élu, filtré par circonscription."""

    # Récupérer les districts gérés par l'élu (pour une gestion multi-district future)
    # Pour l'instant, on prend le district principal de l'User
    user_districts = request.user.district

    # 1. Idées en attente dans la/les circonscription(s) de l'élu
    pending_ideas = Idea.objects.filter(
        district=user_districts,
        status='pending'
    ).order_by('-created_at')

    # 2. Statistiques rapides (Simulations pour remplir le template)
    ongoing_projects_count = Project.objects.filter(
        idea__district=user_districts, status='ongoing'
    ).count()

    total_votes_count = Vote.objects.filter(
        idea__district=user_districts
    ).count()

    context = {
        'pending_ideas': pending_ideas,
        'pending_ideas_count': pending_ideas.count(),
        'ongoing_projects_count': ongoing_projects_count,
        'total_votes_count': total_votes_count,
    }
    return render(request, 'dashboard/official_dashboard.html', context)
