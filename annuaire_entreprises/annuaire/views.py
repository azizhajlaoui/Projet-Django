from django.shortcuts import render, get_object_or_404, redirect
from .models import Entreprise
from .forms import EntrepriseForm

# Page d'accueil
def home(request):
    return render(request, 'home.html')

# Liste des entreprises
def liste_entreprises(request):
    entreprises = Entreprise.objects.all()
    return render(request, 'list.html', {'entreprises': entreprises})

# Détails d'une entreprise
def details_entreprise(request, id):
    entreprise = get_object_or_404(Entreprise, id=id)
    return render(request, 'detail.html', {'entreprise': entreprise})

# Ajouter une entreprise
def ajouter_entreprise(request):
    if request.method == 'POST':
        form = EntrepriseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_entreprises')
    else:
        form = EntrepriseForm()
    return render(request, 'form.html', {'form': form})

# Modifier une entreprise
def modifier_entreprise(request, id):
    entreprise = get_object_or_404(Entreprise, id=id)
    if request.method == 'POST':
        form = EntrepriseForm(request.POST, instance=entreprise)
        if form.is_valid():
            form.save()
            return redirect('liste_entreprises')
    else:
        form = EntrepriseForm(instance=entreprise)
    return render(request, 'form.html', {'form': form})

# Supprimer une entreprise
def supprimer_entreprise(request, id):
    entreprise = get_object_or_404(Entreprise, id=id)
    entreprise.delete()
    return redirect('liste_entreprises')
