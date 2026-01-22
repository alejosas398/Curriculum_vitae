import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Val.settings')
import django
django.setup()

from django.contrib.auth.models import User
from pagina_usuario.models import Perfil, Experiencia, Educacion, Curso, Habilidad, Productos, Recomendacion
from datetime import date

def create_sample_data_for_user(username):
    """Crear datos de ejemplo para un usuario específico"""
    try:
        user = User.objects.get(username=username)
        perfil = Perfil.objects.get(user=user)

        print(f"Creando datos de ejemplo para {username}...")

        # Solo crear datos si el perfil está vacío
        if perfil.experiencias.count() == 0 and perfil.educaciones.count() == 0:
            # Crear experiencia de ejemplo
            Experiencia.objects.create(
                perfil=perfil,
                empresa="Empresa de Ejemplo S.A.",
                cargo="Desarrollador Junior",
                puesto="Desarrollador de Software",
                lugar_empresa="Ciudad de Ejemplo",
                fecha_inicio=date(2023, 1, 1),
                fecha_fin=None,  # Actualidad
                descripcion="Desarrollo de aplicaciones web utilizando Django y React.",
                activo=True
            )

            # Crear educación de ejemplo
            Educacion.objects.create(
                perfil=perfil,
                titulo="Ingeniería en Sistemas",
                institucion="Universidad de Ejemplo",
                estado="En progreso",
                fecha_inicio=date(2020, 9, 1),
                graduado=False
            )

            # Crear curso de ejemplo
            Curso.objects.create(
                perfil=perfil,
                nombre="Curso de Python Avanzado",
                institucion="Plataforma Online",
                total_horas=40,
                fecha_inicio=date(2023, 6, 1),
                fecha_fin=date(2023, 7, 1),
                descripcion="Curso completo de Python para desarrollo web.",
                activo=True
            )

            # Crear habilidades de ejemplo
            habilidades = ["Python", "Django", "JavaScript", "HTML/CSS", "Git"]
            for hab in habilidades:
                Habilidad.objects.create(perfil=perfil, nombre=hab)

            # Crear producto/proyecto de ejemplo
            Productos.objects.create(
                perfil=perfil,
                titulo="Sistema de Gestión de Inventarios",
                tipo="Laboral",
                descripcion="Sistema web para gestión de inventarios desarrollado con Django.",
                activo=True
            )

            # Crear recomendación de ejemplo
            Recomendacion.objects.create(
                perfil=perfil,
                nombre_contacto="Juan Pérez",
                telefono_contacto="0999999999",
                relacion="Supervisor",
                tipo_reconocimiento="Laboral",
                descripcion="Excelente desempeño en proyectos asignados.",
                activo=True
            )

            print(f"✅ Datos de ejemplo creados para {username}")
        else:
            print(f"ℹ️ El usuario {username} ya tiene datos en su CV")

    except User.DoesNotExist:
        print(f"❌ Usuario {username} no encontrado")
    except Perfil.DoesNotExist:
        print(f"❌ Perfil para {username} no encontrado")

def create_sample_data_for_all_empty_users():
    """Crear datos de ejemplo para todos los usuarios que no tienen contenido en su CV"""
    users = User.objects.all()
    print(f"Verificando {users.count()} usuarios...")

    for user in users:
        try:
            perfil = Perfil.objects.get(user=user)
            total_content = (
                perfil.experiencias.count() +
                perfil.educaciones.count() +
                perfil.cursos.count() +
                perfil.productos.count() +
                perfil.recomendaciones.count() +
                perfil.habilidades.count()
            )

            if total_content == 0:
                print(f"Usuario {user.username} tiene CV vacío, creando datos de ejemplo...")
                create_sample_data_for_user(user.username)
            else:
                print(f"Usuario {user.username} ya tiene {total_content} elementos en su CV")

        except Perfil.DoesNotExist:
            print(f"Usuario {user.username} no tiene perfil")

if __name__ == "__main__":
    print("=== CREANDO DATOS DE EJEMPLO ===")
    create_sample_data_for_all_empty_users()
    print("=== PROCESO COMPLETADO ===")

