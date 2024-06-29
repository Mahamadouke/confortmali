from django.db import models
from django.utils import timezone

class Employe(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_embauche = models.DateField(default=timezone.now)
    poste = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

class StatutEmploye(models.Model):
    EMPLOYE_CHOICES = [
        ('present', 'Présent'),
        ('absent', 'Absent'),
        ('malade', 'Malade'),
        ('conge', 'Congé'),
    ]
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    statut = models.CharField(max_length=10, choices=EMPLOYE_CHOICES)

    def __str__(self):
        return f"{self.employe} - {self.statut} le {self.date}"


class Livraison(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    description = models.TextField()
    status = models.CharField(max_length=100, choices=[('en cours', 'En cours'), ('livré', 'Livré')])

    def __str__(self):
        return f"Livraison par {self.employe} le {self.date}"
    
class Salaire(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    date_paiement = models.DateField(default=timezone.now)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    est_paye = models.BooleanField(default=False)

    def __str__(self):
        return f"Salaire de {self.employe} - {self.montant}€ le {self.date_paiement}"