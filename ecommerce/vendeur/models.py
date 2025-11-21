
# vendeur/models.py

from django.db import models
from django.contrib.auth.models import User


class Vendeur(models.Model):
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=50, blank=True)
    ville = models.CharField(max_length=100, blank=True)
    entreprise = models.CharField(max_length=150, blank=True)
    STATUT_CHOICES = [
        ("ACTIF", "Actif"),
        ("SUSPENDU", "Suspendu"),
    ]
    statutCompte = models.CharField(max_length=10, choices=STATUT_CHOICES, default="ACTIF")

    def __str__(self):
        return f"{self.utilisateur.username} ({self.entreprise})"
    
