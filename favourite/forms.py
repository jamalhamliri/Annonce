from django import forms

from . import models
from .models import *


# formulaire pour supprimer une favourite
class Delete_favourite(forms.Form):
    delete_favourite = forms.BooleanField(widget=forms.HiddenInput, initial=True)
