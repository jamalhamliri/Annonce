from datetime import datetime

from PIL import Image
from django.contrib.auth import get_user
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from outil.models import *
from users.models import CustomUser, Gest
from .enums import AnnonceTYPE
#from django.contrib.gis.db.models import PointField

from .validators import file_size


# la table categorie des annonce

class Category(models.Model):
    name = models.CharField(verbose_name="categorie name", max_length=255, unique=True)
    image = models.ImageField(upload_to='media/categorie/', blank=True)
    block = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


# la table sous categories
class Subcategory(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='category',
                                 on_delete=models.CASCADE)
    name = models.CharField(verbose_name="categorie name", max_length=255,
                            unique=True)
    image = models.ImageField(upload_to='media/subcategorie/', blank=True)

    def __str__(self):
        return "la category : " + self.category.name + " --> sous categorie " + self.name


# la table wilaya
class Wilaya(models.Model):
    wilaya_name = models.CharField(verbose_name="wilaya name", max_length=255,
                                   unique=True)

    def __str__(self):
        return self.wilaya_name


# la table commune
class Commune(models.Model):
    wilaya = models.ForeignKey(Wilaya,
                               related_name='wilaya',
                               on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Commune name", max_length=255,
                            unique=True)

    def __str__(self):
        return self.wilaya.wilaya_name + " : commune " + self.name


# la table pour les annonces
class Annonce(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory,
                                    on_delete=models.CASCADE)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200)
    type = models.IntegerField(choices=AnnonceTYPE.choices(), default=AnnonceTYPE.Offre, )
    description = models.TextField(verbose_name="Description", max_length=500, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# la table pour les commentaires
class Commentaire(models.Model):
    gest = models.ForeignKey(Gest, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, default=None, related_name='commentaire')
    comment = models.TextField(blank=False)
    rating = models.IntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


# la table pour la localisation avec map
class Place(models.Model):
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, default=None, related_name='place')
    lat = models.FloatField(default=False)
    lng = models.FloatField(default=False)
    #coordinates = PointField()


# les photos d'annonce
class Images(models.Model):
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, default=None, related_name='images')
    image = models.ImageField(upload_to='media/annonce', validators=[file_size])
    IMAGE_MAX_SIZE = (400, 400)

    def resize_image(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        # sauvegarde de l’image redimensionnée dans le système de fichiers
        # ce n’est pas la méthode save() du modèle !
        image.save(self.image.path)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


# la table pour l'annonce voyage
class Voyage(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, default=False)
    ville_depart = models.CharField(max_length=200)
    ville_arrive = models.CharField(max_length=200)
    date_depart = models.DateField(default=False)
    date_arrive = models.DateField(default=False)
    description = models.TextField(blank=True, default=' ')
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


"""class Service(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory,
                                    related_name='Service',
                                    on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    lieu = models.CharField(max_length=200)
    date_fin = models.DateTimeField(default=False)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Photos(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, default=None, related_name='images')
    image = models.ImageField(upload_to='media/service', blank=True)
"""


# la table pour les informations sur annonce type telephone
class Telephone(models.Model):
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE)
    marque = models.ForeignKey(Telephone_Marque, on_delete=models.CASCADE)
    model = models.ForeignKey(Telephone_Model, on_delete=models.CASCADE)
    etat = models.ForeignKey(Etat, on_delete=models.CASCADE)
    stockage = models.ForeignKey(Stockage, on_delete=models.CASCADE)


# la table pour les informations sur annonce type vehicule
class Vehicule(models.Model):
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE)
    marque = models.ForeignKey(Vehicle_Marque, on_delete=models.CASCADE, default=False)
    modele = models.ForeignKey(Vehicle_Modele, on_delete=models.CASCADE, default=False)
    annee_modele = models.IntegerField()
    kilometrage = models.IntegerField()
    type_carburant = models.ForeignKey(Type_Carburants, on_delete=models.CASCADE)
    puissance_fiscale = models.CharField(max_length=200)
    boite_vitasses = models.CharField(choices=(('Automatique', 'Automatique'), ('Manuelle', 'Manuelle')),
                                      max_length=200)
    Nombre_portes = models.IntegerField()
    origine = models.ForeignKey(Origine, on_delete=models.CASCADE, default=True)
    etat = models.ForeignKey(Etat, on_delete=models.CASCADE, default=True)


# la table pour les informations sur annonce type immobilier
class Immobilier(models.Model):
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE)
    chambres = models.IntegerField()
    salle_bain = models.IntegerField()
    etage = models.IntegerField()
    surface = models.CharField(max_length=200)
    age = models.CharField(max_length=200)
    frais_syndic = models.CharField(max_length=200)


# la table pour les informations sur annonce type immobilier plus
class Immobilier_plus(models.Model):
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE)
    commerces_nombre = models.IntegerField()
    commerces_trajet = models.IntegerField()
    cafe_nombre = models.IntegerField()
    cafe_trajet = models.IntegerField()
    sport_nombre = models.IntegerField()
    sport_trajet = models.IntegerField()
    sante_nombre = models.IntegerField()
    sante_trajet = models.IntegerField()
    transport_nombre = models.IntegerField()
    transport_trajet = models.IntegerField()
    ecole_nombre = models.IntegerField()
    ecole_trajet = models.IntegerField()
    service_nombre = models.IntegerField()
    service_trajet = models.IntegerField()

#la table les top categories
class Top_category(models.Model):
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE)
    def __str__(self):
        return self.annonce.name