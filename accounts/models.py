from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

# --- Modèle Circonscription (District) ---
# Chaque idée, projet et utilisateur (citoyen/élu) y sera lié.


class District(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name
#

# --- Modèle User personnalisé ---


class User(AbstractUser):
    # Rôles définis pour les utilisateurs
    ROLE_CHOICES = [
        ('citizen', 'Citoyen'),
        ('official', 'Élu'),
        ('admin', 'Administrateur'),
    ]
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default='citizen')

    # Association à la circonscription
    district = models.ForeignKey(
        District,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='users'
    )

    # Méthodes d'aide pour les vérifications de rôles
    def is_official(self):
        return self.role == 'official'

    def is_admin(self):
        return self.role == 'admin'

    def __str__(self):
        return self.email or self.username
