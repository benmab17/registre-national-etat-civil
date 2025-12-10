from django.shortcuts import render, get_object_or_404
from .forms import NaissanceForm, RecherchePersonneForm
from .models import Personne, ActeNaissance


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
                # Tu pourras plus tard rendre ces champs dynamiques
                lieu_etablissement="Commune de Démonstration",
                officier="Officier de l'état civil (démo)",
            )

            return render(request, "naissance_succes.html", {"personne": personne, "acte": acte})
    else:
        form = NaissanceForm()

    return render(request, "naissance_form.html", {"form": form})


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


def detail_citoyen(request, personne_id):
    """
    Affiche la fiche détaillée d'un citoyen.
    """
    personne = get_object_or_404(Personne, id=personne_id)
    acte = getattr(personne, "acte_naissance", None)  # peut être None si pas encore créé
    return render(request, "citoyen_detail.html", {"personne": personne, "acte": acte})


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

