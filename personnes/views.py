from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

from .forms import NaissanceForm, RecherchePersonneForm
from .models import Personne, ActeNaissance


def login_view(request):
    """Page de connexion employés/admin."""
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    """Déconnexion simple puis retour à la page de login."""
    logout(request)
    return redirect("login")


@login_required
def dashboard_view(request):
    """Notre beau tableau de bord bleu 😊"""
    return render(request, "dashboard.html")
