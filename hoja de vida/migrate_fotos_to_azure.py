#!/usr/bin/env python
"""
Script para migrar fotos de perfil existentes desde el sistema local a Azure Blob Storage
"""
import os
import sys
import django
from pathlib import Path

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Val.settings')
django.setup()

from pagina_usuario.models import Perfil
from pagina_usuario.azure_blob import upload_file_to_blob
from django.conf import settings
import uuid

def migrate_fotos_to_azure():
    """Migrar todas las fotos de perfil locales a Azure"""
    print("=== Migrando fotos de perfil a Azure Blob Storage ===\n")

    # Obtener todas las fotos de perfil que existen localmente
    perfiles_con_foto = Perfil.objects.exclude(foto='').exclude(foto=None)

    if not perfiles_con_foto:
        print("No hay fotos de perfil para migrar")
        return

    print(f"Encontradas {perfiles_con_foto.count()} fotos de perfil")

    migrated = 0
    errors = 0

    for perfil in perfiles_con_foto:
        try:
            foto_path = perfil.foto.path if hasattr(perfil.foto, 'path') else None

            if not foto_path or not os.path.exists(foto_path):
                print(f"⚠️  Foto no encontrada localmente: {perfil.foto.name}")
                continue

            # Generar nuevo nombre único para Azure
            file_extension = Path(foto_path).suffix
            blob_name = f"perfil_fotos/{uuid.uuid4()}{file_extension}"

            print(f"📤 Migrando foto de {perfil.user.username}: {perfil.foto.name} -> {blob_name}")

            # Subir a Azure
            if upload_file_to_blob(foto_path, blob_name):
                # Actualizar el modelo con la nueva ruta
                perfil.foto.name = blob_name
                perfil.save()
                print(f"✅ Migrada exitosamente")
                migrated += 1
            else:
                print(f"❌ Error subiendo a Azure")
                errors += 1

        except Exception as e:
            print(f"❌ Error migrando foto de {perfil.user.username}: {e}")
            errors += 1

    print("
=== Resumen de migración ===")
    print(f"✅ Migradas exitosamente: {migrated}")
    print(f"❌ Errores: {errors}")
    print(f"📊 Total procesadas: {perfiles_con_foto.count()}")

    if migrated > 0:
        print("\n🔄 Recomendación: Reinicia el servidor para asegurar que los cambios surtan efecto")
        print("🧹 Considera eliminar las fotos locales después de verificar que todo funciona")

def main():
    # Verificar que Azure esté configurado
    conn_str = getattr(settings, 'AZURE_STORAGE_CONNECTION_STRING', None)
    if not conn_str:
        print("❌ AZURE_STORAGE_CONNECTION_STRING no está configurada")
        print("Configure la variable de entorno antes de ejecutar este script")
        return 1

    try:
        migrate_fotos_to_azure()
        return 0
    except Exception as e:
        print(f"❌ Error general: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
