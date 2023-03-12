from django.db import models


class Telephone_Marque(models.Model):
    name = models.CharField(verbose_name="Telephone Marque", max_length=255, unique=True)
    image = models.ImageField(upload_to='media/Telephone_Marque/', blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Telephone_Model(models.Model):
    marque = models.ForeignKey(Telephone_Marque, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Telephone Modele", max_length=255, unique=True)

    def __str__(self):
        return self.name


class Vehicle_Marque(models.Model):
    name = models.CharField(verbose_name="Marque", max_length=255, unique=True)
    image = models.ImageField(upload_to='media/Vehicle_Marque/', blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Vehicle_Modele(models.Model):
    Marque = models.ForeignKey(Vehicle_Marque, on_delete=models.CASCADE, default=False)
    name = models.CharField(verbose_name="Modele", max_length=255, unique=True)

    def __str__(self):
        return self.name


class Etat(models.Model):
    name = models.CharField(verbose_name="Etat", max_length=255, unique=True)

    def __str__(self):
        return self.name


class Stockage(models.Model):
    name = models.CharField(verbose_name="capacite de stockage", max_length=255, unique=True)

    def __str__(self):
        return self.name


class Voyage_Type(models.Model):
    name = models.CharField(verbose_name="Type de voyage", max_length=255, unique=True)

    def __str__(self):
        return self.name


class Type_Carburants(models.Model):
    name = models.CharField(verbose_name="Type de carburant", max_length=255, unique=True)

    def __str__(self):
        return self.name


class Origine(models.Model):
    name = models.CharField(verbose_name="Origine", max_length=255, unique=True)

    def __str__(self):
        return self.name


class Kilometrage(models.Model):
    name = models.CharField(verbose_name="Kilometrage", max_length=255, unique=True)

    def __str__(self):
        return self.name


class Puissance_fiscale(models.Model):
    name = models.CharField(verbose_name="Puissance fiscale", max_length=255, unique=True)

    def __str__(self):
        return self.name
