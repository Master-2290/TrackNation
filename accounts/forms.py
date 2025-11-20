# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, District


class CitizenSignupForm(UserCreationForm):
    """Formulaire d'inscription simple pour les citoyens."""
    # Le citoyen choisit sa circonscription à l'inscription
    district = forms.ModelChoiceField(
        queryset=District.objects.all(),
        label="Votre Circonscription",
        empty_label="Sélectionnez votre zone",
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + \
            ('district', 'role',)  # Inclure le district et le rôle

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'citizen'  # Attribue le rôle 'citizen' par défaut
        user.district = self.cleaned_data.get('district')
        if commit:
            user.save()
        return user
