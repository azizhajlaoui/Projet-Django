from django.shortcuts import render, get_object_or_404, redirect
from .models import Entreprise
from .forms import EntrepriseForm

def home(request):
    return render(request, 'home.html')

def liste_entreprises(request):
    entreprises = Entreprise.objects.all()
    return render(request, 'list.html', {'entreprises': entreprises})

def details_entreprise(request, entreprise_id):
    entreprise = get_object_or_404(Entreprise, id=entreprise_id)
    return render(request, 'detail.html', {'entreprise': entreprise})

def ajouter_entreprise(request):
    if request.method == "POST":
        form = EntrepriseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_entreprises')
    else:
        form = EntrepriseForm()
    return render(request, 'form.html', {'form': form})

def modifier_entreprise(request, entreprise_id):
    entreprise = get_object_or_404(Entreprise, id=entreprise_id)
    if request.method == "POST":
        form = EntrepriseForm(request.POST, instance=entreprise)
        if form.is_valid():
            form.save()
            return redirect('liste_entreprises')
    else:
        form = EntrepriseForm(instance=entreprise)
    return render(request, 'form.html', {'form': form})

def supprimer_entreprise(request, entreprise_id):
    entreprise = get_object_or_404(Entreprise, id=entreprise_id)
    entreprise.delete()
    return redirect('liste_entreprises')
