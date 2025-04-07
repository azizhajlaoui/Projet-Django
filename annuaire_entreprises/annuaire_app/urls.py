from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),  # Page d'accueil
    path('entreprises/', views.liste_entreprises, name='liste_entreprises'),
    path('entreprise/<int:id>/', views.details_entreprise, name='details_entreprise'),
    path('ajouter/', views.ajouter_entreprise, name='ajouter_entreprise'),
    path('modifier/<int:id>/', views.modifier_entreprise, name='modifier_entreprise'),
    path('supprimer/<int:id>/', views.supprimer_entreprise, name='supprimer_entreprise'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
