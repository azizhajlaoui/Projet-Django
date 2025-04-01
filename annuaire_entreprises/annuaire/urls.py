from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('entreprises/', views.liste_entreprises, name='liste_entreprises'),
    path('entreprises/<int:entreprise_id>/', views.details_entreprise, name='details_entreprise'),
    path('entreprises/ajouter/', views.ajouter_entreprise, name='ajouter_entreprise'),
    path('entreprises/modifier/<int:entreprise_id>/', views.modifier_entreprise, name='modifier_entreprise'),
    path('entreprises/supprimer/<int:entreprise_id>/', views.supprimer_entreprise, name='supprimer_entreprise'),
]
