# accounts/views.py
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import CitizenSignupForm
# Create your views here.


# Vue d'enregistrement (Signup)
def signup(request):
    if request.method == 'POST':
        form = CitizenSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CitizenSignupForm()

    return render(request, 'accounts/signup.html', {'form': form})

# Vues de connexion/déconnexion de base de Django
# Redéfinissent les vues de Django pour utiliser nos templates


class LoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('login')


@login_required
def role_based_redirect(request):
    """
    Redirige l'utilisateur vers son tableau de bord spécifique 
    en fonction de son rôle (citizen ou official).
    """
    if request.user.role == 'official':
        # L'élu va sur son tableau de bord de gestion
        return redirect(reverse('official_dashboard'))
    elif request.user.role == 'citizen':
        # Le citoyen va sur la liste des idées filtrées
        return redirect(reverse('idea_list'))
    else:
        # Pour tout autre rôle (ex: admin), rediriger vers l'admin ou une page par défaut
        return redirect('/admin/')


def home_redirect_view(request):
    """
    Redirige l'utilisateur vers la page d'accueil appropriée.
    - S'il est connecté : redirection basée sur le rôle (déjà implémentée).
    - S'il est déconnecté : redirection vers la page de connexion.
    """
    if request.user.is_authenticated:
        # Utilise la vue de redirection par rôle que nous avons déjà créée
        return redirect(reverse('role_based_redirect'))
    else:
        # Si déconnecté, rediriger vers la page de connexion (qui a aussi le lien vers l'inscription)
        return redirect(reverse('login'))
