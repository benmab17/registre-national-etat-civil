from django.contrib import admin
from .models import Personne, ActeNaissance, JournalAudit


@admin.register(Personne)
class PersonneAdmin(admin.ModelAdmin):
    list_display = (
        "numero_national",
        "nom",
        "postnom",
        "prenom",
        "date_naissance",
        "sexe",
        "type_enregistrement",
    )
    search_fields = ("numero_national", "nom", "postnom", "prenom")
    list_filter = ("type_enregistrement", "sexe")
    ordering = ("nom", "postnom", "prenom")


@admin.register(ActeNaissance)
class ActeNaissanceAdmin(admin.ModelAdmin):
    list_display = (
        "personne",
        "type_acte",
        "date_etablissement",
    )
    list_filter = ("type_acte", "date_etablissement")
    search_fields = (
        "personne__numero_national",
        "personne__nom",
        "personne__postnom",
    )
    ordering = ("-date_etablissement",)


@admin.register(JournalAudit)
class JournalAuditAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "user",
        "action",
        "personne",
        "acte",
        "ip_address",
    )
    list_filter = ("action", "created_at")
    search_fields = (
        "user__username",
        "personne__numero_national",
        "personne__nom",
        "personne__postnom",
    )
    ordering = ("-created_at",)
