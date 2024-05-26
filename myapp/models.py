from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Cursos(models.Model):
    nombre = models.CharField(max_length=255)
    tipo = models.CharField(max_length=100)
    decribcion = models.CharField(max_length=255)
    años = models.CharField(max_length=255)
    
    def __str__(self):
        return self.nombre
    
class OtraClase(models.Model):
    fecha_de_nacimiento = models.DateField(null=True, blank=True)
    foto_de_perfil = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    descripcion = models.TextField(blank=True)
    original = models.ForeignKey(User, on_delete=models.CASCADE)
    

class InscripcionCurso(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    curso = models.ForeignKey(Cursos, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inscripción de {self.usuario.username} en {self.curso.nombre}"
    
class Profesor(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    imagen = models.ImageField(upload_to='profesor_images/', null=True, blank=True)
    cursos = models.ForeignKey(Cursos, on_delete=models.CASCADE)

    def __str__(self):
        return {self.nombre}


class Comentario(models.Model):
    alumno = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='comentarios_likes', blank=True)

    def __str__(self):
        return f"Comentario de {self.alumno.username}"

    def toggle_like(self, user):
        if user in self.likes.all():
            self.likes.remove(user)
        else:
            self.likes.add(user)

    def can_edit(self, user):
        return user == self.alumno

    def delete_comment(self):
        self.likes.clear()  # Elimina todas las relaciones ManyToMany con usuarios
        self.delete()

class Respuesta(models.Model):
    comentario_padre = models.ForeignKey(Comentario, on_delete=models.CASCADE, related_name='respuestas')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Respuesta de {self.autor.username} al comentario {self.comentario_padre.id}"
    
    
class Notificacion(models.Model):
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE)
    remitente = models.ForeignKey(User, related_name='notificaciones_enviadas', on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20)  # Tipo de notificación: "like" o "respuesta"
    comentario = models.ForeignKey(Comentario, on_delete=models.CASCADE)
    vista = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    @staticmethod
    def create_like_notification(comentario, remitente, destinatario):
        # Crear notificación de like
        Notificacion.objects.create(destinatario=destinatario, remitente=remitente, tipo="like", comentario=comentario)

    @staticmethod
    def create_response_notification(comentario, remitente, destinatario):
        # Crear notificación de respuesta
        Notificacion.objects.create(destinatario=destinatario, remitente=remitente, tipo="respuesta", comentario=comentario)
    

class Temario(models.Model):
    curso = models.ForeignKey(Cursos, on_delete=models.CASCADE, related_name='temarios')
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    
    def __str__(self):
        return f"{self.titulo} - {self.curso.nombre}"