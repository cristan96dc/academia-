from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm, ComentarioForm  
from .models import Cursos, OtraClase, InscripcionCurso, Profesor, Comentario, Respuesta, Notificacion
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .forms import OtraClaseForm 
from django.http import HttpResponse
from channels.layers import get_channel_layer
# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            fecha_nacimiento = request.POST.get('fecha_de_nacimiento')
            foto_perfil = request.FILES.get('foto_de_perfil')
            descripcion = request.POST.get('descripcion')
            OtraClase.objects.create(original=user, fecha_de_nacimiento=fecha_nacimiento, foto_de_perfil=foto_perfil, descripcion=descripcion)
            return redirect('user_logout')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('welcome')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('welcome')


def send_notification_to_channel(notification):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notifications_channel_name",
        {
            "type": "send_notification",
            "notification": notification
        }
    )


def welcome(request):
    

    return render(request, 'welcome.html')

def lista_cursos(request):
    cursos = Cursos.objects.all()

    tipos = Cursos.objects.values_list('tipo', flat=True).distinct()

    años = Cursos.objects.values_list('años', flat=True).distinct()
    
    # Filtrar los cursos según lo solicitado
    tipo_filtrado = request.GET.get('tipo')
    años_filtrados = request.GET.get('años')
    if tipo_filtrado:
        cursos = cursos.filter(tipo=tipo_filtrado)
    if años_filtrados:
        cursos = cursos.filter(años=años_filtrados)
    
    return render(request, 'cursos.html', {'cursos': cursos, 'tipos': tipos, 'años': años})

@login_required(login_url='/login/')  # Este decorador asegura que el usuario esté autenticado
def detalle_curso(request, curso_id):
    curso = Cursos.objects.get(pk=curso_id)
    usuario_inscrito = InscripcionCurso.objects.filter(usuario=request.user, curso=curso).exists()
    return render(request, 'detalle_curso.html', {'curso': curso, 'usuario_inscrito': usuario_inscrito})


def inscribirse_curso(request, curso_id):
    if request.method == 'POST':
        curso = Cursos.objects.get(pk=curso_id)
        # Verificar si el usuario ya está inscrito en el curso
        if not InscripcionCurso.objects.filter(usuario=request.user, curso=curso).exists():
            # Crear una inscripción para el usuario en el curso
            InscripcionCurso.objects.create(usuario=request.user, curso=curso)
    
    # Redirigir a la página de detalles del curso recién inscrito
    return redirect('detalle_curso', curso_id=curso_id)


def perfil_usuario(request):
    usuario = request.user
    
    # Obtener el objeto OtraClase asociado al usuario, si existe
    try:
        otra_clase_info = OtraClase.objects.get(original=usuario)
    except OtraClase.DoesNotExist:
        otra_clase_info = None
    
    # Obtener la lista de cursos inscritos por el usuario
    cursos_inscritos = InscripcionCurso.objects.filter(usuario=usuario)
    
    # Obtener los comentarios del usuario
    comentarios_usuario = Comentario.objects.filter(alumno=usuario)
    
    return render(request, 'perfil.html', {'usuario': usuario, 'otra_clase_info': otra_clase_info, 'cursos_inscritos': cursos_inscritos, 'comentarios_usuario': comentarios_usuario})


def usuarios_inscritos_curso(request, curso_id):
    curso = get_object_or_404(Cursos, pk=curso_id)
    usuarios_inscritos = InscripcionCurso.objects.filter(curso=curso)
    return render(request, 'usuarios_inscritos_curso.html', {'curso': curso, 'usuarios_inscritos': usuarios_inscritos})


def lista_profe(request):
    # Obtener todos los profesores y todos los cursos
    profesores = Profesor.objects.all()
    cursos = Cursos.objects.all()

    # Obtener tipos únicos de cursos
    tipos_cursos = cursos.values_list('tipo', flat=True).distinct()

    # Obtener parámetros de filtrado
    nombre_filtrado = request.GET.get('nombre_curso')
    descripcion_filtrada = request.GET.get('descripcion_curso')
    tipo_filtrado = request.GET.get('tipo_curso')

    # Filtrar profesores según los parámetros de filtrado
    if nombre_filtrado:
        profesores = profesores.filter(cursos__nombre=nombre_filtrado)
    
    if descripcion_filtrada:
        profesores = profesores.filter(cursos__descripcion=descripcion_filtrada)
    
    if tipo_filtrado:
        profesores = profesores.filter(cursos__tipo=tipo_filtrado)

    return render(request, 'profes.html', {'profesores': profesores, 'tipos_cursos': tipos_cursos})




@login_required
def comentarios_alumno(request):
    comentarios = Comentario.objects.all()
    
    if request.method == 'POST':
        if 'texto' in request.POST:
            # Agregar un nuevo comentario
            texto = request.POST.get('texto')
            usuario = request.user
            alumno, creado = User.objects.get_or_create(username=usuario.username)
            Comentario.objects.create(alumno=alumno, texto=texto)
            return redirect('comentarios_alumno')
        elif 'like' in request.POST:
            # Dar o quitar like a un comentario
            comentario_id = request.POST.get('comentario_id')
            comentario = Comentario.objects.get(pk=comentario_id)
            comentario.toggle_like(request.user)
            comentario.save()
            return redirect('comentarios_alumno')

    return render(request, 'comentarios_alumno.html', {'comentarios': comentarios})
                
        

    
def nueva_respuesta(request, comentario_id):
    comentario = get_object_or_404(Comentario, pk=comentario_id)
    respuestas = Respuesta.objects.filter(comentario_padre=comentario)
    
    if request.method == 'POST':
        texto = request.POST.get('texto')
        autor = request.user
        respuesta = Respuesta.objects.create(comentario_padre=comentario, autor=autor, texto=texto)
        
        # Obtener el destinatario de la notificación (creador del comentario original)
        destinatario = comentario.alumno
        
        # Crear notificación de respuesta
        Notificacion.create_response_notification(comentario, autor, destinatario=destinatario)
        
        return redirect('nueva_respuesta', comentario_id=comentario_id)
    
    # Obtener las notificaciones no vistas del usuario actual
    notificaciones = Notificacion.objects.filter(destinatario=request.user, vista=False)
    # Marcar las notificaciones como vistas
    notificaciones.update(vista=True)
    
    return render(request, 'nueva_respuesta.html', {'comentario': comentario, 'respuestas': respuestas, 'notificaciones': notificaciones})


def editar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, pk=comentario_id)
    
    # Verificar si el usuario tiene permiso para editar el comentario
    if request.user == comentario.alumno:
        if request.method == 'POST':
            form = ComentarioForm(request.POST, instance=comentario)
            if form.is_valid():
                form.save()
                return redirect('perfil_usuario')
        else:
            form = ComentarioForm(instance=comentario)
        
        return render(request, 'editar_comentario.html', {'form': form, 'comentario': comentario})
    else:
        # Manejar caso donde el usuario no tiene permisos para editar el comentario
        return redirect('perfil_usuario')  # O mostrar algún mensaje de error


def eliminar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, pk=comentario_id)
    
    # Verificar si el usuario tiene permiso para eliminar el comentario
    if request.user == comentario.alumno:
        comentario.delete()
    
    return redirect('perfil_usuario')







from asgiref.sync import async_to_sync

def mostrar_notificaciones(request):
    if request.user.is_authenticated:
        notificaciones = Notificacion.objects.filter(destinatario=request.user).order_by('-fecha_creacion')
        respuestas = Respuesta.objects.filter(autor=request.user)
        notificaciones_no_vistas = notificaciones.filter(vista=False)
        tiene_notificaciones_no_vistas = notificaciones_no_vistas.exists()

        if tiene_notificaciones_no_vistas:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"notifications_{request.user.id}",
                {
                    "type": "send_notification",
                    "notification": "Tienes nuevas notificaciones"
                }
            )

        notificaciones_no_vistas.update(vista=True)

        return render(request, 'notificaciones.html', {
            'notificaciones': notificaciones,
            'respuestas': respuestas,
            'notificaciones_no_vistas': tiene_notificaciones_no_vistas
        })
    
def editar_perfil_usuario(request):
    # Obtener el objeto OtraClase asociado al usuario actual, si existe
    try:
        otra_clase_info = OtraClase.objects.get(original=request.user)
    except OtraClase.DoesNotExist:
        otra_clase_info = None
    
    if request.method == 'POST':
        # Si el formulario se envió con datos, crear una instancia del formulario con los datos recibidos
        form = OtraClaseForm(request.POST, request.FILES, instance=otra_clase_info)
        if form.is_valid():
            form.save()  # Guardar los datos del formulario en la base de datos
            return redirect('perfil_usuario')  # Redireccionar a la página de perfil después de guardar los cambios
    else:
        # Si el formulario no se envió con datos, crear una instancia del formulario vacía
        form = OtraClaseForm(instance=otra_clase_info)
    
    return render(request, 'editar_perfil.html', {'form': form})


@login_required
def mostrar_cursos_inscritos(request):
    usuario = request.user
    inscripciones = InscripcionCurso.objects.filter(usuario=usuario)
    cursos_inscritos = [inscripcion.curso for inscripcion in inscripciones]
    return render(request, 'cursos_inscritos.html', {'cursos_inscritos': cursos_inscritos})


def mostrar_temario(request, curso_id):
    usuario = request.user
    inscripciones = InscripcionCurso.objects.filter(usuario=usuario, curso_id=curso_id)
    if not inscripciones:
        return HttpResponse("No estás inscrito en este curso.")
    
    curso = get_object_or_404(Cursos, id=curso_id)
    temarios = curso.temarios.all()
    return render(request, 'temario.html', {'curso': curso, 'temarios': temarios})


