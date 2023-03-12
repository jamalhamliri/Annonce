from django import forms
from django.contrib.auth.forms import PasswordChangeForm

from .models import CustomUser, ProAdditional, NormalAdditional, Gest
from django.contrib.auth import authenticate


## normal user form

class NormalUserForm(forms.ModelForm):
    GENDER_CHOICES = (
        ('Homme', 'Homme'),
        ('Femme', 'Femme'),
    )
    password1 = forms.CharField(widget=forms.PasswordInput(), help_text="password")
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect())

    def clean_gender(self):

        return self.cleaned_data['gender']

    class Meta():
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'gender', 'about', 'image', 'address', 'phone', 'date_of_birth',
                  'password1', 'password2']

    #
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):

        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class ProUserForm(forms.ModelForm):
    class Meta():
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'gender', 'about', 'address', 'phone', 'date_of_birth']


class ProUserFormAdd(forms.ModelForm):
    class Meta():
        model = ProAdditional
        fields = ['numero_ent', 'nom_ent', 'categorie', 'justification', 'address']


class Noraml(forms.ModelForm):
    class Meta():
        model = NormalAdditional
        fields = '__all__'


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Désolé, cette connexion n'était pas valide. Veuillez réessayer.")
        return self.cleaned_data

    def login(self, request):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(request, email=email, password=password)
        return user


class Update_user(forms.ModelForm):
    class Meta():
        model = CustomUser
        fields = ['first_name', 'last_name', 'image', 'email', 'phone', 'address', 'date_of_birth']

    def __init__(self, *args, **kwargs):
        super(Update_user, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': "form-control"})
        self.fields['last_name'].widget.attrs.update({'class': "form-control"})
        self.fields['image'].widget.attrs.update({'class': "form-control-file d-inline"})
        self.fields['email'].widget.attrs.update({'class': "form-control"})
        self.fields['phone'].widget.attrs.update({'class': "form-control"})
        self.fields['address'].widget.attrs.update({'class': "form-control"})
        self.fields['date_of_birth'].widget.attrs.update({'class': "form-control"})


class MyGest(forms.ModelForm):
    class Meta:
        model = Gest

        fields = ['first_name', 'last_name', 'email', 'numero']

    def __init__(self, *args, **kwargs):
        super(MyGest, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
