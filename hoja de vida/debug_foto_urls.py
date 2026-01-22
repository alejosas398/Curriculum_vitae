#!/usr/bin/env python
"""
Script para debuggear las URLs de fotos de perfil
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Val.settings')
django.setup()

from pagina_usuario.models import Perfil
from django.conf import settings

def debug_foto_urls():
    """Debug de URLs de fotos de perfil"""
    print("=== Debug de URLs de fotos de perfil ===\n")

    perfiles = Perfil.objects.all()
    print(f"Total de perfiles: {perfiles.count()}\n")

    for perfil in perfiles:
        print(f"Perfil: {perfil.user.username}")
        print(f"  Tiene foto: {bool(perfil.foto)}")

        if perfil.foto:
            print(f"  Nombre del archivo: {perfil.foto.name}")
            print(f"  Ruta local existe: {os.path.exists(perfil.foto.path) if hasattr(perfil.foto, 'path') else 'N/A'}")

            # Verificar si es Azure
            foto_name = perfil.foto.name
            is_azure = perfil._is_azure_blob_name(foto_name) if hasattr(perfil, '_is_azure_blob_name') else False
            print(f"  Detectado como Azure: {is_azure}")

            # URL generada
            foto_url = perfil.foto_url
            print(f"  foto_url property: {foto_url}")

            # URL local si existe
            try:
                local_url = perfil.foto.url
                print(f"  foto.url (local): {local_url}")
            except Exception as e:
                print(f"  foto.url (error): {e}")

        print()

if __name__ == "__main__":
    debug_foto_urls()
