from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.urls import path, reverse_lazy, include, re_path
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordChangeView, PasswordChangeDoneView, LoginView, PasswordResetCompleteView

from config import settings
from favourite import views as favourite_views
from main_app import main_views
from users import views as user_views
from annonces import views as annonce_views
from chat import views as chat_views

app_name = 'main_app'

urlpatterns = [
    # index
    path('home/', main_views.index, name="index"),
    path('', annonce_views.home, name="home"),
    # annonce
    path('annonce/', annonce_views.createad, name="ajouter-ad"),

    path('commune/<int:commune_id>/', annonce_views.commune, name='commune'),
    path('annonce/ajouter-add/', annonce_views.createad_ad, name="ajouter-annonce"),

    path('annonce/ajouter-add/media/<int:annonce_id>', annonce_views.media, name='media'),
    path('annonce/ajouter-add/immobile/<int:annonce_id>', annonce_views.Immobilier, name='immobile'),
    path('annonce/ajouter-add/vehicule/<int:annonce_id>', annonce_views.Vehicule, name='vehicule'),
    path('annonce/ajouter-add/voyage/<int:annonce_id>', annonce_views.createad_travel, name="ajouter-voyage"),
    #path('annonce/ajouter-Service/', annonce_views.createad_service, name="ajouter-service"),
    #path('annonce/search/', annonce_views.search_annonce, name="search_annonce"),
    path('annonce/<int:annonce_id>', annonce_views.view_annonce, name='view_annonce'),
    path('profile/mes-annonces', annonce_views.mes_annonces, name='mes_annonces'),
    path('delete/<int:annonce_id>', annonce_views.deletead, name='delete_annonce'),
    path('profile/mes-annonces/update/<int:annonce_id>/', annonce_views.updatead, name='update_annonce'),
        path('profile/mes-annonces/delete/<int:annonce_id>/', annonce_views.deletead, name='delete_annonce'),
    path('search/', annonce_views.search, name='search'),
    path('annonce/show_categories/<int:category_id>', annonce_views.show_category, name='show_category'),
path('annonce/see_annonces/<int:user_id>', annonce_views.see_annonce, name='see_annonce'),
    #favourite
    path('favourite/', favourite_views.Favourite_Annonce, name='favourite-annonces'),
        path('favourite/mark/<int:id>/', favourite_views.markFavourtie, name='mark-favourite'),
    path('favourite/delete/<int:favourite_id>/', favourite_views.delete_favourite, name='delete_favourite'),

    # chat
    path('chat/', chat_views.chat_index, name='chat_index'),
        path('chat/<int:annonce_id>', chat_views.chat, name='chat'),
        path('chat/<int:annonce_id>/message/<int:conversation_id>', chat_views.message, name='message'),
    path('chat/<int:annonce_id>/message_gest/<int:gest_id>/<int:conversation_id>', chat_views.message_gest, name='message_gest'),
    #sous
    path('sous_categories/<int:category_id>/', annonce_views.sous_categories, name='sous_categories'),
    path('media_model/<int:telephone_marque_id>/', annonce_views.media_model, name='telephone_model'),
    path('vehicule_model/<int:vehicule_marque_id>/', annonce_views.vehicule_Model, name='vehicule_model'),

    # les liens pour l'application utilisateur
    path('login', user_views.login_user, name="login"),
    # Password reset
    path('change-password/', PasswordChangeView.as_view(
        template_name='registration/password_change_form.html', success_url='done'),
         name='password_change'
         ),
    path('change-password/done/', PasswordChangeDoneView.as_view(
        template_name='registration/password_change_done.html'),
         name='password_change_done'
         ),
    path('profile/', user_views.profile_user, name="profile"),
    path('logout/', user_views.logout_user, name="logout"),
    path('registre/', user_views.registre, name="registre"),
    path('registre/normal-user/', user_views.registreNormalUser, name="normal-registre"),
    path('registre/pro-user/', user_views.registreProUser, name="pro-registre"),
    path('activate/<uidb64>/<token>', user_views.activate, name='activate'),
    #reset



]
