from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='user_login'), 
    path('logout/', views.user_logout, name='user_logout'),
    path('', views.welcome, name='welcome'),
    path('lista-cursos/', views.lista_cursos, name='lista_cursos'),
    path('inscribirse/<int:curso_id>/', views.inscribirse_curso, name='inscribirse_curso'),
    path('detalle_curso/<int:curso_id>/', views.detalle_curso, name='detalle_curso'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('curso/<int:curso_id>/usuarios/', views.usuarios_inscritos_curso, name='usuarios_inscritos_curso'),
    path('profe/', views.lista_profe, name='lista_profe'),
    path('comentarios_alumno/', views.comentarios_alumno, name='comentarios_alumno'),
    path('editar_comentario/<int:comentario_id>/', views.editar_comentario, name='editar_comentario'),
    path('eliminar_comentario/<int:comentario_id>/', views.eliminar_comentario, name='eliminar_comentario'),
    path('nueva_respuesta/<int:comentario_id>/', views.nueva_respuesta, name='nueva_respuesta'),
    path('notificaciones/', views.mostrar_notificaciones, name='notificaciones'),
    path('editar-perfil/', views.editar_perfil_usuario, name='editar_perfil'),
    path('cursos-inscritos/', views.mostrar_cursos_inscritos, name='cursos_inscritos'),
    path('temario/<int:curso_id>/', views.mostrar_temario, name='mostrar_temario'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)