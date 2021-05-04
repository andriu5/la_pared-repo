from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from apps.login_registration_app.models import User, Message, Comment
from time import gmtime, strftime, time, localtime
from datetime import datetime, timedelta
    
# Create your views here.
def wall_index(request):
    print('*'*100)
    print('in the wall index...')
    if request.method == "GET":
        if 'nombre_usuario' not in request.session.keys():
            request.session['nombre_usuario'] = ""
            return redirect('index')
        if 'user' in request.session:
            currentUserID = request.session['user']['id']
            print('Current User:', request.session['user']['id'])
            print('Current User:', request.session['user'])
            half_hour_ago = datetime.today() - timedelta(minutes=30)
            context = {
                'user': request.session['nombre_usuario'],
                'allMessages' : Message.objects.all(),
                #'allUsers' : User.objects.all(),
                'allMessages_halfHourAgo' : User.objects.filter(message__created_at__gt=half_hour_ago),
                #'yourMessages' : Message.objects.filter(user=currentUserID),
                # 'otherComments' : Message.objects.get(id=currentUser).comment.all(),
                # 'allComments' : Comment.objects.filter(message__user=User.objects.get(id=currentUserID)).order_by('created_at') or Comment.objects.exclude(message=currentUserID).order_by('created_at'),
                #'allComments' : Comment.objects.filter(message__user=User.objects.get(id=currentUserID)).order_by('created_at')
            }
            return render(request, "wall/index.html", context)

def post_messages(request):
    print('*'*100)
    print('creating message...')
    #Verificar Texto en post_message_validator recibiendo post
    errors = User.objects.post_message_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('index')
    else:
        if request.method == "POST":
            new_message = Message.objects.create(
                message = request.POST['post_message'],
                user = User.objects.get(id=request.session['user']['id'])
            )
            new_message.save()
            messages.success(request,"Message successfully registered!")
            print("Agregando mensaje a la base de datos: ",new_message.message ,", al usuario: ", new_message.user) 
            return redirect("wall_index")


def post_comments(request,id):
    print('*'*100)
    print('posting comment...')
    print("Request", request)
    print(request.POST)
    print("Message-ID: ", id)

    #Verificar Texto en post_comment_validator recibiendo post
    errors = User.objects.post_comment_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('wall_index')
    else:
        if request.method == "POST":
            new_comment = Comment.objects.create(
                comment = request.POST['post_comment'],
                user = User.objects.get(id=request.session['user']['id']),
                message = Message.objects.get(id=id)
            )
            new_comment.save()
            print("Info: Nuevo Comentario agregado a la base de datos.\n Comentario:",new_comment.comment, ", user:", new_comment.user,", messages:", new_comment.message)
            return redirect("wall_index")

def delete_message(request, id):
    print('*'*100)
    print('Deleting a Message...')
    print("Request", request)
    print(request.POST)
    print("Message-ID: ", id)
    errors = User.objects.message_validator(request.POST)
    print("Errors: ", errors)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('wall_index')
    else:
        if request.method == "POST":
            msgDeleted = Message.objects.get(id=id)
            print("Info: Mensaje borrado de la base de datos.\n Mensaje:",msgDeleted.message)
            messages.success(request,f"Info: The Message '{msgDeleted.message}' was successfully deleted from the Data Base!")
            msgDeleted.delete()
            return redirect('wall_index')

def logout(request):
    print('*'*100)
    print('Clearing session and returning to login...')
    for key in request.session.keys(): # Imprimimos todas las claves de la session antes de borrar
        print("session key: ",key)
        print("session key type(): ",type(key))
    request.session.clear() # borramos todas las claves de la session
    return redirect("index") # go to root: "/"