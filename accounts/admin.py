# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, District
# Register your models here.


# Configuration de l'affichage du modèle User
class UserAdmin(BaseUserAdmin):
    # Ajout du rôle et du district aux champs affichés
    list_display = ('username', 'email', 'first_name',
                    'last_name', 'role', 'district', 'is_staff')

    # Ajout du rôle et du district au formulaire de modification
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('role', 'district',)}),
    )


# Enregistrement des modèles
admin.site.register(User, UserAdmin)
admin.site.register(District)
