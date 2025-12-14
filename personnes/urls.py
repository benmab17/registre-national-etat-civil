from django.urls import path
from . import views

urlpatterns = [
    # Authentification
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),

    # Page d'accueil : on redirige vers le login
    path("", views.login_view, name="accueil"),

    # Module état civil
    path("naissance/nouvelle/", views.nouvelle_naissance, name="nouvelle_naissance"),
    path("citoyen/adulte/nouveau/", views.nouvel_adulte, name="nouvel_adulte"),
    path("citoyen/recherche/", views.recherche_citoyen, name="recherche_citoyen"),
    path("citoyen/<int:personne_id>/", views.detail_citoyen, name="detail_citoyen"),
    path("citoyen/<int:personne_id>/acte-naissance/", views.acte_naissance_view, name="acte_naissance"),
    path("citoyen/<int:personne_id>/etablir-acte-naissance/", views.etablir_acte_naissance, name="etablir_acte_naissance"),
    path("stats/", views.stats_view, name="stats"),
]
