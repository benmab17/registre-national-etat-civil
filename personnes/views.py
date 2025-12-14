from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm

from .forms import PersonneForm, RecherchePersonneForm
from .models import Personne, ActeNaissance
from .audit import log_audit


@login_required
def dashboard(request):
    return render(request, "dashboard.html")


@login_required
def nouvelle_naissance(request):
    """
    Enregistrement d'une nouvelle naissance
    → crée Personne (type_enregistrement=NAISSANCE) + ActeNaissance NORMAL automatiquement
    """
    if request.method == "POST":
        form = PersonneForm(request.POST)
        if form.is_valid():
            personne = form.save(commit=False)
            personne.type_enregistrement = "NAISSANCE"
            personne.save()

            # Créer l'acte NORMAL (évite doublon si déjà existant)
            acte, created = ActeNaissance.objects.get_or_create(
                personne=personne,
                defaults={
                    "lieu_etablissement": "Commune de Démonstration",
                    "officier": "Officier de l'état civil (démo)",
                    "type_acte": "NORMAL",
                },
            )

            # Journal d'audit
            log_audit(
                request,
                action="CREATION_NAISSANCE",
                personne=personne,
                acte=acte,
                details="Création d'une naissance avec acte automatique",
            )

            return render(
                request,
                "naissance_succes.html",
                {"personne": personne, "acte": acte},
            )
    else:
        form = PersonneForm()

    return render(request, "naissance_form.html", {"form": form})


@login_required
def nouvel_adulte(request):
    """
    Enregistrement d'un adulte (recensement)
    → crée Personne (type_enregistrement=ADULTE) sans acte automatique
    """
    if request.method == "POST":
        form = PersonneForm(request.POST)
        if form.is_valid():
            personne = form.save(commit=False)
            personne.type_enregistrement = "ADULTE"
            personne.save()

            # Journal d'audit
            log_audit(
                request,
                action="CREATION_ADULTE",
                personne=personne,
                details="Enregistrement adulte (recensement)",
            )

            return redirect("detail_citoyen", personne_id=personne.id)
    else:
        form = PersonneForm()

    return render(request, "adulte_form.html", {"form": form})


@login_required
def etablir_acte_naissance(request, personne_id):
    """
    Établissement d'un acte de naissance tardif pour un adulte
    """
    personne = get_object_or_404(Personne, id=personne_id)

    # Si l'acte existe déjà, on redirige simplement
    acte = ActeNaissance.objects.filter(personne=personne).first()
    if acte:
        return redirect("acte_naissance", personne_id=personne.id)

    # Création de l'acte tardif
    acte = ActeNaissance.objects.create(
        personne=personne,
        lieu_etablissement="Commune de Démonstration",
        officier="Officier de l'état civil (démo)",
        type_acte="TARDIF",
    )

    # Journal d'audit
    log_audit(
        request,
        action="ETABLIR_ACTE_TARDIF",
        personne=personne,
        acte=acte,
        details="Établissement d'un acte de naissance tardif",
    )

    return redirect("acte_naissance", personne_id=personne.id)


@login_required
def recherche_citoyen(request):
    """
    Recherche d'un citoyen
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

    return render(
        request,
        "recherche_citoyen.html",
        {"form": form, "resultats": resultats},
    )


@login_required
def detail_citoyen(request, personne_id):
    """
    Fiche citoyenne
    """
    personne = get_object_or_404(Personne, id=personne_id)
    acte = ActeNaissance.objects.filter(personne=personne).first()

    return render(
        request,
        "citoyen_detail.html",
        {"personne": personne, "acte": acte},
    )


@login_required
def acte_naissance_view(request, personne_id):
    """
    Affiche l'acte de naissance officiel.
    """
    personne = get_object_or_404(Personne, id=personne_id)
    acte = get_object_or_404(ActeNaissance, personne=personne)

    contexte = {
        "personne": personne,
        "acte": acte,
    }
    return render(request, "acte_naissance.html", contexte)


@login_required
def stats_view(request):
    """
    Vue pour afficher les statistiques du registre.
    """
    total_citoyens = Personne.objects.count()
    total_naissances = Personne.objects.filter(type_enregistrement="NAISSANCE").count()
    total_adultes = Personne.objects.filter(type_enregistrement="ADULTE").count()
    total_actes = ActeNaissance.objects.count()
    actes_normaux = ActeNaissance.objects.filter(type_acte="NORMAL").count()
    actes_tardifs = ActeNaissance.objects.filter(type_acte="TARDIF").count()

    contexte = {
        "total_citoyens": total_citoyens,
        "total_naissances": total_naissances,
        "total_adultes": total_adultes,
        "total_actes": total_actes,
        "actes_normaux": actes_normaux,
        "actes_tardifs": actes_tardifs,
    }
    return render(request, "stats.html", contexte)


def login_view(request):
    # Si déjà connecté, aller au dashboard
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")
    else:
        form = AuthenticationForm(request)

    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")
