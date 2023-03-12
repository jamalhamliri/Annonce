# models.py
from django.db import models

from annonces.models import Annonce
from users.models import CustomUser, Gest


# la table des conversations
class Conversation(models.Model):
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, default=False)
    user1 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, related_name='user1')
    gest1 = models.ForeignKey(Gest, on_delete=models.CASCADE, blank=True, null=True, related_name='gest1')
    user2 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=False, related_name='user2')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.annonce.name


# la table des messages
class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='conversation')
    sender_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True,
                                    related_name='sender_user')
    sender_gest = models.ForeignKey(Gest, on_delete=models.CASCADE, blank=True, null=True, related_name='sender_gest')
    contenu = models.TextField()
    seen = models.BooleanField(default=False)
    date_envoi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.contenu
