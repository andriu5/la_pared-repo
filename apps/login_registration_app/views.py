from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt
from time import gmtime, strftime, time, localtime
from datetime import datetime
from .next_birthday import calculate_days_left_for_next_birthday
from django.http import JsonResponse

# Create your views here.
def index(request):
    if request.method == "GET":
        if 'nombre_usuario' not in request.session.keys():
            request.session['nombre_usuario'] = ""
        if 'dias_restantes_para_cumple_del_usuario' not in request.session.keys():
            request.session['dias_restantes_para_cumple_del_usuario'] = 0
        context = {
            "strftime": strftime("%Y-%m-%d %H:%M %p", gmtime()), # python siempre maneja YYYY-MM-DD
            "gmtime": gmtime(),
            "time": time(),
            "localtime": localtime(),
            "strfTime2": strftime("%Y-%m-%d %H:%M %p"),
            "datetime": datetime.now()
        }
    return render(request, "index.html", context)

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('index')
    else:
        if request.method == "POST":
            #Verificar Email!
            if User.objects.filter(email=request.POST['email']).exists():
                messages.add_message(request, messages.ERROR, f"Error: email '{request.POST['email']}' is already taken!")
                return redirect('index')
            else:
                password = request.POST['password']
                pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  # create the hash
                print(pw_hash)      # imprime algo como b'$2b$12$sqjyok5RQccl9S6eFLhEPuaRaJCcH3Esl2RWLm/cimMIEnhnLb7iC' 
                new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash, birthday=request.POST['birthday'])
                print(f"Info: Nuevo Usuario agregado a la base de datos.\n Nombre: {new_user.first_name} {new_user.last_name} | Email: {new_user.email} | Fecha de Cumpleaños: {new_user.birthday}")
                messages.success(request,"Successfully registered!")
                # Iniciamos la sesion del usuario y aprovechandonos que estamos validando los emails, podemos hacer lo siguiente:
                email_usuario = request.POST['email']
                print(email_usuario)
                # aqui da lo mismo que tengamos personas con nombres iguales, 
                # por que sacamos el ID del email que fue previamente validado y luego obtenemos el nombre del usuario!
                nombre_usuario = User.objects.get(email=email_usuario).first_name
                print("El Nombre del Usuario es:", nombre_usuario) 
                
                print(type(new_user.birthday)) # string!
                print(new_user.birthday[0])  # string!

                fechaNacimientoUsuario = {
                    "year": new_user.birthday[0:4],
                    "month": new_user.birthday[5:7],
                    "day": new_user.birthday[8:10]
                }
                print(fechaNacimientoUsuario)

                request.session['dias_restantes_para_cumple_del_usuario'] = calculate_days_left_for_next_birthday(**fechaNacimientoUsuario)

                request.session['nombre_usuario'] = nombre_usuario
                return redirect("success") # nunca renderizar en una publicación, ¡siempre redirigir!

def success(request):
    if request.method == "GET":
        # Happy birthday
        if request.session['dias_restantes_para_cumple_del_usuario'] == 0:
            request.session['dias_restantes_para_cumple_del_usuario'] = True
            #messages.add_message(request, messages.INFO, f"Happy Birthday!!")
        return render(request, "success.html")

def login(request):
    # ver si el nombre de usuario proporcionado existe en la base de datos
    user = User.objects.filter(email=request.POST['email']) # ¿Por qué usamos el filtro aquí en lugar de get?
    if user: # tenga en cuenta que aquí aprovechamos la veracidad: una lista vacía devolverá falso
        logged_user = user[0] 
        # asumiendo tenemos un usuario con este nombre de usuario, éste sería el primero en la lista que obtenemos
        # por supuesto, deberíamos tener cierta lógica para evitar duplicados de nombres cuando creamos usuarios
        # usa el método check_password_hash de bcrypt, pasando el hash de nuestra base de datos y la contraseña del formulario
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
        # si obtenemos True después de validar la contraseña, podemos poner la identificación del usuario en la sesión
            request.session['userid'] = logged_user.id
            # ¡Nunca renderices en una publicación, siempre redirigir!
            messages.success(request,"Successfully logged in!")
            return redirect('success')
    # si no encontramos nada en la base de datos buscando por nombre de usuario o si las contraseñas no coinciden, 
    # redirigir a una ruta segura
    return redirect('index')

def logout(request):
    for key in request.session.keys(): # Imprimimos todas las claves de la session antes de borrar
        print("session key: ",key)
        print("session key type(): ",type(key))
    request.session.clear() # borramos todas las claves de la session
    return redirect("index") # go to root: "/"

def verificar_email(request):
    if request.method == "POST":
        email = request.POST['email']
        print("Email:", email)
        if User.objects.filter(email=request.POST['email']).exists():
            # Valimos que no exista 
            # Guardamos los datos en la base de datos
            print("Imprimiendo desde Verificar Email!")
            # return HttpResponse( f"Error: email '{email}' is already in the data base!")\
            return JsonResponse({"errors":  f"Error: email '{email}' is already in the data base!"})
        else:
            return JsonResponse({"errors":  "True"})