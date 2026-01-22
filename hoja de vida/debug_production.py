#!/usr/bin/env python
"""
Script para debuggear fotos en producción
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Val.settings')
django.setup()

from pagina_usuario.models import Perfil
from django.conf import settings

def debug_production_photos():
    """Debug de fotos para producción"""
    print("=== Debug de fotos para producción ===\n")

    # Verificar configuración de Azure
    conn_str = getattr(settings, 'AZURE_STORAGE_CONNECTION_STRING', None)
    container = getattr(settings, 'AZURE_CONTAINER_NAME', 'cursos')

    print(f"AZURE_STORAGE_CONNECTION_STRING: {'Configurada' if conn_str else 'NO CONFIGURADA'}")
    print(f"AZURE_CONTAINER_NAME: {container}")

    if conn_str:
        # Extraer account name
        if 'AccountName=' in conn_str:
            start = conn_str.find('AccountName=') + len('AccountName=')
            end = conn_str.find(';', start)
            if end == -1:
                end = len(conn_str)
            account_name = conn_str[start:end]
            print(f"Account Name: {account_name}")
            print(f"Blob URL base: https://{account_name}.blob.core.windows.net/{container}/")
        else:
            print("No se pudo extraer AccountName de connection string")
    print()

    # Verificar perfiles
    perfiles = Perfil.objects.all()
    print(f"Total de perfiles: {perfiles.count()}\n")

    for perfil in perfiles:
        print(f"Perfil: {perfil.user.username}")
        print(f"  Tiene foto: {bool(perfil.foto)}")

        if perfil.foto:
            foto_name = perfil.foto.name
            print(f"  Nombre del archivo: {foto_name}")

            # Verificar si es Azure
            is_azure = perfil._is_azure_blob_name(foto_name) if hasattr(perfil, '_is_azure_blob_name') else False
            print(f"  Detectado como Azure: {is_azure}")

            # URL generada
            foto_url = perfil.foto_url
            print(f"  foto_url property: {foto_url}")

            # Verificar accesibilidad de la URL
            if foto_url and foto_url.startswith('https://'):
                print(f"  Es URL HTTPS: ✅")
            else:
                print(f"  Es URL local: ❌")

        print()

def simulate_production_request():
    """Simular una petición como en producción"""
    print("=== Simulación de petición de producción ===\n")

    # Simular la petición de la hoja de vida
    try:
        from django.test import RequestFactory
        from pagina_usuario.views import ver_hoja_de_vida

        factory = RequestFactory()
        request = factory.get('/hoja-de-vida/')

        # Simular usuario logueado (tomar el primer perfil)
        perfil = Perfil.objects.first()
        if perfil:
            request.user = perfil.user
            print(f"Simulando petición para usuario: {perfil.user.username}")

            # Obtener la URL de la foto
            foto_url = perfil.foto_url
            print(f"URL de foto generada: {foto_url}")

            # Verificar si es Azure
            if foto_url and 'blob.core.windows.net' in foto_url:
                print("✅ URL apunta a Azure Blob Storage")
            elif foto_url and foto_url.startswith('/media/'):
                print("❌ URL aún apunta a sistema local")
            else:
                print("⚠️ URL no válida o vacía")

        else:
            print("No hay perfiles para simular")

    except Exception as e:
        print(f"Error en simulación: {e}")

if __name__ == "__main__":
    debug_production_photos()
    simulate_production_request()

