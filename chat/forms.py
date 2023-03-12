from django import forms

from chat.models import *




class MessageForm(forms.ModelForm):
    contenu= forms.CharField(widget=forms.Textarea(attrs={"class":"forms", "rows":3, "placeholder": "Type message here"}))
    class Meta:
        model = Message
        fields = ["contenu",]

