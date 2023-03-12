from django import forms
from django.forms import NumberInput
from . import models
from .models import *


# formulaire pour catgorie
class MyCategory(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all())

    def __init__(self, *args, **kwargs):
        super(MyCategory, self).__init__(*args, **kwargs)

        self.fields['category'].widget.attrs.update({'class': "form-select"})


# formulaire pour vehicule marque
class MyVehicule_marque(forms.Form):
    marque = forms.ModelChoiceField(queryset=Vehicle_Marque.objects.all())

    def __init__(self, *args, **kwargs):
        super(MyVehicule_marque, self).__init__(*args, **kwargs)
        self.fields['marque'].label = 'La marque'
        self.fields['marque'].widget.attrs.update({'class': "form-select"})


# formulaire pour telephone marque
class MyMedia_marque(forms.Form):
    marque = forms.ModelChoiceField(queryset=Telephone_Marque.objects.all())

    def __init__(self, *args, **kwargs):
        super(MyMedia_marque, self).__init__(*args, **kwargs)
        self.fields['marque'].label = 'La marque'
        self.fields['marque'].widget.attrs.update({'class': "form-select"})


# formulaire pour wilaya
class Wilaya(forms.Form):
    wilaya = forms.ModelChoiceField(queryset=Wilaya.objects.all())

    def __init__(self, *args, **kwargs):
        super(Wilaya, self).__init__(*args, **kwargs)
        self.fields['wilaya'].widget.attrs.update({'class': "form-select"})


# formulaire pour annonce
class AddAd(forms.ModelForm):
    # category = forms.ChoiceField(choices=[(item.pk, item) for item in Category.objects.all()])
    # subcategory = forms.ChoiceField(choices=[(item.pk, item) for item in Subcategory.objects.filter(category)])

    class Meta():
        model = Annonce
        fields = '__all__'
        exclude = ['user', 'subcategory', 'commune']

    def __init__(self, *args, **kwargs):
        super(AddAd, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': "form-control"})
        self.fields['type'].widget.attrs.update({'class': "form-select"})
        # self.fields['commune'].widget.attrs.update({'class': "form-select"})
        # self.fields['subcategory'].label = 'La categorie'
        # self.fields['subcategory'].widget.attrs.update({'label': 'sous Categorie', 'class': "form-select"})


# formulaire pour voyage
class AddTravel(forms.ModelForm):
    date_arrive = forms.DateField(widget=NumberInput(attrs={'type': 'date', 'class': "form-control"}))
    date_depart = forms.DateField(widget=NumberInput(attrs={'type': 'date', 'class': "form-control"}))

    class Meta():
        model = Voyage
        fields = '__all__'
        exclude = ['user', 'annonce']

    def __init__(self, *args, **kwargs):
        super(AddTravel, self).__init__(*args, **kwargs)
        self.fields['ville_depart'].widget.attrs.update({'class': "form-control"})
        self.fields['ville_arrive'].widget.attrs.update({'class': "form-control"})
        self.fields['type'].widget.attrs.update({'class': "form-select"})
        self.fields['budget'].widget.attrs.update({'class': "form-control"})


"""class AddService(forms.ModelForm):
    # category = forms.ChoiceField(choices=[(item.pk, item) for item in Category.objects.all()])
    # subcategory = forms.ChoiceField(choices=[(item.pk, item) for item in Subcategory.objects.filter(category)])
    date_fin = forms.DateField(widget=NumberInput(attrs={'type': 'date', 'class': "form-control"}))

    class Meta():
        model = Service
        fields = '__all__'
        exclude = ['user', 'subcategory']

    def __init__(self, *args, **kwargs):
        super(AddService, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': "form-control"})
        self.fields['budget'].widget.attrs.update({'class': "form-control"})
        self.fields['lieu'].widget.attrs.update({'class': "form-control"})

        # self.fields['subcategory'].label = 'La categorie'
        # self.fields['subcategory'].widget.attrs.update({'label': 'sous Categorie', 'class': "form-select"})
        self.fields['description'].widget.attrs.update({'class': "form-control"})

"""


# formulaire pour les images des annonces
class PhotoForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ['image']

    def __init__(self, *args, **kwargs):
        super(PhotoForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'class': "form-control"})


# formulaire pour la mise à jour des annonces
class UpdateAd(forms.ModelForm):
    edit_annonce = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta():
        model = Annonce
        fields = '__all__'
        exclude = ['user', 'subcategory', 'commune']

    def __init__(self, *args, **kwargs):
        super(UpdateAd, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['available'].widget.attrs.update({'class': "form-check-input"})


# formulaire pour la suppression des annonces
class DeleteAd(forms.Form):
    delete_annonce = forms.BooleanField(widget=forms.HiddenInput, initial=True)


# formulaire pour les informations sur telephone
class MyMedia(forms.ModelForm):
    class Meta:
        model = Telephone
        fields = '__all__'
        exclude = ['annonce', 'marque', 'model']

    def __init__(self, *args, **kwargs):
        super(MyMedia, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


# formulaire pour les informations sur immobilier
class MyImobilier(forms.ModelForm):
    class Meta:
        model = Immobilier
        fields = '__all__'
        exclude = ['annonce']

    def __init__(self, *args, **kwargs):
        super(MyImobilier, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


# formulaire pour les informations sur les services d'immobilier
class MyImobilier_plus(forms.ModelForm):
    class Meta:
        model = Immobilier_plus
        fields = '__all__'
        exclude = ['annonce']


# formulaire pour les informations de vehicule
class MyVehicule(forms.ModelForm):
    class Meta:
        model = Vehicule
        fields = '__all__'
        exclude = ['annonce', 'marque', 'modele']

    def __init__(self, *args, **kwargs):
        super(MyVehicule, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


# formulaire pour les commentaires
class MyComment(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = '__all__'
        exclude = ['user', 'gest', 'annonce']
        labels = {'rating': 'Note /5'}

    def __init__(self, *args, **kwargs):
        super(MyComment, self).__init__(*args, **kwargs)
        self.fields['rating'] = forms.IntegerField(max_value=5, min_value=0)
        self.fields['rating'].label = 'Note /5'
        self.fields['rating'].widget.attrs.update({'class': 'Stars'})
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
