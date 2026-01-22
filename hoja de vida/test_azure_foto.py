#!/usr/bin/env python
"""
Script para probar la integración de fotos de perfil con Azure Blob Storage
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Val.settings')
django.setup()

from pagina_usuario.models import Perfil
from pagina_usuario.azure_blob import upload_blob_bytes, download_blob_bytes
from django.conf import settings

def test_azure_connection():
    """Probar conexión básica con Azure"""
    print("=== Probando conexión con Azure Blob Storage ===")

    # Verificar configuración
    conn_str = getattr(settings, 'AZURE_STORAGE_CONNECTION_STRING', None)
    container = getattr(settings, 'AZURE_CONTAINER_NAME', 'cursos')

    if not conn_str:
        print("❌ AZURE_STORAGE_CONNECTION_STRING no configurada")
        return False

    print(f"✅ Connection string configurada")
    print(f"📦 Container: {container}")

    # Probar subir un archivo pequeño de prueba
    test_data = b"Test data for Azure Blob Storage"
    test_blob_name = "test_foto_integration.txt"

    if upload_blob_bytes(test_blob_name, test_data, "text/plain"):
        print("✅ Subida de prueba exitosa")

        # Probar descarga
        downloaded = download_blob_bytes(test_blob_name)
        if downloaded == test_data:
            print("✅ Descarga de prueba exitosa")
            return True
        else:
            print("❌ Error en descarga de prueba")
            return False
    else:
        print("❌ Error en subida de prueba")
        return False

def test_perfil_foto_url():
    """Probar la propiedad foto_url de los perfiles"""
    print("\n=== Probando propiedad foto_url ===")

    try:
        # Obtener un perfil de ejemplo
        perfil = Perfil.objects.first()
        if not perfil:
            print("❌ No hay perfiles en la base de datos")
            return False

        print(f"Perfil encontrado: {perfil}")

        if perfil.foto:
            print(f"Foto actual: {perfil.foto.name}")
            foto_url = perfil.foto_url
            print(f"URL de foto: {foto_url}")
        else:
            print("El perfil no tiene foto asignada")

        return True

    except Exception as e:
        print(f"❌ Error probando foto_url: {e}")
        return False

def main():
    print("Iniciando pruebas de integración de fotos con Azure...\n")

    azure_ok = test_azure_connection()
    perfil_ok = test_perfil_foto_url()

    if azure_ok and perfil_ok:
        print("\n✅ Todas las pruebas pasaron correctamente")
        return 0
    else:
        print("\n❌ Algunas pruebas fallaron")
        return 1

if __name__ == "__main__":
    sys.exit(main())
