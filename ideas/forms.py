# ideas/forms.py

from django import forms
from .models import Idea, Comment


class IdeaForm(forms.ModelForm):
    """
    Formulaire pour permettre à un citoyen de soumettre une nouvelle idée.
    Le district et l'auteur seront définis automatiquement par la vue.
    """
    class Meta:
        model = Idea
        # Le citoyen doit seulement fournir le titre et la description.
        fields = ('title', 'description')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500', 'placeholder': 'Titre court et clair'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500', 'rows': 5, 'placeholder': 'Décrivez votre idée, pourquoi elle est nécessaire, et où elle devrait être mise en œuvre.'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError(
                "Le titre doit contenir au moins 5 caractères.")
        return title

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) < 10:
            raise forms.ValidationError(
                "La description doit contenir au moins 10 caractères.")
        return description


class CommentForm(forms.ModelForm):  # <-- NOUVEAU
    """
    Formulaire pour soumettre un commentaire.
    """
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-orange-500 focus:border-orange-500', 'rows': 3, 'placeholder': 'Ajoutez votre commentaire ici...'}),
        }
