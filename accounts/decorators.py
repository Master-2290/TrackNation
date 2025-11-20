# accounts/decorators.py
from django.contrib.auth.decorators import user_passes_test


def is_official_user(user):
    """Vérifie si l'utilisateur est un 'official' (Élu)."""
    return user.is_authenticated and user.role == 'official'


def official_required(view_func, redirect_field_name=None, login_url='/login/'):
    """Décorateur qui restreint l'accès aux utilisateurs Élus."""
    return user_passes_test(
        is_official_user,
        redirect_field_name=redirect_field_name,
        login_url=login_url
    )(view_func)
