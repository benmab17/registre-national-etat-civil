from django.contrib import admin
from .models import Personne


@admin.register(Personne)
class PersonneAdmin(admin.ModelAdmin):
    list_display = ('numero_national', 'nom', 'postnom', 'prenom', 'date_naissance', 'sexe')
    search_fields = ('numero_national', 'nom', 'postnom', 'prenom')
