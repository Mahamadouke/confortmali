from django.contrib import admin
from .models import Employe, StatutEmploye, Livraison, Salaire

admin.site.register(Employe)
admin.site.register(StatutEmploye)
admin.site.register(Livraison)
admin.site.register(Salaire)

