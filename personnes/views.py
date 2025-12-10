from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

from .forms import NaissanceForm, RecherchePersonneForm
from .models import Personne, ActeNaissance


def login_view(request):
    """
    Page de connexion pour les agents de l'état civil et l'admin.
    """
    if request.user.is_authenticated:
        return redirect("dashboard")

    message = None
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")
        else:
            message = "Identifiants incorrects. Veuillez réessayer."
    else:
        form = AuthenticationForm(request)

    contexte = {
        "form": form,
        "message": message,
    }
    return render(request, "login.html", contexte)


@login_required
def logout_view(request):
    """
    Déconnexion simple, retour à la page de login.
    """
    logout(request)
    return redirect("login")


@login_required
def dashboard(request):
    """
    Tableau de bord principal après connexion.
    """
    user = request.user
    contexte = {
        "user": user,
        "is_admin": user.is_staff or user.is_superuser,
    }
    return render(request, "dashboard.html", contexte)


@login_required
def nouvelle_naissance(request):
    """
    Page pour que l'officier encode une nouvelle naissance.
    """
    if request.method == "POST":
        form = NaissanceForm(request.POST)
        if form.is_valid():
            personne = form.save()  # numero_national généré automatiquement

            # Création automatique de l'acte de naissance associé
            acte = ActeNaissance.objects.create(
                personne=personne,
                lieu_etablissement="Commune de Démonstration",
                officier="Officier de l'état civil (démo)",
            )

            return render(request, "naissance_succes.html", {"personne": personne, "acte": acte})
    else:
        form = NaissanceForm()

    return render(request, "naissance_form.html", {"form": form})


@login_required
def recherche_citoyen(request):
    """
    Recherche d'un citoyen par numéro national, nom, postnom, prénom, date de naissance.
    """
    form = RecherchePersonneForm(request.GET or None)
    resultats = None

    if form.is_valid():
        data = form.cleaned_data
        if any(data.values()):
            qs = Personne.objects.all()

            if data.get("numero_national"):
                qs = qs.filter(numero_national__icontains=data["numero_national"])

            if data.get("nom"):
                qs = qs.filter(nom__icontains=data["nom"])

            if data.get("postnom"):
                qs = qs.filter(postnom__icontains=data["postnom"])

            if data.get("prenom"):
                qs = qs.filter(prenom__icontains=data["prenom"])

            if data.get("date_naissance"):
                qs = qs.filter(date_naissance=data["date_naissance"])

            resultats = qs.order_by("nom", "postnom", "prenom")

    contexte = {
        "form": form,
        "resultats": resultats,
    }
    return render(request, "recherche_citoyen.html", contexte)


@login_required
def detail_citoyen(request, personne_id):
    """
    Affiche la fiche détaillée d'un citoyen.
    """
    personne = get_object_or_404(Personne, id=personne_id)
    acte = getattr(personne, "acte_naissance", None)
    return render(request, "citoyen_detail.html", {"personne": personne, "acte": acte})


@login_required
def acte_naissance_view(request, personne_id):
    """
    Affiche l'acte de naissance officiel (version imprimable / PDF via impression navigateur).
    """
    personne = get_object_or_404(Personne, id=personne_id)
    acte = get_object_or_404(ActeNaissance, personne=personne)
    contexte = {
        "personne": personne,
        "acte": acte,
    }
    return render(request, "acte_naissance.html", contexte)
