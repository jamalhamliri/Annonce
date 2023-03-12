from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from django.db.models import Q

from config import settings
from .managers import CustomUserManager
from multiselectfield import MultiSelectField
import datetime


# fonction pour convert email a des lettres minuscules
class LowercaseEmailField(models.EmailField):
    """
    Override EmailField to convert emails to lowercase before saving.
    """

    def to_python(self, value):
        """
        Convert email to lowercase.
        """
        value = super(LowercaseEmailField, self).to_python(value)
        # Value can be None so check that it's a string before lowercasing.
        if isinstance(value, str):
            return value.lower()
        return value


# la table utilisateur
class CustomUser(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        ('', 'Choose gender'),
        ('Homme', 'Homme'),
        ('Femme', 'Femme'),
    )
    Normal = 'Normal'
    Type = (
        ("Pro", "PRO"),
        ("Normal", "NORMAL")
    )
    alphanumeric = RegexValidator(r'^[a-zA-Z]*$', 'Seuls les caractères alphanumériques sont autorisés.')
    pinnumbers = RegexValidator(r'^[0-9]*$', 'Seuls les chiffres entre 0 et 9 sont autorisés.')
    email = LowercaseEmailField(_('email address'), max_length=255, unique=True)
    first_name = models.CharField(max_length=150, blank=True, validators=[alphanumeric])
    last_name = models.CharField(max_length=150, blank=True, validators=[alphanumeric])
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, blank=True)
    type = models.CharField(max_length=50, default=Normal)
    about = models.TextField(_('compliment'), max_length=500, blank=True)
    image = models.ImageField(verbose_name='Photo de profil', upload_to='media/user/', blank=True)
    address = models.CharField(max_length=1000, blank=True)
    phone_regex = RegexValidator(regex=r'^\d{16}$', message="phone number should exactly be in 10 digits")
    phone = models.CharField(max_length=16, blank=True,
                             null=True)  # you can set it unique = True
    date_of_birth = models.DateField(_("Date de naissance"), default=datetime.date.today)
    date_joined = models.DateTimeField(default=timezone.now)
    # Les utilisateurs de is staff auront accès aux abonnements au panneau d'administration, etc.
    is_staff = models.BooleanField(default=False)

    is_active = models.BooleanField(default=False)  # Détermine que l'utilisateur peut se connecter à l'application Web

    # lorsque l'utilisateur est créé, le système envoie un e-mail après avoir vérifié l'utilisateur, nous vérifions que l'utilisateur est actif

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# la table des listes des utilisateur normal
class NormalAdditional(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


# la table des utilisater particuliere qui contienne le donnees de leur entreprise
class ProAdditional(models.Model):
    alphanumeric = RegexValidator(r'^[a-zA-Z]*$', 'Seuls les caractères alphanumériques sont autorisés.')
    pinnumbers = RegexValidator(r'^[0-9]*$', 'Seuls les chiffres entre 0 et 9 sont autorisés.')

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    numero_ent = models.CharField(verbose_name="Numero d'entreprise", max_length=14, validators=[pinnumbers])
    nom_ent = models.CharField(verbose_name="Nom d'entreprise", max_length=100, blank=True)
    categorie = models.CharField(max_length=100, blank=True, validators=[alphanumeric],
                                 help_text="entreprise categorie")
    address = models.CharField(verbose_name="le lieu de l'entreprise", max_length=100, blank=True)
    justification = models.FileField(upload_to='media/pro_justification', blank=True)

    def __str__(self):
        return self.user.email


# la table des invites
class Gest(models.Model):
    alphanumeric = RegexValidator(r'^[a-zA-Z]*$', 'Seuls les caractères alphanumériques sont autorisés.')
    email = LowercaseEmailField(_('email address'), max_length=255,unique=True)
    first_name = models.CharField(_('first name'), max_length=150, blank=True, validators=[alphanumeric])
    last_name = models.CharField(_('last name'), max_length=150, blank=True, validators=[alphanumeric])
    numero = models.CharField(_('numero'), max_length=14)
    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
