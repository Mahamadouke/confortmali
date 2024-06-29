from django.shortcuts import render, get_object_or_404, redirect
from .models import Employe, StatutEmploye, Livraison
from .forms import EmployeForm, StatutEmployeForm, LivraisonForm, SalaireForm

def liste_employes(request):
    employes = Employe.objects.all()
    return render(request, 'personnel/liste_employes.html', {'employes': employes})

def detail_employe(request, pk):
    employe = get_object_or_404(Employe, pk=pk)
    livraisons = Livraison.objects.filter(employe=employe)
    return render(request, 'personnel/detail_employe.html', {'employe': employe, 'livraisons': livraisons})

def ajouter_employe(request):
    if request.method == "POST":
        form = EmployeForm(request.POST)
        if form.is_valid():
            employe = form.save()
            return redirect('detail_employe', pk=employe.pk)
    else:
        form = EmployeForm()
    return render(request, 'personnel/ajouter_employe.html', {'form': form})

def ajouter_statut(request, pk):
    employe = get_object_or_404(Employe, pk=pk)
    if request.method == "POST":
        form = StatutEmployeForm(request.POST)
        if form.is_valid():
            statut = form.save(commit=False)
            statut.employe = employe
            statut.save()
            return redirect('detail_employe', pk=employe.pk)
    else:
        form = StatutEmployeForm()
    return render(request, 'personnel/ajouter_statut.html', {'form': form})

def ajouter_livraison(request):
    if request.method == "POST":
        form = LivraisonForm(request.POST)
        if form.is_valid():
            livraison = form.save()
            return redirect('detail_employe', pk=livraison.employe.pk)
    else:
        form = LivraisonForm()
    return render(request, 'personnel/ajouter_livraison.html', {'form': form})

def ajouter_salaire(request):
    if request.method == "POST":
        form = SalaireForm(request.POST)
        if form.is_valid():
            salaire = form.save()
            return redirect('detail_employe', pk=salaire.employe.pk)
    else:
        form = SalaireForm()
    return render(request, 'gestion/ajouter_salaire.html', {'form': form})