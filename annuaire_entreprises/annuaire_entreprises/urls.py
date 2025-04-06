from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('annuaire_app.urls')),  # Inclusion des URLs de l'application "annuaire"
]
