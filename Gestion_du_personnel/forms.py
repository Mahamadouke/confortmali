from django import forms
from .models import Employe, StatutEmploye, Livraison, Salaire

class EmployeForm(forms.ModelForm):
    class Meta:
        model = Employe
        fields = ['nom', 'prenom', 'email', 'date_embauche', 'poste', 'salaire', 'est_paye']

class StatutEmployeForm(forms.ModelForm):
    class Meta:
        model = StatutEmploye
        fields = ['date', 'statut']

class LivraisonForm(forms.ModelForm):
    class Meta:
        model = Livraison
        fields = ['employe', 'date', 'description', 'status']

class SalaireForm(forms.ModelForm):
    class Meta:
        model = Salaire
        fields = ['employe', 'date_paiement', 'montant', 'est_paye']