#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import django

# Fix encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Val.settings')
django.setup()

from django.contrib.auth.models import User
from pagina_usuario.models import (
    Perfil, Experiencia, Educacion, Curso, Productos, 
    Recomendacion, Habilidad, VentaGarage
)

# Obtener o crear usuario
user = User.objects.filter(username='marti').first()
if not user:
    user = User.objects.create_user(
        username='marti',
        email='marti@example.com',
        first_name='Martín',
        last_name='García'
    )

# Obtener o crear perfil
perfil, _ = Perfil.objects.get_or_create(user=user)

# Actualizar perfil con datos completos
perfil.cedula = '0995172140'
perfil.profesion = 'Desarrollador de Software'
perfil.telefono = '0995172140'
perfil.telefono_convencional = '05-2621234'
perfil.telefono_fijo = '05-2621234'
perfil.direccion_domicilio = 'Av. Circunvalación 5374, Manta'
perfil.direccion_trabajo = 'Facultad de Ciencias Médicas - ULEAM'
perfil.nacionalidad = 'Ecuatoriano'
perfil.fecha_nacimiento = date(1995, 5, 15)
perfil.lugar_nacimiento = 'Manta, Ecuador'
perfil.sexo = 'H'
perfil.estado_civil = 'Soltero'
perfil.licencia_conducir = 'B'
perfil.sitio_web = 'https://example.com'
perfil.descripcion = 'Profesional especializado en tecnología'
perfil.activo = True
perfil.save()

print("OK: Perfil actualizado")

# Experiencias
experiencias_data = [
    {
        'empresa': 'Girasol Soluciones',
        'cargo': 'Desarrollador Full Stack',
        'puesto': 'Senior Developer',
        'lugar_empresa': 'Manta, Ecuador',
        'email_empresa': 'info@girasol.com',
        'sitio_web_empresa': 'https://girasol.com',
        'nombre_contacto_empresarial': 'Juan Pérez',
        'telefono_contacto_empresarial': '0987654321',
        'fecha_inicio': date(2025, 1, 15),
        'fecha_fin': date(2026, 1, 15),
        'descripcion': 'Desarrollo de aplicaciones web con Django y React. Implementacion de APIs REST.',
        'activo': True
    },
    {
        'empresa': 'Tech Innovations',
        'cargo': 'Desarrollador Backend',
        'puesto': 'Mid Level Developer',
        'lugar_empresa': 'Quito, Ecuador',
        'email_empresa': 'jobs@techinnovations.com',
        'sitio_web_empresa': 'https://techinnovations.com',
        'nombre_contacto_empresarial': 'María López',
        'telefono_contacto_empresarial': '0988888888',
        'fecha_inicio': date(2023, 6, 1),
        'fecha_fin': date(2024, 12, 31),
        'descripcion': 'Desarrollo de microservicios. Optimizacion de bases de datos.',
        'activo': True
    }
]

for exp_data in experiencias_data:
    exp, created = Experiencia.objects.get_or_create(
        perfil=perfil,
        empresa=exp_data['empresa'],
        defaults=exp_data
    )
    if not created:
        for key, value in exp_data.items():
            setattr(exp, key, value)
        exp.save()

print("OK: Experiencias agregadas")

# Educaciones
educaciones_data = [
    {
        'titulo': 'Ingeniero en Sistemas',
        'institucion': 'Universidad Eloy Alfaro de Manabí (ULEAM)',
        'estado': 'Completado',
        'graduado': True,
        'fecha_inicio': date(2017, 9, 1),
        'fecha_fin': date(2021, 5, 30)
    },
    {
        'titulo': 'Bachiller en Ciencias',
        'institucion': 'Unidad Educativa Eugenio Espejo',
        'estado': 'Completado',
        'graduado': True,
        'fecha_inicio': date(2010, 9, 1),
        'fecha_fin': date(2017, 6, 30)
    }
]

for edu_data in educaciones_data:
    edu, created = Educacion.objects.get_or_create(
        perfil=perfil,
        titulo=edu_data['titulo'],
        defaults=edu_data
    )

print("OK: Educaciones agregadas")

# Cursos
cursos_data = [
    {
        'nombre_curso': 'Django Advanced - Rest Framework',
        'nombre': 'Django Advanced',
        'institucion': 'Coursera',
        'entidad': 'Google',
        'nombre_contacto_auspicia': 'Carlos Sanchez',
        'telefono_contacto_auspicia': '0999999999',
        'email_empresa_patrocinadora': 'contact@coursera.com',
        'total_horas': 40,
        'fecha_inicio': date(2024, 1, 15),
        'fecha_fin': date(2024, 3, 15),
        'descripcion': 'Curso avanzado de Django REST Framework para desarrollo de APIs',
        'activo': True
    },
    {
        'nombre_curso': 'Docker & Kubernetes Mastery',
        'nombre': 'Docker Kubernetes',
        'institucion': 'Udemy',
        'entidad': 'Cloud Native Foundation',
        'nombre_contacto_auspicia': 'Roberto Garcia',
        'telefono_contacto_auspicia': '0988777666',
        'email_empresa_patrocinadora': 'info@udemy.com',
        'total_horas': 35,
        'fecha_inicio': date(2023, 10, 1),
        'fecha_fin': date(2023, 12, 1),
        'descripcion': 'Domina la contenedorizacion con Docker y orquestacion con Kubernetes',
        'activo': True
    }
]

for curso_data in cursos_data:
    curso, created = Curso.objects.get_or_create(
        perfil=perfil,
        nombre_curso=curso_data['nombre_curso'],
        defaults=curso_data
    )

print("OK: Cursos agregados")

# Productos (académicos y laborales)
productos_data = [
    {
        'titulo': 'Sistema de Gestión Académica',
        'nombre': 'SGA Web App',
        'tipo': 'Académico',
        'clasificador': 'Web Application',
        'descripcion': 'Aplicación web para gestión de estudiantes y calificaciones. Desarrollado con Django y Bootstrap.',
        'activo': True
    },
    {
        'titulo': 'API REST de E-commerce',
        'nombre': 'Commerce API',
        'tipo': 'Laboral',
        'clasificador': 'API REST',
        'descripcion': 'API RESTful para plataforma de comercio electrónico con autenticación JWT y pagos integrados.',
        'activo': True
    },
    {
        'titulo': 'Dashboard Analytics',
        'nombre': 'Analytics Dashboard',
        'tipo': 'Laboral',
        'clasificador': 'Dashboard',
        'descripcion': 'Dashboard interactivo para análisis de datos con gráficos en tiempo real usando React y Chart.js',
        'activo': True
    }
]

for prod_data in productos_data:
    prod, created = Productos.objects.get_or_create(
        perfil=perfil,
        titulo=prod_data['titulo'],
        defaults=prod_data
    )

print("OK: Productos agregados")

# Recomendaciones/Reconocimientos
recomendaciones_data = [
    {
        'nombre_contacto': 'Jeiko Ramírez',
        'telefono_contacto': '+593 99 734 886',
        'relacion': 'Jefe Directo',
        'tipo_reconocimiento': 'Público',
        'fecha_reconocimiento': date(2025, 10, 15),
        'descripcion': 'Excelente desempeño y liderazgo en proyectos críticos',
        'entidad_patrocinadora': 'Girasol Soluciones',
        'activo': True
    },
    {
        'nombre_contacto': 'Dr. Francisco Morales',
        'telefono_contacto': '+593 98 765 4321',
        'relacion': 'Profesor',
        'tipo_reconocimiento': 'Académico',
        'fecha_reconocimiento': date(2021, 5, 28),
        'descripcion': 'Mejor proyecto de grado en la carrera de Ingeniería en Sistemas',
        'entidad_patrocinadora': 'ULEAM',
        'activo': True
    },
    {
        'nombre_contacto': 'María Estrada',
        'telefono_contacto': '+593 99 111 2222',
        'relacion': 'Colega',
        'tipo_reconocimiento': 'Privado',
        'fecha_reconocimiento': date(2024, 8, 20),
        'descripcion': 'Reconocimiento por contribuciones significativas al equipo',
        'entidad_patrocinadora': 'Tech Innovations',
        'activo': True
    }
]

for reco_data in recomendaciones_data:
    reco, created = Recomendacion.objects.get_or_create(
        perfil=perfil,
        nombre_contacto=reco_data['nombre_contacto'],
        defaults=reco_data
    )

print("OK: Recomendaciones agregadas")

# Habilidades
habilidades_data = [
    'Python', 'Django', 'React', 'JavaScript', 'PostgreSQL',
    'Docker', 'Git', 'REST APIs', 'Linux', 'HTML/CSS'
]

for hab_nombre in habilidades_data:
    hab, created = Habilidad.objects.get_or_create(
        perfil=perfil,
        nombre=hab_nombre
    )

print("OK: Habilidades agregadas")

# Ventas Garage
ventas_data = [
    {
        'nombre_producto': 'Laptop Dell XPS 13',
        'estado_producto': 'Bueno',
        'descripcion': 'Laptop en excelente estado, solo 1 año de uso. Intel i7, 16GB RAM, SSD 512GB',
        'valor_bien': 800.00,
        'activo': True
    },
    {
        'nombre_producto': 'Bicicleta Mountain Bike',
        'estado_producto': 'Regular',
        'descripcion': 'Bicicleta todo terreno con cambios Shimano. Usada pero funcional.',
        'valor_bien': 250.00,
        'activo': True
    },
    {
        'nombre_producto': 'Guitarra Acústica',
        'estado_producto': 'Bueno',
        'descripcion': 'Guitarra acústica marca Yamaha, muy poco uso, con estuche incluido',
        'valor_bien': 180.00,
        'activo': True
    }
]

for venta_data in ventas_data:
    venta, created = VentaGarage.objects.get_or_create(
        perfil=perfil,
        nombre_producto=venta_data['nombre_producto'],
        defaults=venta_data
    )

print("OK: Ventas Garage agregadas")

print("\n" + "="*50)
print("OK: TODOS LOS DATOS DE DEMOSTRACIÓN HAN SIDO AGREGADOS")
print("="*50)
print("\nAhora ve a http://127.0.0.1:8000/hoja-de-vida/")
print("Y verás toda la información completa en la hoja de vida visual")
