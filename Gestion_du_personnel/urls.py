from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_employes, name='liste_employes'),
    path('employe/<int:pk>/', views.detail_employe, name='detail_employe'),
    path('employe/ajouter/', views.ajouter_employe, name='ajouter_employe'),
    path('employe/<int:pk>/ajouter_statut/', views.ajouter_statut, name='ajouter_statut'),
    path('livraison/ajouter/', views.ajouter_livraison, name='ajouter_livraison'),
    path('salaire/ajouter/', views.ajouter_salaire, name='ajouter_salaire'),
]
