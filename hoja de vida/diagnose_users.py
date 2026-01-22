import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Val.settings')
import django
django.setup()

from django.contrib.auth.models import User
from pagina_usuario.models import Perfil

print("=== DIAGNÓSTICO DE USUARIOS Y PERFILES ===")

# Obtener todos los usuarios
users = User.objects.all()
print(f"Total de usuarios: {users.count()}")

for user in users:
    print(f"\nUsuario: {user.username} ({user.first_name} {user.last_name})")
    print(f"  Email: {user.email}")
    print(f"  Staff: {user.is_staff}")
    print(f"  Superuser: {user.is_superuser}")

    # Verificar si tiene perfil
    try:
        perfil = Perfil.objects.get(user=user)
        print(f"  ✅ Tiene perfil: {perfil.nombre_completo or 'Sin nombre completo'}")
        print(f"  Profesión: {perfil.profesion or 'No definida'}")

        # Contar contenido del perfil
        experiencias = perfil.experiencias.count()
        educaciones = perfil.educaciones.count()
        cursos = perfil.cursos.count()
        productos = perfil.productos.count()
        recomendaciones = perfil.recomendaciones.count()
        habilidades = perfil.habilidades.count()

        print("  Contenido del CV:")
        print(f"    - Experiencias: {experiencias}")
        print(f"    - Educaciones: {educaciones}")
        print(f"    - Cursos: {cursos}")
        print(f"    - Productos/Proyectos: {productos}")
        print(f"    - Recomendaciones: {recomendaciones}")
        print(f"    - Habilidades: {habilidades}")

        total_contenido = experiencias + educaciones + cursos + productos + recomendaciones + habilidades
        print(f"  Total elementos en CV: {total_contenido}")

    except Perfil.DoesNotExist:
        print("  ❌ NO tiene perfil creado")
        # Crear perfil automáticamente
        print("  Creando perfil...")
        perfil = Perfil.objects.create(user=user)
        print(f"  ✅ Perfil creado: {perfil}")

print("\n=== RESUMEN ===")
print(f"Usuarios totales: {User.objects.count()}")
print(f"Perfiles totales: {Perfil.objects.count()}")
print(f"Usuarios sin perfil: {User.objects.count() - Perfil.objects.count()}")
