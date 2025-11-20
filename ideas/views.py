from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponse, Http404

from ideas.forms import IdeaForm


from .models import Idea, PoliceStation, Vote, Project, Comment, Hospital
from accounts.models import User
from django.db.models import Count, Exists, OuterRef
from .forms import IdeaForm, CommentForm
from accounts.decorators import official_required
from django.db.utils import IntegrityError
# Create your views here.

def accueil(request):
    return render(request, 'ideas/accueil.html')
@login_required
def idea_list(request):
    """
    Liste les idées en filtrant par la circonscription de l'utilisateur connecté (citoyen).
    """
    user_district = request.user.district
    user_id = request.user.id  # Récupération de l'ID utilisateur

    # Création d'un sous-QuerySet pour vérifier si l'utilisateur a voté pour une idée donnée
    # Ceci remplace les N requêtes dans le template par une annotation unique (subquery)
    user_vote_subquery = Vote.objects.filter(
        # 'idea' doit correspondre à l'idée de la requête principale
        idea=OuterRef('pk'),
        user=user_id  # Filtre par l'utilisateur connecté
    )

    ideas = Idea.objects.filter(
        district=user_district
    ).annotate(
        # NOUVEAU : Annotation booléenne pour savoir si l'utilisateur a voté
        has_voted_by_user=Exists(user_vote_subquery),
        # Garder l'annotation pour le compte total
        num_votes=Count('votes')
    ).order_by('-num_votes', '-created_at')

    context = {
        'ideas': ideas,
    }
    return render(request, 'ideas/idea_list.html', context)


# --- VUE DE VOTE (AJAX/HTMX) ---


@login_required
def vote_idea(request, idea_id):
    if request.user.role != 'citizen':
        # Seuls les citoyens peuvent voter
        return HttpResponse("Non autorisé", status=403)

    idea = get_object_or_404(Idea, pk=idea_id)
    user = request.user

    # Vérifie si l'utilisateur a déjà voté
    has_voted = Vote.objects.filter(user=user, idea=idea).exists()

    if has_voted:
        # Si a déjà voté, annuler le vote
        Vote.objects.filter(user=user, idea=idea).delete()
    else:
        # Sinon, créer le vote
        Vote.objects.create(user=user, idea=idea)

    # Préparer le contexte pour renvoyer le fragment HTMX mis à jour
    # Ceci est un pattern clé pour l'intégration HTMX
    context = {
        'idea': idea,
        'has_voted': not has_voted,  # L'état inverse
        'vote_id': f'vote-count-{idea.id}',
    }
    # Renvoyer le fragment HTML qui sera SWAP (remplacé) par HTMX
    return render(request, 'ideas/idea_list_vote_component.html', context)


@official_required
@require_POST
def update_idea_status(request, idea_id):
    """
    Vue HTMX pour changer le statut d'une idée par un Élu.
    Renvoie le nouveau statut sous forme de fragment HTML.
    """
    idea = get_object_or_404(Idea, id=idea_id)
    # Récupère la valeur du <select name="status">
    new_status = request.POST.get('status')

    # Vérification de sécurité : l'élu peut-il gérer cette idée ?
    if idea.district != request.user.district:
        return HttpResponse("Non autorisé.", status=403)

    if new_status in [choice[0] for choice in Idea.STATUS_CHOICES]:
        idea.status = new_status
        idea.save()

    # Logique pour le rendu du statut mis à jour (le badge)
    # Ceci est le fragment HTML qui remplace le <span id="idea-status-display-...">
    # Cette logique doit refléter la coloration Tailwind du template.
    status_display = idea.get_status_display()

    if new_status == 'approved':
        css_class = "bg-green-100 text-green-800"
    elif new_status == 'rejected':
        css_class = "bg-red-100 text-red-800"
    else:  # review, pending
        css_class = "bg-yellow-100 text-yellow-800"

    html_response = f"""
    <span id="idea-status-display-{idea.id}" class="ml-4 px-3 py-1 text-sm font-bold {css_class} rounded-full" hx-swap-oob="true">
        {status_display}
    </span>
    """
    # Renvoie la réponse HTTP, qui sera insérée par HTMX
    return HttpResponse(html_response)


@login_required
def submit_idea(request):
    # S'assurer que seul un citoyen peut soumettre une idée
    if request.user.role != 'citizen':
        # Rediriger ailleurs s'il n'est pas citoyen
        return redirect('idea_list')

    if request.method == 'POST':
        form = IdeaForm(request.POST)
        if form.is_valid():
            idea = form.save(commit=False)

            # ATTRIBUTION AUTOMATIQUE :
            # 1. Assigner l'auteur (utilisateur connecté)
            idea.author = request.user
            # 2. Assigner le district de l'utilisateur
            idea.district = request.user.district

            idea.save()
            # Rediriger vers la liste des idées après succès
            return redirect('idea_list')
    else:
        form = IdeaForm()

    return render(request, 'ideas/submit_idea.html', {'form': form})


@login_required
def idea_detail(request, idea_id):
    idea = get_object_or_404(Idea, pk=idea_id)
    user = request.user

    # Sécurité: S'assurer que les citoyens ne voient que les idées de leur circonscription
    if user.role == 'citizen' and idea.district != user.district:
        raise Http404("Cette idée n'est pas dans votre circonscription.")

    if request.method == 'POST':
        # 1. Traitement du formulaire de commentaire
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.idea = idea
            new_comment.author = user
            new_comment.save()

            # Rediriger vers la même page pour effacer les données POST du formulaire
            return redirect('idea_detail', idea_id=idea.id)

    else:
        comment_form = CommentForm()

    has_voted = Vote.objects.filter(user=user, idea=idea).exists()

    context = {
        'idea': idea,
        'comments': idea.comment_set.all().order_by('-created_at'),
        'comment_form': comment_form,  # Le formulaire
        'has_voted': has_voted,
        # ID pour la gestion HTMX potentielle
        'vote_id': f'vote-count-{idea.id}',
    }

    return render(request, 'ideas/idea_detail.html', context)


@login_required
def police_station_list(request):
    """
    Liste les postes de police en filtrant par la circonscription de l'utilisateur connecté.
    """
    user_district = request.user.district

    # Filtrer par circonscription de l'utilisateur
    stations = PoliceStation.objects.filter(
        district=user_district
    ).order_by('commune', 'quartier')  # Tri pour une meilleure lisibilité

    context = {
        'stations': stations,
        'user_district_name': user_district.name if user_district else "Non définie"
    }
    return render(request, 'ideas/police_station_list.html', context)


@login_required
def hospital_list(request):
    """
    Liste les hôpitaux de référence en filtrant par la circonscription de l'utilisateur.
    """
    # Vérifie si l'utilisateur a une circonscription attribuée
    user_district = request.user.district

    # Filtre les hôpitaux par circonscription de l'utilisateur
    hospitals = Hospital.objects.filter(
        district=user_district
    ).order_by('commune', 'quartier')

    context = {
        'hospitals': hospitals,
        'user_district_name': user_district.name if user_district else "Non définie"
    }
    return render(request, 'ideas/hospital_list.html', context)
