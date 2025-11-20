from django.db import models
from accounts.models import User, District
from core import settings
# Create your models here.


class Idea(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # L'idée est liée à une circonscription
    district = models.ForeignKey(
        District, on_delete=models.CASCADE, related_name='ideas')

    # Statuts de l'idée
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('review', 'En analyse'),
        ('approved', 'Approuvé'),
        ('rejected', 'Rejeté'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    def __str__(self):
        return self.title


class Vote(models.Model):
    # Le vote concerne une Idea
    idea = models.ForeignKey(Idea, related_name='votes',
                             on_delete=models.CASCADE)
    # Le vote est fait par un User
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Assure qu'un utilisateur ne vote qu'une seule fois par idée
    class Meta:
        unique_together = ('idea', 'user')

    def __str__(self):
        return f"Vote de {self.user.username} pour l'idée {self.idea.title}"


class Comment(models.Model):
    idea = models.ForeignKey('Idea', on_delete=models.CASCADE)

    # L'auteur est l'utilisateur connecté
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    text = models.TextField(verbose_name="Commentaire")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"
        ordering = ['created_at']  # Tri par défaut

    def __str__(self):
        return f"Commentaire de {self.author.username} sur l'idée {self.idea.id}"


class Project(models.Model):
    # Un projet est la concrétisation d'une seule idée approuvée
    idea = models.OneToOneField(Idea, on_delete=models.CASCADE)

    # Informations de suivi du projet
    progress = models.IntegerField(default=0)

    STATUS_CHOICES = [
        ('planned', 'Planifié'),
        ('ongoing', 'En cours'),
        ('done', 'Terminé')
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='planned'
    )

    def __str__(self):
        return f"Projet: {self.idea.title}"


class PoliceStation(models.Model):
    # Lien avec la Circonscription de l'utilisateur
    district = models.ForeignKey(
        District,
        on_delete=models.CASCADE,
        related_name='police_stations',
        verbose_name="Circonscription"
    )

    name = models.CharField(
        max_length=150, verbose_name="Nom du Poste de Police")
    quartier = models.CharField(max_length=100, verbose_name="Quartier")
    commune = models.CharField(max_length=100, verbose_name="Commune")
    emergency_number = models.CharField(
        max_length=20, verbose_name="Numéro d'Urgence")

    # Optionnel : pour la géolocalisation sur une carte future
    # latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    # longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    class Meta:
        verbose_name = "Poste de Police"
        verbose_name_plural = "Postes de Police"

    def __str__(self):
        return f"{self.name} ({self.quartier})"


class Hospital(models.Model):
    # Liaison avec la Circonscription
    district = models.ForeignKey(
        District,  # Utiliser le nom réel de votre modèle de Circonscription
        on_delete=models.CASCADE,
        related_name='hospitals',
        verbose_name="Circonscription"
    )

    name = models.CharField(max_length=150, verbose_name="Nom de l'Hôpital")
    quartier = models.CharField(max_length=100, verbose_name="Quartier")
    commune = models.CharField(max_length=100, verbose_name="Commune")
    emergency_number = models.CharField(
        max_length=20, verbose_name="Numéro d'Urgence")

    class Meta:
        verbose_name = "Hôpital de Référence"
        verbose_name_plural = "Hôpitaux de Référence"

    def __str__(self):
        return f"{self.name} ({self.commune})"
