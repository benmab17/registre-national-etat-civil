from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from personnes import views as personnes_views

urlpatterns = [
    # Admin Django
    path('admin/', admin.site.urls),

    # Authentification
    path('login/', auth_views.LoginView.as_view(
        template_name='login.html'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Tableau de bord / accueil applicatif
    path('dashboard/', personnes_views.dashboard, name='dashboard'),
    path('', personnes_views.accueil, name='accueil'),

    # Naissances & citoyens
    path('naissance/nouvelle/', personnes_views.nouvelle_naissance, name='nouvelle_naissance'),
    path('citoyen/recherche/', personnes_views.recherche_citoyen, name='recherche_citoyen'),
    path('citoyen/<int:personne_id>/', personnes_views.detail_citoyen, name='detail_citoyen'),
    path('citoyen/<int:personne_id>/acte-naissance/', personnes_views.acte_naissance, name='acte_naissance'),
]
