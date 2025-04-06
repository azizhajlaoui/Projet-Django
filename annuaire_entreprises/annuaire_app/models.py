from django.db import models

class Entreprise(models.Model):
    nom = models.CharField(max_length=255)
    secteur = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=15)
    adresse = models.CharField(max_length=255)
    site_web = models.URLField(blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom
