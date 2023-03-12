import uuid

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from chat.forms import *
from annonces.models import Annonce
from users.Tokens import account_activation_token
from users.forms import Gest, MyGest
from chat import *

"""def chat(request, annonce_id):
    annonce = get_object_or_404(Annonce, id=annonce_id)
    discussion_user = models.Conversation.objects.filter(annonce=annonce.id, user1=request.user)
    discussion_annonce = models.Conversation.objects.filter(annonce=annonce.id, user2=annonce.user)
    gest = MyGest()
    if request.method == 'POST':
        annonce = get_object_or_404(Annonce, id=annonce_id)
        print(request.POST)
        print(request.user)
        gest = MyGest(request.POST)
        print(request.user.is_authenticated)
        if request.user.is_authenticated:
            chat = Conversation(user1=request.user, user2=annonce.user, contenu=request.POST['contenu'],
                                annonce=annonce)
            chat.save()
        else:

            pass

    return render(request, 'chat/chat.html', {'annonce': annonce, 'gest': gest, 'discussion_user': discussion_user,
                                              'discussion_annonce': discussion_annonce})"""


def sendchatEmail(request, gest, Con):
    mail_subject = "le lien de discussion."
    message = render_to_string("chat/lienchat.html", {
        'gest': gest,
        'user': Con.user2,
        'gest_id':gest.id,
        'conversation_id':Con.id,
        'domain': get_current_site(request).domain,
        'annonce_id': Con.annonce.id,
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[gest.email])
    if email.send():
        messages.success(request, f'Dear {gest}, vous allez trouver le lien de  cette discussion dasn votre boite email.')
    else:
        messages.error(request, f'Problem sending email to {gest.email}, check if you typed it correctly.')


def chat(request, annonce_id):
    annonce = get_object_or_404(Annonce, id=annonce_id)
    gest = MyGest()
    context = {'annonce': annonce, 'gest': gest}
    if request.method == 'POST':
        if request.user.is_authenticated:
            Con = Conversation(user1=request.user, user2=annonce.user, annonce=annonce)
            Con.save()
            conversation_id = Con.id
            message = Message(conversation_id=conversation_id, contenu=request.POST['contenu'],
                              sender_user=request.user)
            message.save()
            print(Con)
            return HttpResponseRedirect(str(annonce_id) + '/message/' + str(conversation_id))
        else:
            gest = MyGest(request.POST)
            if gest.is_valid():
                gest = gest.save(commit=False)
                gest.save()
                Con = Conversation(gest1=gest, user2=annonce.user, annonce=annonce)
                Con.save()
                conversation_id = Con.id
                gest_id = gest.id
                message = Message(conversation_id=conversation_id, contenu=request.POST['contenu'],
                                  sender_gest=gest)
                message.save()

                print(Con)
                sendchatEmail(request, gest,Con)
                return HttpResponseRedirect(
                    str(annonce_id) + '/message_gest/' + str(gest_id) + '/' + str(conversation_id))

    return render(request, 'chat/chat.html', context)


def message(request, annonce_id, conversation_id):
    annonce = get_object_or_404(Annonce, id=annonce_id)
    Msg = Message.objects.filter(conversation_id=conversation_id)
    context = {'annonce': annonce, 'Msg': Msg}
    if request.method == 'POST':
        token = request.POST['csrfmiddlewaretoken']
        if token in request.session:
            request.session[token] = True
            request.session['csrfmiddlewaretoken'] = uuid.uuid4().hex
            context.update({'csrfmiddlewaretoken': request.session['csrfmiddlewaretoken']})
            return render(request, 'chat/chat.html', context)
        else:
            request.session[token] = True
            request.session['csrfmiddlewaretoken'] = uuid.uuid4().hex
            context.update({'csrfmiddlewaretoken': request.session['csrfmiddlewaretoken']})
            message = Message(conversation_id=conversation_id, contenu=request.POST['contenu'],
                              sender_user=request.user)
            message.save()
            sees=Message.objects.filter(Q(conversation_id=conversation_id) & Q(seen=False)).exclude(sender_user=request.user)
            for see in sees:
                see.seen=True
                see.save()
    return render(request, 'chat/chat.html', context)


def message_gest(request, annonce_id, gest_id, conversation_id):
    annonce = get_object_or_404(Annonce, id=annonce_id)
    Msg = Message.objects.filter(conversation_id=conversation_id)
    context = {'annonce': annonce, 'Msg': Msg, 'gest_id': gest_id}
    if request.method == 'POST':
        print(request.POST)
        token = request.POST['csrfmiddlewaretoken']
        if token in request.session:
            request.session[token] = True
            request.session['csrfmiddlewaretoken'] = uuid.uuid4().hex
            context.update({'csrfmiddlewaretoken': request.session['csrfmiddlewaretoken']})
            return render(request, 'chat/chat_gest.html', context)
        else:
            request.session[token] = True
            request.session['csrfmiddlewaretoken'] = uuid.uuid4().hex
            context.update({'csrfmiddlewaretoken': request.session['csrfmiddlewaretoken']})
            if request.user.is_authenticated:
                message = Message(conversation_id=conversation_id, contenu=request.POST['contenu'],
                                  sender_user=request.user)
                message.save()
            else:
                message = Message(conversation_id=conversation_id, contenu=request.POST['contenu'],
                                  sender_gest_id=gest_id)
                message.save()
    return render(request, 'chat/chat_gest.html', context)


def chat_index(request):
    conversations = Conversation.objects.filter(Q(user2=request.user) | Q(user1=request.user)).order_by('-created')

    context = {'conversations': conversations}
    return render(request, 'chat/conversation.html', context)



