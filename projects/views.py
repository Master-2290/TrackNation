# projects/views.py
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.urls import reverse
from accounts.decorators import official_required
from ideas.models import Idea, Project

# Create your views here.


@official_required
def convert_to_project(request, idea_id):
    """
    Convertit une idée approuvée en un nouveau projet.
    """
    idea = get_object_or_404(Idea, id=idea_id)

    # 1. Vérification du statut de l'idée
    if idea.status != 'approved':
        messages.error(
            request, "L'idée doit être 'Approuvée' avant de pouvoir être convertie en projet.")
        return redirect(reverse('official_dashboard'))

    # 2. Vérification de l'existence du projet
    if hasattr(idea, 'project'):
        messages.warning(request, "Cette idée est déjà associée à un projet.")
        return redirect(reverse('official_dashboard'))

    # 3. Création du projet
    try:
        # La relation OneToOne entre Idea et Project est établie ici
        Project.objects.create(idea=idea, progress=0, status='planned')
        messages.success(
            request, f"L'idée '{idea.title}' a été convertie en Projet (Planifié).")
    except Exception as e:
        messages.error(request, f"Erreur lors de la création du projet : {e}")

    # Rediriger l'élu vers son tableau de bord après l'action
    return redirect(reverse('official_dashboard'))

# Vue simple pour lister les projets (à développer)


@official_required
def project_list(request):
    """Liste tous les projets de la circonscription de l'élu."""
    projects = Project.objects.filter(
        idea__district=request.user.district).order_by('-id')
    context = {'projects': projects}
    return render(request, 'projects/project_list.html', context)
