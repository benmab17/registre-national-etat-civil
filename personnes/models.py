from django.db import models
from django.utils import timezone


class Personne(models.Model):
    SEXE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]

    # Exemple : 251209001-14
    numero_national = models.CharField(max_length=12, unique=True, blank=True)

    nom = models.CharField(max_length=100)
    postnom = models.CharField(max_length=100, blank=True)
    prenom = models.CharField(max_length=100)

    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
    date_naissance = models.DateField()

    nom_pere = models.CharField(max_length=100)
    prenom_pere = models.CharField(max_length=100, blank=True)
    nom_mere = models.CharField(max_length=100)
    prenom_mere = models.CharField(max_length=100, blank=True)

    nationalite = models.CharField(max_length=100, default='Congolaise')
    adresse_actuelle = models.CharField(max_length=255, blank=True)

    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nom} {self.postnom} {self.prenom} ({self.numero_national})"

    def save(self, *args, **kwargs):
        # Générer automatiquement le numéro national
        if not self.numero_national and self.date_naissance:
            self.numero_national = self.generer_numero_national()
        super().save(*args, **kwargs)

    def generer_numero_national(self):
        """
        Génère un numéro du type AAMMJJOOO-CC :
        - AA = 2 derniers chiffres de l'année
        - MM = mois
        - JJ = jour
        - OOO = ordre (compteur des personnes déjà enregistrées pour cette date + 1)
        - CC = clé de contrôle mod 97
        """

        # 1) Partie date AAMMJJ
        aa = str(self.date_naissance.year)[-2:]
        mm = f"{self.date_naissance.month:02d}"
        jj = f"{self.date_naissance.day:02d}"
        date_part = f"{aa}{mm}{jj}"  # Exemple : 251209

        # 2) Calcul de OOO (ordre de la naissance ce jour-là)
        count_same_date = self.__class__.objects.filter(date_naissance=self.date_naissance).count()
        ordre = count_same_date + 1
        ooo = f"{ordre:03d}"  # Exemple : 001, 045, 452

        # 3) Calcul de la clé de contrôle CC
        base_number = int(f"{date_part}{ooo}")  # 9 chiffres
        reste = base_number % 97
        cc_val = 97 - reste
        if cc_val == 97:
            cc_val = 0
        cc = f"{cc_val:02d}"

        # Final : AAMMJJOOO-CC
        return f"{date_part}{ooo}-{cc}"


class ActeNaissance(models.Model):
    """
    Acte de naissance officiel lié à une Personne.
    Un acte par personne.
    """
    personne = models.OneToOneField(Personne, on_delete=models.CASCADE, related_name="acte_naissance")
    numero_acte = models.CharField(max_length=20, unique=True, blank=True)
    date_etablissement = models.DateField(auto_now_add=True)
    lieu_etablissement = models.CharField(max_length=150, default="Commune de Démonstration")
    officier = models.CharField(max_length=150, default="Officier de l'état civil (démo)")

    def __str__(self):
        return f"Acte {self.numero_acte} – {self.personne.nom} {self.personne.postnom} {self.personne.prenom}"

    def save(self, *args, **kwargs):
        # Générer le numéro d'acte si absent
        if not self.numero_acte:
            self.numero_acte = self.generer_numero_acte()
        super().save(*args, **kwargs)

    def generer_numero_acte(self):
        """
        Numéro d'acte du type : AN-2025-00001
        (AN = acte de naissance, année, compteur annuel)
        """
        annee = timezone.now().year
        count_year = ActeNaissance.objects.filter(date_etablissement__year=annee).count() + 1
        return f"AN-{annee}-{count_year:05d}"
