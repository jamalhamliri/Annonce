from datetime import datetime
from typing import Dict, Union, Any

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
#from django.contrib.gis.geos import Point
from django.core.paginator import Paginator
from django.db.models import Q
from django.forms import formset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from chat.models import Conversation, Message
from favourite.models import FavouriteAnnonce
from .forms import *
# from .models import *
from . import forms, models
from .models import Commune
from users.forms import MyGest


# Create your views here.
@login_required(login_url='/login')
def createad(request):
    return render(request, 'annonces/add/ajouterAd.html')


# ajouter un annonce
@login_required(login_url='/login')
def createad_ad(request):
    form = AddAd()
    category = MyCategory()
    wilaya = Wilaya()
    photo=PhotoForm()
    PhotoFormSet = formset_factory(PhotoForm, extra=4)
    formset = PhotoFormSet()
    if request.method == 'POST':
        form = AddAd(request.POST)
        photo = PhotoForm(request.POST, request.FILES)
        formset = PhotoFormSet(request.POST, request.FILES)
        category = get_object_or_404(models.Category, id=request.POST['category'])
        subcategory = get_object_or_404(models.Subcategory, id=request.POST['subcategory'])
        if any([form.is_valid(), formset.is_valid()]):
            # ici les droites pour un utilisateur normal
            if request.user.type == "Normal":
                if category.name == "Made in Bladi" or category.name == "Ecole" or category.name == "Voyage" or subcategory.name == "Immobilier neuf":
                    messages.error(request, "Excusez-moi, il semble que pour ajouter ce type d'annonce, vous devez "
                                            "être un utilisateur professionnel. Veuillez noter que seuls les "
                                            "utilisateurs professionnels ont la permission de publier ce type "
                                            "d'annonce.")
                    return redirect('main_app:ajouter-annonce')
                else:
                    annonce = form.save(commit=False)
                    annonce.user = request.user
                    annonce.subcategory_id = request.POST['subcategory']
                    annonce.commune_id = request.POST['commune']
                    print(request.user.type)
                    annonce.save()
                    photo=photo.save(commit=False)
                    photo.annonce_id = annonce.id
                    photo.save()

                    for formp in formset:
                        if formp.cleaned_data:
                            images = formp.save(commit=False)
                            images.annonce_id = annonce.id
                            images.save()
                    if category.name == 'Telephone':
                        annonce_id = annonce.id
                        return HttpResponseRedirect('media/' + str(annonce_id))
                    elif category.name == 'Immobilier':
                        annonce_id = annonce.id
                        return HttpResponseRedirect('immobile/' + str(annonce_id))
                    elif category.name == 'Vehicule':
                        annonce_id = annonce.id
                        return HttpResponseRedirect('vehicule/' + str(annonce_id))
                    else:
                        return redirect('/')
            elif request.user.type == "Pro":
                annonce = form.save(commit=False)
                annonce.user = request.user
                annonce.subcategory_id = request.POST['subcategory']
                annonce.commune_id = request.POST['commune']
                annonce.save()
                photo = photo.save(commit=False)
                photo.annonce_id = annonce.id
                photo.save()
                for formp in formset:
                    if formp.cleaned_data:
                        images = formp.save(commit=False)
                        images.annonce_id = annonce.id
                        images.save()
                if category.name == 'Telephone':
                    annonce_id = annonce.id
                    return HttpResponseRedirect('media/' + str(annonce_id))
                elif category.name == 'Immobilier':
                    annonce_id = annonce.id
                    return HttpResponseRedirect('immobile/' + str(annonce_id))
                elif category.name == 'Vehicule':
                    annonce_id = annonce.id
                    return HttpResponseRedirect('vehicule/' + str(annonce_id))
                elif category.name == 'Voyage':
                    annonce_id = annonce.id
                    return HttpResponseRedirect('voyage/' + str(annonce_id))
                else:
                    return redirect('/')
    ctx = {
        "form": form,
        "photo_form": formset, "category": category, "wilaya": wilaya,'photo':photo

    }
    return render(request, 'annonces/add/ajouterAnnonce.html', ctx)


# ajouter des donnees supplimentaires pour la categorie telephone
def media(request, annonce_id):
    fmedia = MyMedia()
    media_marque = MyMedia_marque()
    if request.method == 'POST':
        fmedia = MyMedia(request.POST)
        print(request.POST)
        if fmedia.is_valid():
            media = fmedia.save(commit=False)
            media.annonce_id = annonce_id
            media.marque_id = request.POST['marque']
            media.model_id = request.POST['media_model']
            media.save()
            return redirect('/')

    ctx = {
        'fmedia': fmedia, 'media_marque': media_marque

    }
    return render(request, 'annonces/add/MyMedia.html', ctx)


# ajoutement des donnees supplimentaires pour categorie vehicule
def Vehicule(request, annonce_id):
    Vehic = MyVehicule()
    vehicule_marque = MyVehicule_marque()
    if request.method == 'POST':
        Vehic = MyVehicule(request.POST)
        if Vehic.is_valid():
            vh = Vehic.save(commit=False)
            vh.annonce_id = annonce_id
            vh.marque_id = request.POST['marque']
            vh.modele_id = request.POST['vehicule_model']
            vh.save()
            return redirect('/')
    ctx = {
        'vehic': Vehic, 'vehicule_marque': vehicule_marque
    }
    return render(request, 'annonces/add/Vehicule.html', ctx)


# ajoutement des donnees supplimentaire pour categorie immobilier
def Immobilier(request, annonce_id):
    form_plus = MyImobilier_plus()
    if request.method == 'POST':
        chambre = request.POST['chambre']
        salle_bain = request.POST['salle_bain']
        etage = request.POST['etage']
        age = request.POST['age']
        surface = request.POST['surface']
        frais_syndiq = request.POST['frais_syndiq']
        lat = request.POST['lat']
        lng = request.POST['lng']
        #coordinates = Point(float(lng), float(lat))
        place = Place(annonce_id=annonce_id, lat=lat, lng=lng)
        place.save()
        immob1 = models.Immobilier(annonce_id=annonce_id, salle_bain=salle_bain, chambres=chambre, etage=etage,
                                   surface=surface,
                                   age=age, frais_syndic=frais_syndiq)
        immob1.save()
        form_plus = MyImobilier_plus(request.POST)
        if form_plus.is_valid():
            plus = form_plus.save(commit=False)
            plus.annonce_id = annonce_id
            plus.save()
            return redirect('/')
    return render(request, 'annonces/add/Immobile.html', {'form_plus': form_plus})


# ajoutement des donnees supplimentaire pour la categorie voyage
def createad_travel(request, annonce_id):
    form = AddTravel()
    if request.method == 'POST':
        form = AddTravel(request.POST)
        # print(request.POST)
        if form.is_valid():
            travel = form.save(commit=False)
            travel.user = request.user
            travel.annonce_id = annonce_id
            # print(travel.user)
            # print(travel.annonce_id)
            travel.save()
            return redirect('/')
    ctx = {
        "form": form,
    }
    return render(request, 'annonces/add/ajouterVoyage.html', ctx)


# affichement des sous donnees pour categorie,telephone,vehicule,commune
def sous_categories(request, category_id):
    sous_categories = Subcategory.objects.filter(category=category_id)
    return render(request, 'petite_annonce/elements/subcategory.html', {'subcategorys': sous_categories})


def media_model(request, telephone_marque_id):
    media_models = models.Telephone_Model.objects.filter(marque=telephone_marque_id)
    return render(request, 'petite_annonce/elements/media_model.html', {'media_models': media_models})


def vehicule_Model(request, vehicule_marque_id):
    vehicule_models = models.Vehicle_Modele.objects.filter(Marque=vehicule_marque_id)
    return render(request, 'petite_annonce/elements/media_model.html', {'media_models': vehicule_models})


def commune(request, commune_id):
    communes = Commune.objects.filter(wilaya_id=commune_id)
    return render(request, 'petite_annonce/elements/subcategory.html', {'communes': communes})


"""def createad_service(request):
    form = AddService(request.POST)
    photo_form = PhotoForm(request.POST)
    category = MyCategory()
    if request.method == 'POST':
        form = AddAd(request.POST)
        photo_form = PhotoForm(request.POST, request.FILES)
        if any([form.is_valid(), photo_form.is_valid()]):
            annonce = form.save(commit=False)
            annonce.user = request.user
            annonce.save()
            images = photo_form.save(commit=False)
            images.annonce_id = annonce
            images.save()
            return redirect('/')
    ctx = {
        "form": form,
        "photo_form": photo_form, "category": category,

    }
    return render(request, 'annonces/add/ajouterService.html', ctx)"""


# la mise a jour des annonces
def updatead(request, annonce_id):
    annonce = get_object_or_404(models.Annonce, id=annonce_id)
    photos = models.Images.objects.filter(annonce=annonce.id)
    imobs = models.Immobilier.objects.filter(annonce_id=annonce.id)
    voyage = models.Voyage.objects.filter(annonce_id=annonce.id)
    comts = models.Commentaire.objects.filter(annonce_id=annonce.id)
    points = models.Place.objects.filter(annonce_id=annonce.id)
    plus = models.Immobilier_plus.objects.filter(annonce_id=annonce.id)
    category = annonce.subcategory.category.name
    # print(category)
    if category == 'Vehicule':
        autos = get_object_or_404(models.Vehicule, annonce_id=annonce_id)
        edit_form = forms.UpdateAd(instance=annonce)
        edit_vehicule = MyVehicule(instance=autos)
        if request.method == 'POST':
            edit_form = forms.UpdateAd(request.POST, instance=annonce)
            edit_vehicule = MyVehicule(request.POST, instance=autos)
            if any([edit_form.is_valid(), edit_vehicule.is_valid()]):
                edit_form.save()
                edit_vehicule.save()
                return redirect('main_app:mes_annonces')
        context = {
            'edit_form': edit_form, 'edit_vehicule': edit_vehicule

        }
    elif category == 'Telephone':
        medias = get_object_or_404(models.Telephone, annonce_id=annonce_id)
        edit_form = forms.UpdateAd(instance=annonce)
        edit_media = MyMedia(instance=medias)
        if request.method == 'POST':
            edit_form = forms.UpdateAd(request.POST, instance=annonce)
            edit_media = MyMedia(request.POST, instance=medias)
            if any([edit_form.is_valid(), edit_media.is_valid()]):
                edit_form.save()
                edit_media.save()
                return redirect('main_app:mes_annonces')
        context = {
            'edit_form': edit_form, 'edit_media': edit_media

        }
    elif category == 'Immobilier':
        imobs = get_object_or_404(models.Immobilier, annonce_id=annonce_id)
        imobs_plus = get_object_or_404(models.Immobilier_plus, annonce_id=annonce_id)
        edit_form = forms.UpdateAd(instance=annonce)
        edit_imobs = MyImobilier(instance=imobs)
        edit_imobs_plus = MyImobilier_plus(instance=imobs_plus)
        if request.method == 'POST':
            edit_form = forms.UpdateAd(request.POST, instance=annonce)
            edit_imobs = MyImobilier(request.POST, instance=imobs)
            edit_imobs_plus = MyImobilier_plus(request.POST, instance=imobs_plus)
            if any([edit_form.is_valid(), edit_imobs.is_valid(), edit_imobs_plus.is_valid()]):
                edit_form.save()
                edit_imobs.save()
                edit_imobs_plus.save()
                return redirect('main_app:mes_annonces')
        context = {
            'edit_form': edit_form, 'edit_imobs': edit_imobs, 'edit_imobs_plus': edit_imobs_plus

        }
    elif category == 'Voyage':
        travel = get_object_or_404(models.Voyage, annonce_id=annonce_id)
        edit_form = forms.UpdateAd(instance=annonce)
        edit_travel = AddTravel(instance=travel)
        if request.method == 'POST':
            edit_form = forms.UpdateAd(request.POST, instance=annonce)
            edit_travel = AddTravel(request.POST, instance=travel)
            if any([edit_form.is_valid(), edit_travel.is_valid()]):
                edit_form.save()
                edit_travel.save()
                return redirect('main_app:mes_annonces')
        context = {
            'edit_form': edit_form, 'edit_travel': edit_travel

        }
    else:
        edit_form = forms.UpdateAd(instance=annonce)
        if request.method == 'POST':
            edit_form = forms.UpdateAd(request.POST, instance=annonce)
            if any([edit_form.is_valid()]):
                edit_form.save()

                return redirect('main_app:mes_annonces')
        context = {
            'edit_form': edit_form

        }
    return render(request, 'annonces/update/updateAnnonce.html', context=context)


# la suppression des annonces
def deletead(request, annonce_id):
    annonce = get_object_or_404(models.Annonce, id=annonce_id)
    delete_form = forms.DeleteAd()
    if request.method == 'POST':
        delete_form = forms.DeleteAd(request.POST)
        if delete_form.is_valid():
            # photos.delete()
            annonce.delete()
            return redirect('main_app:mes_annonces')
    context = {
        'delete_form': delete_form,
    }
    return render(request, 'annonces/deleteAnnonce.html', context)


# la page home
def home(request):
    photos = models.Images.objects.all()
    annonces = models.Annonce.objects.all().order_by('-created')
    category = Category.objects.all()
    subcategory = Subcategory.objects.all()
    commune = Commune.objects.all()
    rating = Commentaire.objects.all()
    date = datetime.now()
    top=models.Top_category.objects.all()
    list = [0, 0]
    context = {
        "category": category, "subcategory": subcategory,
        "commune": commune, 'photos': photos, 'annonces': annonces, 'date': date, 'commentery': rating, 'top': top}
    if request.user.is_authenticated:
        conv = Conversation.objects.filter(
            Q(user1=request.user) | Q(user2=request.user))
        for cnv in conv:
            msg = Message.objects.filter(
                Q(conversation_id=cnv.id) & Q(seen=False)).exclude(sender_user=request.user)
            context.update({'msg':msg})
        return render(request, 'annonces/home.html', context)
    return render(request, 'annonces/home.html', context)


# la fonction de recherche
def search(request):
    photos = models.Images.objects.all()
    annonces = models.Annonce.objects.all().order_by('-created')
    category = Category.objects.all()
    subcategory = Subcategory.objects.all()
    commune = Commune.objects.all()
    date = datetime.now()
    context = {
        "category": category, "subcategory": subcategory,
        "commune": commune, 'photos': photos, 'annonces': annonces, 'date': date}
    print(request.POST)
    if request.method == 'POST':
        subcategory = request.POST['sub']
        commune = request.POST['commune']
        rechercher = request.POST['rechercher']
        type = request.POST['type']
        min = request.POST['min']
        max = request.POST['max']
        # sub = models.Subcategory.objects.get(name=subcategory)
        """search = models.Annonce.objects.filter(
            Q(name=rechercher) | Q(subcategory=sub.id) | Q(commune=commune) | Q(type=type))
        return render(request, 'annonces/RechercherAnnonce.html',
                      {'rechercher': rechercher, 'search': search, 'date': date})"""

        if subcategory == "" and rechercher == "" and commune != "":  # verifie1
            print(commune)
            comm = models.Commune.objects.get(id=commune)
            search = models.Annonce.objects.filter(
                Q(commune=commune) & Q(type=type) & Q(price__range=(min, max))).order_by('-created')
            """paginator = Paginator(search, 6)
            page_number = request.GET.get('page')
            search = paginator.get_page(page_number)"""
            context.update({'commune_name': comm, 'search': search})
            # print(context)
            return render(request, 'annonces/RechercherAnnonce.html', context)
        elif commune == "" and rechercher == "" and subcategory != "":  # verifie2
            sub = models.Subcategory.objects.get(name=subcategory)
            search = models.Annonce.objects.filter(
                Q(subcategory=sub.id) & Q(type=type) & Q(price__range=(min, max))).order_by('-created')
            context.update({'subcategory_name': subcategory, 'search': search})
            return render(request, 'annonces/RechercherAnnonce.html', context)
        elif commune != "" and rechercher == "" and subcategory != "":  # verifie3
            comm = models.Commune.objects.get(id=commune)
            sub = models.Subcategory.objects.get(name=subcategory)
            search = models.Annonce.objects.filter(Q(commune=commune) &
                                                   Q(subcategory=sub.id) & Q(type=type) & Q(
                price__range=(min, max))).order_by('-created')
            context.update({'subcategory_name': subcategory, 'commune_name': comm, 'search': search})
            return render(request, 'annonces/RechercherAnnonce.html', context)
        elif subcategory == "" and commune == "" and rechercher != "":  # verifie4

            search = models.Annonce.objects.filter(
                Q(name=rechercher) & Q(type=type) & Q(price__range=(min, max))).order_by('-created')
            print(search)
            context.update({'rechercher': rechercher, 'search': search})
            return render(request, 'annonces/RechercherAnnonce.html', context)
        elif subcategory != "" and commune == "" and rechercher != "":  # verifie7
            sub = models.Subcategory.objects.get(name=subcategory)
            search = models.Annonce.objects.filter(
                Q(name=rechercher) & Q(subcategory=sub.id) & Q(type=type) & Q(price__range=(min, max))).order_by(
                '-created')
            context.update({'subcategory_name': subcategory, 'rechercher': rechercher, 'search': search})
            return render(request, 'annonces/RechercherAnnonce.html', context)
        elif subcategory == "" and commune != "" and rechercher != "":  # verifie8
            comm = models.Commune.objects.get(id=commune)
            search = models.Annonce.objects.filter(Q(commune=commune) &
                                                   Q(name=rechercher) & Q(type=type) & Q(
                price__range=(min, max))).order_by('-created')
            print(search)
            context.update({'commune_name': comm, 'rechercher': rechercher, 'search': search})
            return render(request, 'annonces/RechercherAnnonce.html', context)
        elif subcategory == "" and rechercher == "" and commune == "":  # verifie5
            return redirect('/')
        else:  # verifie6
            sub = models.Subcategory.objects.get(name=subcategory)
            comm = models.Commune.objects.get(id=commune)
            search = models.Annonce.objects.filter(
                Q(name=rechercher) & Q(subcategory=sub.id) & Q(commune=commune) & Q(type=type) & Q(
                    price__range=(min, max))).order_by('-created')
            context.update(
                {'subcategory_name': subcategory, 'commune_name': comm, 'rechercher': rechercher, 'search': search})
            return render(request, 'annonces/RechercherAnnonce.html', context)
    return render(request, 'annonces/RechercherAnnonce.html', context)


# function qui affiche les annonces d'utilisateur
def mes_annonces(request):
    annonces = models.Annonce.objects.filter(user=request.user)
    photos = models.Images.objects.all()
    return render(request, 'annonces/mesAnnonces.html', {'annonces': annonces, 'photos': photos})


# function qui affiche un annonce
def view_annonce(request, annonce_id):
    annonce = get_object_or_404(models.Annonce, id=annonce_id)
    photos = models.Images.objects.filter(annonce=annonce.id)
    medias = models.Telephone.objects.filter(annonce_id=annonce.id)
    imobs = models.Immobilier.objects.filter(annonce_id=annonce.id)
    autos = models.Vehicule.objects.filter(annonce_id=annonce.id)
    voyage = models.Voyage.objects.filter(annonce_id=annonce.id)
    comts = models.Commentaire.objects.filter(annonce_id=annonce.id)
    points = models.Place.objects.filter(annonce_id=annonce.id)
    plus = models.Immobilier_plus.objects.filter(annonce_id=annonce.id)
    form_gest = MyGest()
    form_com = forms.MyComment()
    ctx = {'annonce': annonce, 'photos': photos, 'medias': medias, 'imobs': imobs, 'autos': autos, 'comts': comts,
           'form_com': form_com, 'voyage': voyage,
           'form_gest': form_gest, 'points': points, 'form_plus': plus}
    if request.method == 'POST':
        if request.user.is_authenticated:
            form_com = forms.MyComment(request.POST)
            if form_com.is_valid():
                comt = form_com.save(commit=False)
                comt.user = request.user
                comt.annonce_id = annonce_id
                comt.save()

                return HttpResponseRedirect(str(annonce_id))
        else:
            form_gest = MyGest(request.POST)
            form_com = forms.MyComment(request.POST)
            if all([form_gest.is_valid(), form_com.is_valid()]):
                gest = form_gest.save(commit=False)
                # annonce.user = request.user
                gest.save()
                comt = form_com.save(commit=False)
                comt.gest = gest
                comt.annonce_id = annonce_id
                comt.save()
                return HttpResponseRedirect(str(annonce_id))

    return render(request, 'annonces/view/view_annonce.html', ctx)


# function qui affiche tout les annonces pour un utilisateur specifique
def see_annonce(request, user_id):
    annonce = models.Annonce.objects.filter(user_id=user_id)
    photos = models.Images.objects.all()
    category = Category.objects.all()
    commune = Commune.objects.all()
    date = datetime.now()
    context = {
        "category": category,
        "commune": commune, 'photos': photos, 'annonce': annonce, 'date': date}
    return render(request, 'annonces/view/see_annonce.html', context)


"""def search_annonce(request):
    category = Category.objects.all()
    subcategory = Subcategory.objects.all()
    commune = Commune.objects.all()

    context = {
        "category": category, "subcategory": subcategory,
        "commune": commune
    }

    return render(request, 'petite_annonce/elements/search.html', context)"""


# fonction pour afficher les donnees pour chaque sous categorie
def show_category(request, category_id):
    # subcategory = get_object_or_404(models.Subcategory, category=category_id)
    annonce = models.Annonce.objects.filter(subcategory=category_id)
    photos = models.Images.objects.all()
    category = Category.objects.all()

    commune = Commune.objects.all()
    date = datetime.now()
    context = {
        "category": category,
        "commune": commune, 'photos': photos, 'annonce': annonce, 'date': date}
    return render(request, 'annonces/show_categories.html', context)
