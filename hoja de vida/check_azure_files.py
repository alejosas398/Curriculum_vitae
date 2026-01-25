#!/usr/bin/env python
"""
Script para verificar qué archivos están en Azure y sus nombres reales.
Ejecutar con: python manage.py shell < check_azure_files.py
"""

import os
import sys
from django.conf import settings

def main():
    print("\n" + "="*60)
    print("🔍 Verificando archivos en Azure Blob Storage")
    print("="*60)
    
    # Check if Azure is configured
    if not settings.AZURE_STORAGE_CONNECTION_STRING:
        print("❌ ERROR: Azure NO está configurado")
        return
    
    print(f"✅ Azure configurado")
    print(f"   Storage Account: {settings.AZURE_STORAGE_CONNECTION_STRING[:50]}...")
    print(f"   Container: {settings.AZURE_CONTAINER_NAME}")
    
    from Val.azure_storage import AzureBlobStorage
    from pagina_usuario.models import Perfil
    
    try:
        storage = AzureBlobStorage()
        
        print("\n📋 Listando archivos en Azure:\n")
        
        # List all blobs
        service_client = storage._get_service_client()
        container_client = service_client.get_container_client(settings.AZURE_CONTAINER_NAME)
        
        blobs = container_client.list_blobs()
        count = 0
        for blob in blobs:
            print(f"  📄 {blob.name}")
            print(f"     └─ Tamaño: {blob.size} bytes")
            print(f"     └─ Modificado: {blob.last_modified}")
            count += 1
        
        if count == 0:
            print("  ⚠️  No hay archivos en Azure")
        else:
            print(f"\n✅ Total: {count} archivos")
        
        print("\n📊 Verificando perfiles en BD:\n")
        
        for perfil in Perfil.objects.all():
            print(f"  👤 {perfil.user.username}")
            if perfil.foto:
                print(f"     └─ Foto BD: {perfil.foto.name}")
                print(f"     └─ Foto URL: {perfil.foto.url}")
                
                # Check if file exists in Azure
                try:
                    exists = storage.exists(perfil.foto.name)
                    if exists:
                        print(f"     └─ ✅ Existe en Azure")
                    else:
                        print(f"     └─ ❌ NO existe en Azure")
                except Exception as e:
                    print(f"     └─ ⚠️  Error verificando: {str(e)}")
            else:
                print(f"     └─ Sin foto")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*60)

if __name__ == '__main__':
    main()
