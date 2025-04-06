from django import forms
from .models import Entreprise

class EntrepriseForm(forms.ModelForm):
    class Meta:
        model = Entreprise
        fields = '__all__'  # Inclut tous les champs
