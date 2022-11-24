from django import forms
from django.contrib.auth.models import User
from .models import Categoria, AreaEspecialidad, Conocimiento, Habilidad, Tarea, Herramienta, Provincia, \
                    Municipio, Genero, CentroTrabajo, RolTrabajo, Especialista


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class EspecialistaForm(forms.ModelForm):
    class Meta:
        model = Especialista
        fields = ['avatar', 'genero', 'fecha_nacimiento', 'ci', 'direccion', 'telefono', 'municipio', 'trabajo_antiguos',
                  'conocimientos','habilidades', 'tareas', 'herramientas']


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'abreviatura', 'descripcion']


class AreaEspecialidadForm(forms.ModelForm):
    class Meta:
        model = AreaEspecialidad
        fields = ['nombre', 'abreviatura', 'descripcion', 'categoria']


class ConocimientoForm(forms.ModelForm):
    class Meta:
        model = Conocimiento
        fields = ['descripcion']


class HabilidadForm(forms.ModelForm):
    class Meta:
        model = Habilidad
        fields = ['descripcion']


class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['descripcion']


class HerramientaForm(forms.ModelForm):
    class Meta:
        model = Herramienta
        fields = ['descripcion']


class ProvinciaForm(forms.ModelForm):
    class Meta:
        model = Provincia
        fields = ['nombre']


class GeneroForm(forms.ModelForm):
    class Meta:
        model = Genero
        fields = ['nombre']


class CentroTrabajoForm(forms.ModelForm):
    class Meta:
        model = CentroTrabajo
        fields = ['nombre']


class MunicipioForm(forms.ModelForm):
    class Meta:
        model = Municipio
        fields = ['nombre', 'provincia']


class RolTrabajoForm(forms.ModelForm):
    class Meta:
        model = RolTrabajo
        fields = ['nombre', 'descripcion', 'area_especialidad', 'conocimientos', 'habilidades', 'tareas', 'herramientas']