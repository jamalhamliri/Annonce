from django.shortcuts import render
from annonces.models import Category, Commune, Subcategory


# Create your views here.

def index(request):
    category = Category.objects.all()
    subcategory = Subcategory.objects.all()
    commune = Commune.objects.all()
    context = {
     "category" : category,"subcategory" : subcategory,
     "commune" : commune
    }
    return render(request,'petite_annonce/apps/index.html',context)