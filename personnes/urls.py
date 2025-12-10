from django.urls import path
from . import views

urlpatterns = [
    path("naissance/nouvelle/", views.nouvelle_naissance, name="nouvelle_naissance"),
    path("citoyen/recherche/", views.recherche_citoyen, name="recherche_citoyen"),
    path("citoyen/<int:personne_id>/", views.detail_citoyen, name="detail_citoyen"),
    path("citoyen/<int:personne_id>/acte-naissance/", views.acte_naissance_view, name="acte_naissance"),
]
