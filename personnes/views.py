from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from .forms import NaissanceForm, RecherchePersonneForm
from .models import Personne, ActeNaissance


# -----------------------------
# Utilitaires
# -----------------------------
def _generer_numero_acte(personne: Personne) -> str:
    """
    Génère un numéro d'acte simple à partir de la date de naissance + l'id.
    Exemple : 250101-0007
    """
    if personne.date_naissance:
        date_part = personne.date_naissance.strftime("%y%m%d")
    else:
        # au cas où la date serait absente (ne devrait pas arriver)
        from django.utils import timezone
        date_part = timezone.now().strftime("%y%m%d")

    return f"{date_part}-{personne.id:04d}"


# -----------------------------
# Authentification
# -----------------------------
def login_view(request):
    """
    Page de connexion.
    Utilise le template templates/login.html
    """
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # si ?next= est présent dans l'URL on y retourne, sinon dashboard
            next_url = request.GET.get("next") or request.POST.get("next") or "dashboard"
            return redirect(next_url)
    else:
        form = AuthenticationForm(request)

    return render(request, "login.html", {"form": form})


def logout_view(request):
    """
    Déconnexion puis retour vers la page de login.
    """
    logout(request)
    return redirect("login")


# Alias au cas où ton urls.py utilise d’autres noms
page_login = login_view
page_logout = logout_view


# -----------------------------
# Accueil & tableau de bord
# -----------------------------
def accueil(request):
    """
    / => si connecté -> dashboard, sinon -> login
    """
    if request.user.is_authenticated:
        return redirect("dashboard")
    return redirect("login")


@login_required(login_url="login")
def dashboard(request):
    """
    Tableau de bord principal.
    Utilise le template templates/dashboard.html
    """
    return render(request, "dashboard.html")


# -----------------------------
# Enregistrement d'une naissance
# -----------------------------
@login_required(login_url="login")
def nouvelle_naissance(request):
    """
    Formulaire d'enregistrement d'une nouvelle personne + acte de naissance.
    Utilise :
      - templates/naissance_form.html pour le formulaire
      - templates/naissance_succes.html après succès
    """
    if request.method == "POST":
        form = NaissanceForm(request.POST)
        if form.is_valid():
            personne: Personne = form.save()  # ModelForm lié à Personne

            # Création (ou récupération) de l'acte de naissance lié
            acte, created = ActeNaissance.objects.get_or_create(
                personne=personne,
                defaults={"numero_acte": _generer_numero_acte(personne)},
            )

            contexte = {
                "personne": personne,
                "acte": acte,
            }
            return render(request, "naissance_succes.html", contexte)
    else:
        form = NaissanceForm()

    return render(request, "naissance_form.html", {"form": form})


# -----------------------------
# Recherche d'un citoyen
# -----------------------------
@login_required(login_url="login")
def recherche_citoyen(request):
    """
    Moteur de recherche :
    - par numéro national
    - par nom / postnom / prénom
    - par date de naissance
    Utilise templates/recherche_citoyen.html
    """
    form = RecherchePersonneForm(request.GET or None)
    resultats = []

    if form.is_valid():
        numero_national = form.cleaned_data.get("numero_national")
        nom = form.cleaned_data.get("nom")
        postnom = form.cleaned_data.get("postnom")
        prenom = form.cleaned_data.get("prenom")
        date_naissance = form.cleaned_data.get("date_naissance")

        q = Q()
        if numero_national:
            q &= Q(numero_national__iexact=numero_national)
        if nom:
            q &= Q(nom__icontains=nom)
        if postnom:
            q &= Q(postnom__icontains=postnom)
        if prenom:
            q &= Q(prenom__icontains=prenom)
        if date_naissance:
            q &= Q(date_naissance=date_naissance)

        if q:
            resultats = Personne.objects.filter(q).order_by("nom", "postnom", "prenom")

    contexte = {
        "form": form,
        "resultats": resultats,
    }
    return render(request, "recherche_citoyen.html", contexte)


# -----------------------------
# Fiche détaillée d'un citoyen
# -----------------------------
@login_required(login_url="login")
def detail_citoyen(request, personne_id: int):
    """
    Affiche la fiche complète d'une personne + lien vers l'acte.
    Utilise templates/citoyen_detail.html
    """
    personne = get_object_or_404(Personne, pk=personne_id)
    acte = ActeNaissance.objects.filter(personne=personne).first()

    contexte = {
        "personne": personne,
        "acte": acte,
    }
    return render(request, "citoyen_detail.html", contexte)


# -----------------------------
# Affichage de l'acte de naissance
# -----------------------------
@login_required(login_url="login")
def acte_naissance(request, personne_id: int):
    """
    Affiche un acte de naissance HTML (pas de PDF pour rester simple
    et éviter des dépendances compliquées sur Render).
    Utilise templates/acte_naissance.html
    """
    personne = get_object_or_404(Personne, pk=personne_id)

    acte, created = ActeNaissance.objects.get_or_create(
        personne=personne,
        defaults={"numero_acte": _generer_numero_acte(personne)},
    )

    contexte = {
        "personne": personne,
        "acte": acte,
    }
    return render(request, "acte_naissance.html", contexte)
