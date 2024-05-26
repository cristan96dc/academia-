from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import OtraClase
from django import forms
from .models import Cursos

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")
        

from .models import Comentario

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        
        
class OtraClaseForm(forms.ModelForm):
    class Meta:
        model = OtraClase
        fields = [ 'foto_de_perfil', 'descripcion']

    def __init__(self, *args, **kwargs):
        super(OtraClaseForm, self).__init__(*args, **kwargs)
        self.fields['foto_de_perfil'].required = False  # Hacer que la foto de perfil no sea obligatoria en la edición  # Lista de campos que deseas editar en el formulario
        
        


class InscripcionForm(forms.Form):
    curso_id = forms.ModelChoiceField(queryset=Cursos.objects.all(), widget=forms.HiddenInput)