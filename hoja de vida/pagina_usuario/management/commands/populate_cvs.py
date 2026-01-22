from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from pagina_usuario.models import Perfil, Experiencia, Educacion, Curso, Habilidad, Productos, Recomendacion
from datetime import date
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Poblar CVs vacíos con datos de ejemplo para nuevos usuarios'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando población de CVs vacíos...')

        users = User.objects.all()
        self.stdout.write(f'Encontrados {users.count()} usuarios')

        populated_count = 0
        skipped_count = 0

        for user in users:
            if self.populate_empty_cv(user):
                populated_count += 1
            else:
                skipped_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Completado. Poblados: {populated_count}, Omitidos: {skipped_count}'
            )
        )

    def populate_empty_cv(self, user):
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
                self.stdout.write(f'Poblando CV vacío para: {user.username}')

                # Crear datos de ejemplo
                self.create_sample_data(perfil)
                return True
            else:
                self.stdout.write(f'Usuario {user.username} ya tiene contenido ({total_content} items)')
                return False

        except Perfil.DoesNotExist:
            self.stderr.write(f'Perfil no encontrado para usuario {user.username}')
            return False
        except Exception as e:
            self.stderr.write(f'Error poblando CV para {user.username}: {str(e)}')
            return False

    def create_sample_data(self, perfil):
        """Crear todos los datos de ejemplo para un perfil"""
        self.create_sample_experience(perfil)
        self.create_sample_education(perfil)
        self.create_sample_course(perfil)
        self.create_sample_skills(perfil)
        self.create_sample_product(perfil)
        self.create_sample_recommendation(perfil)

        # Actualizar profesión si está vacía
        if not perfil.profesion:
            perfil.profesion = "Profesional de Tecnología"
            perfil.save()

    def create_sample_experience(self, perfil):
        """Crear experiencia laboral de ejemplo"""
        if perfil.experiencias.count() == 0:
            Experiencia.objects.create(
                perfil=perfil,
                empresa="Empresa Tecnológica S.A.",
                cargo="Desarrollador Web",
                puesto="Desarrollador Full Stack",
                lugar_empresa="Ciudad Principal",
                fecha_inicio=date.today().replace(month=1, day=1),
                descripcion="Desarrollo de aplicaciones web modernas utilizando tecnologías como Django, React y bases de datos relacionales.",
                activo=True
            )

    def create_sample_education(self, perfil):
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

    def create_sample_course(self, perfil):
        """Crear curso de ejemplo"""
        if perfil.cursos.count() == 0:
            Curso.objects.create(
                perfil=perfil,
                nombre="Desarrollo Web con Django",
                institucion="Plataforma Online",
                total_horas=60,
                fecha_inicio=date.today().replace(month=date.today().month-2, day=1),
                fecha_fin=date.today().replace(month=date.today().month-1, day=30),
                descripcion="Curso completo de desarrollo web con Django framework.",
                activo=True
            )

    def create_sample_skills(self, perfil):
        """Crear habilidades de ejemplo"""
        if perfil.habilidades.count() == 0:
            skills = ["Python", "Django", "JavaScript", "HTML/CSS", "Git", "SQL"]
            for skill in skills:
                Habilidad.objects.create(perfil=perfil, nombre=skill)

    def create_sample_product(self, perfil):
        """Crear producto/proyecto de ejemplo"""
        if perfil.productos.count() == 0:
            Productos.objects.create(
                perfil=perfil,
                titulo="Sistema de Gestión Web",
                tipo="Académico",
                descripcion="Aplicación web para gestión desarrollada como proyecto académico.",
                activo=True
            )

    def create_sample_recommendation(self, perfil):
        """Crear recomendación de ejemplo"""
        if perfil.recomendaciones.count() == 0:
            Recomendacion.objects.create(
                perfil=perfil,
                nombre_contacto="Dr. Ana López",
                telefono_contacto="0991234567",
                relacion="Profesora",
                tipo_reconocimiento="Académico",
                fecha_reconocimiento=date.today().replace(year=date.today().year-1),
                descripcion="Excelente estudiante con gran capacidad de aprendizaje.",
                activo=True
            )

