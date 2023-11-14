from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .models import Profesor, Curso, Estudiante, Avatar
from .forms import ProfesorFormulario, UserRegisterForm, UserEditForm, AvatarFormulario
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
"""
def profe_nuevo(request):
    profeN = Profesor(nombre="Pepe", apellido="Python", email="pepe@python.com", profesion="Biofisico")
    profeN.save()

    return HttpResponse(f"Hemos guardado al profesor {profeN.nombre}")


def curso_nuevo(request):
    mi_curso_favorito = Curso(nombre="Python", comision=47765)
    mi_curso_favorito.save()

    return HttpResponse(f"Bienvenidos al curso {mi_curso_favorito.nombre}")
"""
@login_required
def inicio(request):
    nombre = "Pepe"
    return render(request, "AppCoder/inicio.html", {"name":nombre}) #3er argumento: contexto


@login_required
def ver_entregras(request):
    return render(request, "AppCoder/ver_entregas.html")

@login_required
def ver_estudiante(request):
    return render(request, "AppCoder/ver_estudiantes.html")

def crear_cursos(request):
    if request.method == "POST": #al presionar el botón
        curso_nuevo = Curso(nombre=request.POST["nombre"], comision=request.POST["comision"])
        curso_nuevo.save()
        return render(request, "AppCoder/inicio.html")

    return render(request, "AppCoder/crear_cursos.html")



def buscar_profes(request):

    return render(request, "AppCoder/buscar_profes.html")

def resultado_profes(request):

    if request.GET["apellido"]: #cuando hagamos click al botón y hay datos

        apellido = request.GET["apellido"] #valor que introduje en el cuadrito de búsqueda
        profes_resultado = Profesor.objects.filter(apellido__icontains=apellido) #buscar un match entre los datos que ya tengo

        return render(request, "AppCoder/resultado_profes.html", {"valor":apellido, "res":profes_resultado})

    else: #si hacemos click al botón sin datos!!!!
        return HttpResponse("No enviaste datos.")

    return render(request, "AppCoder/resultado_profes.html")





#HACIENDO EL CRUD de Profes --- CLÁSICO

#Read
@login_required
def ver_profes(request):

    todos = Profesor.objects.all()

    return render(request, "AppCoder/ver_profes.html", {"profes":todos})

#Create
def crear_profes(request):
 
    if request.method == "POST": #hacemos click al botón enviar

        miFormulario = ProfesorFormulario(request.POST) # Aqui me llega la informacion del html 

        if miFormulario.is_valid():
                info = miFormulario.cleaned_data
                profe_nuevo = Profesor(nombre=info["nombre"], apellido=info["apellido"], 
                                    email=info["email"],profesion =info["profesion"])
                profe_nuevo.save()
                return render(request, "AppCoder/inicio.html")
    else:
        miFormulario = ProfesorFormulario() #mostramos formulario vacío

        return render(request, "AppCoder/crear_profes.html", {"form": miFormulario})
    

def eliminar_profesor(request, profesor_nombre):

    profesor_escogido = Profesor.objects.get(nombre=profesor_nombre)
    profesor_escogido.delete()
    todos = Profesor.objects.all()

    return render(request,"AppCoder/ver_profes.html", {"profes":todos} )



def actualizar_profesor(request, profesor_nombre):

    profesor_escogido = Profesor.objects.get(nombre=profesor_nombre)
    
    if request.method == "POST": #hacemos click al botón actualizar

        miFormulario = ProfesorFormulario(request.POST) # Aqui me llega la informacion del html 

        if miFormulario.is_valid():
                
                info = miFormulario.cleaned_data
                
                profesor_escogido.nombre = info["nombre"]
                profesor_escogido.apellido = info["apellido"]
                profesor_escogido.email = info["email"]
                profesor_escogido.profesion = info["profesion"]

                profesor_escogido.save()

                return render(request, "AppCoder/inicio.html")
    else:
        miFormulario = ProfesorFormulario(initial={"nombre":profesor_escogido.nombre,
                                                   "apellido":profesor_escogido.apellido,
                                                   "email":profesor_escogido.email,
                                                   "profesion":profesor_escogido.profesion}) #mostrar formulario con la informacion previa

        return render(request, "AppCoder/editar_profes.html", {"form": miFormulario})





#HACIENDO EL CRUD de Profes --- CLÁSICO

#Read
def ver_cursos(request):
    todos = Curso.objects.all()
    return render(request, "AppCoder/ver_cursos.html", {"cursos":todos})





def login_view(request):

    if request.method == "POST": #click al boton iniciar sesion

        form_inicio = AuthenticationForm(request, data = request.POST)
        
        if form_inicio.is_valid(): #el formulario nos ayuda a validar

            info = form_inicio.cleaned_data #data que se escribio en el formulario de login en modo diccionario 
            usuario = info.get("username")
            contra = info.get("password")

            #acá hacemos la validación
            user = authenticate(username=usuario, password=contra) #existe el usuario (retorna el usuario) ---- no existe usuario (retorna None)

            if user:
                login(request, user)    #iniciar sesion ya que el usuario si existe (credenciales correctas)
                return render(request, "AppCoder/inicio.html", {"usuario":user})
        
        else:
            return render(request,"AppCoder/inicio.html", {"mensaje":"DATOS INCORRECTOS"})

    form_inicio = AuthenticationForm() #formulario vacio

    return render(request,"AppCoder/login.html", {"form":form_inicio} )


def register(request):

      if request.method == 'POST':

            #form = UserCreationForm(request.POST)
            form = UserRegisterForm(request.POST)
            if form.is_valid():

                  username = form.cleaned_data['username']
                  form.save()
                  return render(request,"AppCoder/inicio.html" ,  {"mensaje":"Usuario Creado :)"})

      else:
            #form = UserCreationForm()       
            form = UserRegisterForm()     

      return render(request,"AppCoder/register.html" ,  {"form":form})



# Vista de editar el perfil
@login_required
def editarPerfil(request):

    usuario = request.user

    if request.method == 'POST':

        miFormulario = UserEditForm(request.POST)

        if miFormulario.is_valid():

            informacion = miFormulario.cleaned_data

            usuario.email = informacion['email']
            usuario.password1 = informacion['password1']
            usuario.password2 = informacion['password2']
            usuario.last_name = informacion['last_name']
            usuario.first_name = informacion['first_name']

            usuario.save()

            return render(request, "AppCoder/inicio.html")

    else:

        miFormulario = UserEditForm(initial={'email': usuario.email})

    return render(request, "AppCoder/editarPerfil.html", {"miFormulario": miFormulario, "usuario": usuario})


@login_required
def agregarAvatar(request):
    if request.method == 'POST':
        miFormulario = AvatarFormulario(request.POST, request.FILES)
        if miFormulario.is_valid():
            usuario = request.user
            imagen = miFormulario.cleaned_data['imagen']
            avatar = Avatar(user=usuario, imagen=imagen)
            avatar.save()
            # Redirigir a alguna página de éxito o realizar alguna otra acción
            return render(request, "AppCoder/inicio.html")  # Asegúrate de reemplazar 'nombre_de_la_vista_de_exito' con la vista que desees

    else:
        miFormulario = AvatarFormulario()
    
    return render(request, "AppCoder/agregarAvatar.html", {"miFormulario": miFormulario})








#Vista basada en clases  --- CRUD estudiantes

#Read 
class EstudianteLista(ListView): #estudiante_list.html
    model = Estudiante
    template_name = "AppCoder/LISTA_ESTUDIANTES.html"

#Detail 
class EstudianteDetalle(DetailView): #estudiante_detail.html
    model = Estudiante
    
#Create
class EstudianteCrear(CreateView): #estudiante_form.html
    model = Estudiante
    fields = ["nombre", "apellido", "email"]
    success_url = "/AC/estudiantes/lista/"

#Update
class EstudianteActualizar(UpdateView): #estudiante_form.html
    model = Estudiante
    fields = ["nombre", "apellido", "email"]
    success_url = "/AC/estudiantes/lista/"

#Delete
class EstudianteBorrar(DeleteView): #estudiante_confirm_delete.html
    model = Estudiante 
    success_url = "/AC/estudiantes/lista/"


