from django import forms
from .models import (
    Task, Perfil, Experiencia, Habilidad, 
    Productos, Recomendacion, Curso, Educacion
)

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título de la tarea'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción...'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        exclude = ['user']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'direccion_domicilio': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

class ExperienciaForm(forms.ModelForm): # Antes ExperienciaLaboralForm
    class Meta:
        model = Experiencia # Antes ExperienciaLaboral
        fields = ['empresa', 'cargo', 'fecha_inicio', 'fecha_fin', 'descripcion']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

class EducacionForm(forms.ModelForm):
    class Meta:
        model = Educacion
        fields = ['titulo', 'institucion', 'graduado']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'institucion': forms.TextInput(attrs={'class': 'form-control'}),
        }

class HabilidadForm(forms.ModelForm):
    class Meta:
        model = Habilidad
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Python, Liderazgo...'}),
        }

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['nombre_curso', 'institucion', 'entidad', 'total_horas', 'fecha_inicio', 'fecha_fin']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class ProductosForm(forms.ModelForm):
    class Meta:
        model = Productos
        fields = ['titulo', 'tipo', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

class RecomendacionForm(forms.ModelForm):
    class Meta:
        model = Recomendacion
        fields = ['nombre_contacto', 'telefono_contacto', 'relacion']
        widgets = {
            'nombre_contacto': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono_contacto': forms.TextInput(attrs={'class': 'form-control'}),
        }