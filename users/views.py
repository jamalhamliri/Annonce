from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.views.generic import TemplateView

from .Tokens import account_activation_token
from .forms import *
from django.http import HttpResponse
from django.contrib.auth import login, logout, update_session_auth_hash, get_user_model
from django.contrib import messages
from django.http import HttpResponseRedirect
from .decorators import user_not_authenticated
from .Tokens import account_activation_token


# activation de compte a travers email
def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('main_app:home')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('main_app:home')


# l'envoie de l'email a l'utilsateur de l'activation
def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("registration/template_activate_account.html", {
        'user': user.email,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')


# fonction login
def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.login(request.POST)
            if user is not None and user.is_active:
                login(request, user)
                messages.success(request, f'Login Success.')
                next_url = request.GET.get('next')
                if next_url:
                    return HttpResponseRedirect(next_url)
                else:
                    return redirect('main_app:home')
            else:
                messages.warning(request, "le compte n'est pas active Veuillez vérifier ton e-mail pour l'active")
        else:
            messages.warning(request, "Le formulaire n'est pas valide! Veuillez vérifier l'e-mail et le mot de passe "
                                      "or le compte n'est pas active Veuillez vérifier ton e-mail pour l'active")
            return render(request, 'registration/login.html', context={'form': form})
    else:
        if request.user.is_authenticated:
            return redirect('main_app:home')
        form = LoginForm()
    return render(request, 'registration/login.html', context={'form': form})


@user_not_authenticated
def registre(request):
    return render(request, 'registration/registre.html')


# fonction d'inscreption pour un utilisateur normal
@user_not_authenticated
def registreNormalUser(request):
    Normal = NormalAdditional()
    if request.method == "POST":
        form = NormalUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            Normal.user = user
            Normal.save()
            messages.success(request, 'add valid')
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('main_app:login')
        else:
            messages.warning(request, 'Form is not valid')
            return render(request, 'registration/normalSignUp.html', {'form': form})
    form = NormalUserForm()
    context = {
        'form': form
    }
    return render(request, 'registration/normalSignUp.html', context)


# fonction d'inscreption pour un utilisateur pro
@user_not_authenticated
def registreProUser(request):
    form = NormalUserForm()
    formadd = ProUserFormAdd()
    print(request.POST)
    if request.method == 'POST':
        form = NormalUserForm(request.POST, request.FILES)
        formadd = ProUserFormAdd(request.POST)
        if all([form.is_valid(), formadd.is_valid()]):
            User = form.save(commit=False)
            User.type = 'Pro'
            User.is_active = False
            form.save()
            Pro = formadd.save(commit=False)
            Pro.user = User
            Pro.save()
            messages.success(request, 'add valid')
            activateEmail(request, User, form.cleaned_data.get('email'))
            return redirect('main_app:login')
        else:
            messages.warning(request, 'Form is not valid')
            return render(request, 'registration/ProSignUp.html', {'form': form, 'formadd': formadd})

    context = {
        'form': form,
        'formadd': formadd
    }
    return render(request, 'registration/ProSignUp.html', context)


# fonction deconnecter
def logout_user(request):
    logout(request)
    messages.success(request, 'Logout Successfully')
    return redirect('main_app:home')


# la fonction pour la mise a jour des donnees d'utilisateur
@login_required(login_url='/login')
def profile_user(request):
    form = Update_user(instance=request.user)
    if request.method == 'POST':
        form = Update_user(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'change valid')
            return redirect('/profile')
        else:
            messages.warning(request, 'Form is not valid')
            return redirect('/profile')
    return render(request, 'registration/profile.html', context={'form': form})
