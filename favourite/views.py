from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.context_processors import request
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.list import ListView

from . import forms
from .models import FavouriteAnnonce
from annonces.models import Annonce, Images


# fonction pour afficher mes favourites
@login_required(login_url='/login')
def Favourite_Annonce(request):
    favourite = FavouriteAnnonce.objects.filter(user=request.user, is_favourite=True)
    photos = Images.objects.all()
    return render(request, 'annonces/favourite/mes_favourites.html', {'favourite': favourite, 'photos': photos})


# fonction pour ajouter une annonce
@csrf_exempt
def markFavourtie(request, id):
    annonce = get_object_or_404(Annonce, id=id)
    favourite = FavouriteAnnonce(annonce=annonce, user=request.user)
    favourite.save()
    return redirect('main_app:home')


# fonction pour supprimer une favourite
def delete_favourite(request, favourite_id):
    favourite = get_object_or_404(FavouriteAnnonce, id=favourite_id)
    delete_form = forms.Delete_favourite()
    if request.method == 'POST':
        delete_form = forms.Delete_favourite(request.POST)
        if delete_form.is_valid():
            favourite.delete()
            return redirect('main_app:favourite-annonces')
    context = {
        'delete_form': delete_form,
    }
    return render(request, 'annonces/favourite/deletefavourite.html', context)
