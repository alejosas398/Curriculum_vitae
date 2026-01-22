#!/usr/bin/env python
"""
Script para convertir todos los usuarios existentes en superusuarios independientes.
Cada usuario tendrá acceso completo al admin pero podrá gestionar su propio contenido.
"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Val.settings')
import django
django.setup()

from django.contrib.auth.models import User
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def make_all_users_admins():
    """Convertir todos los usuarios en superusuarios"""
    users = User.objects.all()
    updated_count = 0

    logger.info(f"Encontrados {users.count()} usuarios")

    for user in users:
        if not user.is_staff or not user.is_superuser:
            user.is_staff = True
            user.is_superuser = True
            user.save()
            logger.info(f"✅ Usuario {user.username} convertido en superusuario")
            updated_count += 1
        else:
            logger.info(f"ℹ️ Usuario {user.username} ya es superusuario")

    logger.info(f"Proceso completado. {updated_count} usuarios actualizados")
    print(f"\n=== RESUMEN ===")
    print(f"Usuarios totales: {users.count()}")
    print(f"Usuarios convertidos a admin: {updated_count}")
    print(f"Usuarios que ya eran admin: {users.count() - updated_count}")

if __name__ == "__main__":
    print("=== CONvirtiendo todos los usuarios en superusuarios independientes ===")
    make_all_users_admins()
    print("=== PROCESO COMPLETADO ===")

