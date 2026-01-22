#!/usr/bin/env python
"""
Script simple para probar que las fotos se muestren correctamente
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Val.settings')
django.setup()

from pagina_usuario.models import Perfil
from django.conf import settings

def test_foto_display():
    """Prueba simple de que las fotos se muestran correctamente"""
    print("=== Prueba simple de fotos ===\n")

    print(f"DEBUG mode: {settings.DEBUG}")
    print(f"Azure configured: {bool(getattr(settings, 'AZURE_STORAGE_CONNECTION_STRING', None))}\n")

    perfiles = Perfil.objects.all()

    for perfil in perfiles:
        print(f"Usuario: {perfil.user.username}")

        if perfil.foto:
            print(f"  Archivo: {perfil.foto.name}")

            # Verificar si existe localmente
            exists_local = False
            if hasattr(perfil.foto, 'path'):
                exists_local = os.path.exists(perfil.foto.path)
            print(f"  Existe local: {exists_local}")

            # Obtener URL
            foto_url = perfil.foto_url
            print(f"  URL generada: {foto_url}")

            # Verificar tipo de URL
            if foto_url:
                if foto_url.startswith('/media/'):
                    print("  ✅ URL local (correcto para desarrollo)")
                elif 'blob.core.windows.net' in foto_url:
                    print("  ✅ URL Azure (correcto para producción)")
                else:
                    print("  ⚠️  URL desconocida")
            else:
                print("  ❌ No hay URL")
        else:
            print("  No tiene foto asignada")

        print()

if __name__ == "__main__":
    test_foto_display()
