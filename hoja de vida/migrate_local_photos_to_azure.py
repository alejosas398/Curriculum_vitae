#!/usr/bin/env python
"""
Script para migrar fotos del filesystem local a Azure Blob Storage.
Ejecutar con: python manage.py shell < migrate_local_photos_to_azure.py
O desde manage.py shell:
    exec(open('migrate_local_photos_to_azure.py').read())
"""

import os
import sys
from django.conf import settings
from pagina_usuario.models import Perfil, Experiencia, Curso, Recomendacion
from django.core.files.base import ContentFile
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import AzureError

def migrate_perfil_photos():
    """Migrate Perfil photos to Azure"""
    print("\n📸 Migrando fotos de perfil...")
    migrated = 0
    errors = 0
    
    for perfil in Perfil.objects.all():
        if not perfil.foto:
            continue
        
        try:
            # Check if file exists locally
            if hasattr(perfil.foto, 'path') and os.path.exists(perfil.foto.path):
                print(f"  Migrando foto de {perfil.user.username}...", end=' ')
                
                # Read the file
                with open(perfil.foto.path, 'rb') as f:
                    file_content = f.read()
                
                # Create a new file field and save
                file_name = os.path.basename(perfil.foto.name)
                perfil.foto.save(
                    file_name,
                    ContentFile(file_content),
                    save=True
                )
                print("✅")
                migrated += 1
            else:
                print(f"  ⏭️  {perfil.user.username} - ya migrada o no existe localmente")
        
        except Exception as e:
            print(f"  ❌ Error migrando {perfil.user.username}: {str(e)}")
            errors += 1
    
    return migrated, errors

def migrate_experiencia_certificates():
    """Migrate Experiencia certificates to Azure"""
    print("\n📋 Migrando certificados de experiencias...")
    migrated = 0
    errors = 0
    
    for exp in Experiencia.objects.filter(certificado__isnull=False):
        if not exp.certificado:
            continue
        
        try:
            if hasattr(exp.certificado, 'path') and os.path.exists(exp.certificado.path):
                print(f"  Migrando certificado de {exp.empresa}...", end=' ')
                
                with open(exp.certificado.path, 'rb') as f:
                    file_content = f.read()
                
                file_name = os.path.basename(exp.certificado.name)
                exp.certificado.save(
                    file_name,
                    ContentFile(file_content),
                    save=True
                )
                print("✅")
                migrated += 1
            else:
                print(f"  ⏭️  {exp.empresa} - ya migrado o no existe")
        
        except Exception as e:
            print(f"  ❌ Error migrando {exp.empresa}: {str(e)}")
            errors += 1
    
    return migrated, errors

def migrate_curso_certificates():
    """Migrate Curso certificates to Azure"""
    print("\n🎓 Migrando certificados de cursos...")
    migrated = 0
    errors = 0
    
    for curso in Curso.objects.filter(certificado__isnull=False):
        if not curso.certificado:
            continue
        
        try:
            if hasattr(curso.certificado, 'path') and os.path.exists(curso.certificado.path):
                print(f"  Migrando certificado de {curso.nombre_curso or curso.nombre}...", end=' ')
                
                with open(curso.certificado.path, 'rb') as f:
                    file_content = f.read()
                
                file_name = os.path.basename(curso.certificado.name)
                curso.certificado.save(
                    file_name,
                    ContentFile(file_content),
                    save=True
                )
                print("✅")
                migrated += 1
            else:
                print(f"  ⏭️  {curso.nombre_curso or curso.nombre} - ya migrado")
        
        except Exception as e:
            print(f"  ❌ Error migrando {curso.nombre_curso}: {str(e)}")
            errors += 1
    
    return migrated, errors

def migrate_recomendacion_certificates():
    """Migrate Recomendacion certificates to Azure"""
    print("\n⭐ Migrando certificados de recomendaciones...")
    migrated = 0
    errors = 0
    
    for rec in Recomendacion.objects.filter(certificado__isnull=False):
        if not rec.certificado:
            continue
        
        try:
            if hasattr(rec.certificado, 'path') and os.path.exists(rec.certificado.path):
                print(f"  Migrando certificado de {rec.nombre_contacto}...", end=' ')
                
                with open(rec.certificado.path, 'rb') as f:
                    file_content = f.read()
                
                file_name = os.path.basename(rec.certificado.name)
                rec.certificado.save(
                    file_name,
                    ContentFile(file_content),
                    save=True
                )
                print("✅")
                migrated += 1
            else:
                print(f"  ⏭️  {rec.nombre_contacto} - ya migrado")
        
        except Exception as e:
            print(f"  ❌ Error migrando {rec.nombre_contacto}: {str(e)}")
            errors += 1
    
    return migrated, errors

def main():
    """Run all migrations"""
    print("=" * 60)
    print("🚀 Iniciando migración de archivos a Azure Blob Storage...")
    print("=" * 60)
    
    # Check if Azure is configured
    if not settings.AZURE_STORAGE_CONNECTION_STRING:
        print("❌ ERROR: AZURE_STORAGE_CONNECTION_STRING no está configurada")
        print("   Por favor configura las variables de entorno de Azure")
        return
    
    print(f"Container: {settings.AZURE_CONTAINER_NAME}")
    
    total_migrated = 0
    total_errors = 0
    
    # Migrate photos
    m, e = migrate_perfil_photos()
    total_migrated += m
    total_errors += e
    
    # Migrate certificates
    m, e = migrate_experiencia_certificates()
    total_migrated += m
    total_errors += e
    
    m, e = migrate_curso_certificates()
    total_migrated += m
    total_errors += e
    
    m, e = migrate_recomendacion_certificates()
    total_migrated += m
    total_errors += e
    
    print("\n" + "=" * 60)
    print(f"📊 Resumen de migración:")
    print(f"   ✅ Migrados: {total_migrated}")
    print(f"   ❌ Errores: {total_errors}")
    print("=" * 60)
    
    if total_errors == 0:
        print("✨ ¡Migración completada exitosamente!")
    else:
        print(f"⚠️  Se completó con {total_errors} errores")

# Run if executed directly
if __name__ == '__main__':
    main()

# Also run automatically when imported
print("\n⚠️  NOTA: Este script migrará archivos del filesystem a Azure.")
print("    Asegúrate de que AZURE_STORAGE_CONNECTION_STRING esté configurada.")
print("    Presiona Ctrl+C para cancelar en los próximos 5 segundos...")

import time
try:
    for i in range(5):
        time.sleep(1)
except KeyboardInterrupt:
    print("\n❌ Migración cancelada")
    sys.exit(1)

main()
