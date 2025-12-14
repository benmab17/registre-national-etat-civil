from django import forms
from .models import Personne


class NaissanceForm(forms.ModelForm):
    class Meta:
        model = Personne
        fields = [
            'nom',
            'postnom',
            'prenom',
            'sexe',
            'date_naissance',
            'nom_pere',
            'prenom_pere',
            'nom_mere',
            'prenom_mere',
            'nationalite',
            'adresse_actuelle',
        ]
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de famille'}),
            'postnom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postnom'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            'sexe': forms.Select(attrs={'class': 'form-select'}),
            'date_naissance': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'nom_pere': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du père'}),
            'prenom_pere': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom du père'}),
            'nom_mere': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la mère'}),
            'prenom_mere': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom de la mère'}),
            'nationalite': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse_actuelle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adresse complète'}),
        }


class RecherchePersonneForm(forms.Form):
    numero_national = forms.CharField(
        required=False,
        label="Numéro national",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex : 251209001-14'})
    )
    nom = forms.CharField(
        required=False,
        label="Nom",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'})
    )
    postnom = forms.CharField(
        required=False,
        label="Postnom",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postnom'})
    )
    prenom = forms.CharField(
        required=False,
        label="Prénom",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'})
    )
    date_naissance = forms.DateField(
        required=False,
        label="Date de naissance",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )


class AdulteForm(forms.ModelForm):
    class Meta:
        model = Personne
        fields = [
            'nom',
            'postnom',
            'prenom',
            'sexe',
            'date_naissance',
            'nom_pere',
            'prenom_pere',
            'nom_mere',
            'prenom_mere',
            'nationalite',
            'adresse_actuelle',
        ]
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de famille'}),
            'postnom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postnom'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            'sexe': forms.Select(attrs={'class': 'form-select'}),
            'date_naissance': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'nom_pere': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du père'}),
            'prenom_pere': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom du père'}),
            'nom_mere': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la mère'}),
            'prenom_mere': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom de la mère'}),
            'nationalite': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse_actuelle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adresse complète'}),
        }
