import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Val.settings')
import django
django.setup()

from django.contrib.auth.models import User

print("=== DIAGNÓSTICO DE PERMISOS DE USUARIOS ===")

users = User.objects.all()
print(f"Total de usuarios: {users.count()}\n")

for user in users:
    print(f"Usuario: {user.username}")
    print(f"  - is_staff: {user.is_staff}")
    print(f"  - is_superuser: {user.is_superuser}")
    print(f"  - is_active: {user.is_active}")

    # Verificar si puede acceder al admin
    if user.is_staff and user.is_superuser and user.is_active:
        print("  ✅ DEBERÍA poder acceder al admin")
    else:
        print("  ❌ NO puede acceder al admin")
        if not user.is_staff:
            print("     Razón: No es staff")
        if not user.is_superuser:
            print("     Razón: No es superusuario")
        if not user.is_active:
            print("     Razón: Usuario inactivo")

    # Verificar grupos y permisos
    print(f"  - Grupos: {[group.name for group in user.groups.all()]}")
    print(f"  - Permisos específicos: {user.user_permissions.count()}")

    print()

