from django.db import models
from django.views.generic.dates import DateMixin

from annonces.models import Annonce
from users.models import CustomUser


# Create your models here.
# la table favourite
class FavouriteAnnonce(models.Model):
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, related_name='Annonce')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user')
    is_favourite = models.BooleanField(default=True)

    def __str__(self):
        return "Annonce {} {} par {}".format(self.annonce.name, 'marque comme favourite', self.user.first_name)
