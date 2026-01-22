#!/usr/bin/env python
"""
Script para poblar CVs vacíos con datos de ejemplo.
Este script se puede ejecutar en Render para solucionar el problema
de usuarios que no ven contenido en su CV.
"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Val.settings')
import django
django.setup()

from django.contrib.auth.models import User
from pagina_usuario.models import Perfil, Experiencia, Educacion, Curso, Habilidad, Productos, Recomendacion
from datetime import date
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_sample_experience(perfil):
    """Crear experiencia laboral de ejemplo"""
    if perfil.experiencias.count() == 0:
        Experiencia.objects.create(
            perfil=perfil,
            empresa="Empresa de Desarrollo S.A.",
            cargo="Desarrollador Web",
            puesto="Desarrollador Full Stack",
            lugar_empresa="Ciudad Principal",
            email_empresa="contacto@empresa.com",
            sitio_web_empresa="https://empresa.com",
            fecha_inicio=date.today().replace(month=1, day=1),
            descripcion="Desarrollo de aplicaciones web modernas utilizando tecnologías como Django, React y PostgreSQL. Participación en proyectos de e-commerce y sistemas de gestión.",
            activo=True
        )
        logger.info(f"Created sample experience for {perfil.user.username}")

def create_sample_education(perfil):
    """Crear educación de ejemplo"""
    if perfil.educaciones.count() == 0:
        Educacion.objects.create(
            perfil=perfil,
            titulo="Licenciatura en Informática",
            institucion="Universidad Nacional",
            estado="Completado",
            graduado=True,
            fecha_inicio=date.today().replace(year=date.today().year-4, month=9, day=1),
            fecha_fin=date.today().replace(year=date.today().year-1, month=6, day=30)
        )
        logger.info(f"Created sample education for {perfil.user.username}")

def create_sample_course(perfil):
    """Crear curso de ejemplo"""
    if perfil.cursos.count() == 0:
        Curso.objects.create(
            perfil=perfil,
            nombre="Desarrollo Web con Django",
            institucion="Plataforma de Cursos Online",
            entidad="Ministerio de Educación",
            total_horas=60,
            fecha_inicio=date.today().replace(month=date.today().month-2, day=1),
            fecha_fin=date.today().replace(month=date.today().month-1, day=30),
            descripcion="Curso completo de desarrollo web con Django, incluyendo modelos, vistas, templates y despliegue en producción.",
            activo=True
        )
        logger.info(f"Created sample course for {perfil.user.username}")

def create_sample_skills(perfil):
    """Crear habilidades de ejemplo"""
    if perfil.habilidades.count() == 0:
        skills = ["Python", "Django", "JavaScript", "HTML/CSS", "Git", "PostgreSQL"]
        for skill in skills:
            Habilidad.objects.create(perfil=perfil, nombre=skill)
        logger.info(f"Created sample skills for {perfil.user.username}")

def create_sample_product(perfil):
    """Crear producto/proyecto de ejemplo"""
    if perfil.productos.count() == 0:
        Productos.objects.create(
            perfil=perfil,
            titulo="Sistema de Gestión de Proyectos",
            tipo="Académico",
            clasificador="Desarrollo de Software",
            descripcion="Aplicación web para gestión de proyectos desarrollada como trabajo final de carrera. Incluye funcionalidades de creación de proyectos, asignación de tareas y seguimiento de progreso.",
            activo=True
        )
        logger.info(f"Created sample product for {perfil.user.username}")

def create_sample_recommendation(perfil):
    """Crear recomendación de ejemplo"""
    if perfil.recomendaciones.count() == 0:
        Recomendacion.objects.create(
            perfil=perfil,
            nombre_contacto="Dr. María González",
            telefono_contacto="0991234567",
            relacion="Profesora Universitaria",
            tipo_reconocimiento="Académico",
            fecha_reconocimiento=date.today().replace(year=date.today().year-1),
            descripcion="Excelente estudiante con gran capacidad de aprendizaje y dedicación. Destacó en proyectos finales y demostró habilidades excepcionales en desarrollo de software.",
            entidad_patrocinadora="Universidad Nacional",
            activo=True
        )
        logger.info(f"Created sample recommendation for {perfil.user.username}")

def populate_empty_cv(user):
    """Poblar un CV vacío con datos de ejemplo"""
    try:
        perfil = Perfil.objects.get(user=user)

        # Contar contenido actual
        total_content = (
            perfil.experiencias.count() +
            perfil.educaciones.count() +
            perfil.cursos.count() +
            perfil.productos.count() +
            perfil.recomendaciones.count() +
            perfil.habilidades.count()
        )

        if total_content == 0:
            logger.info(f"Populating empty CV for user: {user.username}")

            # Crear datos de ejemplo
            create_sample_experience(perfil)
            create_sample_education(perfil)
            create_sample_course(perfil)
            create_sample_skills(perfil)
            create_sample_product(perfil)
            create_sample_recommendation(perfil)

            # Actualizar profesión si está vacía
            if not perfil.profesion:
                perfil.profesion = "Desarrollador Web"
                perfil.save()

            logger.info(f"Successfully populated CV for {user.username}")
            return True
        else:
            logger.info(f"User {user.username} already has content ({total_content} items)")
            return False

    except Perfil.DoesNotExist:
        logger.error(f"Profile not found for user {user.username}")
        return False
    except Exception as e:
        logger.error(f"Error populating CV for {user.username}: {str(e)}")
        return False

def main():
    """Función principal"""
    logger.info("Starting CV population script")

    # Obtener todos los usuarios
    users = User.objects.all()
    logger.info(f"Found {users.count()} users")

    populated_count = 0
    skipped_count = 0

    for user in users:
        if populate_empty_cv(user):
            populated_count += 1
        else:
            skipped_count += 1

    logger.info(f"Script completed. Populated: {populated_count}, Skipped: {skipped_count}")

    # Mostrar resumen final
    print("\n=== RESUMEN FINAL ===")
    print(f"Usuarios procesados: {users.count()}")
    print(f"CVs poblados: {populated_count}")
    print(f"CVs ya tenían contenido: {skipped_count}")

if __name__ == "__main__":
    main()
