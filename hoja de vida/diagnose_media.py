"""
Script para diagnosticar problemas con media files en Render
Uso: python diagnose_media.py
"""

import os
import sys
from pathlib import Path

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Val.settings')

import django
django.setup()

from django.conf import settings
from pagina_usuario.models import Perfil, Experiencia, Curso, Recomendacion


def check_settings():
    """Verificar configuración de media"""
    print("\n=== CONFIGURACIÓN DE MEDIA ===")
    print(f"DEBUG: {settings.DEBUG}")
    print(f"MEDIA_URL: {settings.MEDIA_URL}")
    print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
    print(f"DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
    print(f"AZURE_CONTAINER_NAME: {getattr(settings, 'AZURE_CONTAINER_NAME', 'NO CONFIGURADO')}")
    
    azure_conn = getattr(settings, 'AZURE_STORAGE_CONNECTION_STRING', '')
    if azure_conn:
        print(f"AZURE_STORAGE_CONNECTION_STRING: {'*' * 20}...***")
    else:
        print("AZURE_STORAGE_CONNECTION_STRING: NO CONFIGURADO")


def check_local_files():
    """Verificar archivos media locales"""
    print("\n=== ARCHIVOS MEDIA LOCALES ===")
    media_root = Path(settings.MEDIA_ROOT)
    
    if not media_root.exists():
        print(f"❌ MEDIA_ROOT no existe: {media_root}")
        return 0
    
    total_files = 0
    for root, dirs, files in os.walk(media_root):
        for file in files:
            total_files += 1
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, media_root)
            size_mb = os.path.getsize(full_path) / (1024 * 1024)
            print(f"  {rel_path} ({size_mb:.2f} MB)")
    
    print(f"\nTotal de archivos locales: {total_files}")
    return total_files


def check_database_references():
    """Verificar referencias a media en la base de datos"""
    print("\n=== REFERENCIAS EN BASE DE DATOS ===")
    
    # Fotos de perfil
    perfiles_con_foto = Perfil.objects.filter(foto__isnull=False).exclude(foto='')
    print(f"\nFotos de perfil: {perfiles_con_foto.count()}")
    for perfil in perfiles_con_foto[:5]:  # Mostrar solo primeras 5
        print(f"  {perfil.user.username}: {perfil.foto.name}")
    if perfiles_con_foto.count() > 5:
        print(f"  ... y {perfiles_con_foto.count() - 5} más")
    
    # Certificados
    exp_con_cert = Experiencia.objects.filter(certificado__isnull=False).exclude(certificado='')
    print(f"\nCertificados de experiencia: {exp_con_cert.count()}")
    for exp in exp_con_cert[:3]:
        print(f"  {exp.empresa}: {exp.certificado.name}")
    
    cursos_con_cert = Curso.objects.filter(certificado__isnull=False).exclude(certificado='')
    print(f"\nCertificados de cursos: {cursos_con_cert.count()}")
    for curso in cursos_con_cert[:3]:
        print(f"  {curso.nombre}: {curso.certificado.name}")
    
    rec_con_cert = Recomendacion.objects.filter(certificado__isnull=False).exclude(certificado='')
    print(f"\nCertificados de recomendaciones: {rec_con_cert.count()}")
    for rec in rec_con_cert[:3]:
        print(f"  {rec.nombre_contacto}: {rec.certificado.name}")


def check_azure_connectivity():
    """Verificar conexión a Azure"""
    print("\n=== CONECTIVIDAD AZURE ===")
    
    if not getattr(settings, 'AZURE_STORAGE_CONNECTION_STRING', ''):
        print("⚠️  Azure no configurado")
        return
    
    try:
        from Val.azure_storage import AzureBlobStorage
        storage = AzureBlobStorage()
        print(f"✓ Conexión a Azure establecida")
        print(f"  Cuenta: {storage.account_name}")
        print(f"  Container: {storage.container_name}")
        
        # Intentar listar blobs
        try:
            dirs, files = storage.listdir('perfil_fotos/')
            print(f"  Archivos en perfil_fotos/: {len(files)}")
            for f in files[:5]:
                print(f"    - {f}")
        except Exception as e:
            print(f"  ⚠️  Error al listar blobs: {e}")
    except Exception as e:
        print(f"❌ Error de conectividad: {e}")


def check_file_integrity():
    """Verificar integridad de archivos"""
    print("\n=== INTEGRIDAD DE ARCHIVOS ===")
    
    media_root = Path(settings.MEDIA_ROOT)
    missing_files = 0
    
    for perfil in Perfil.objects.filter(foto__isnull=False).exclude(foto=''):
        if perfil.foto:
            file_path = os.path.join(settings.MEDIA_ROOT, perfil.foto.name)
            if not os.path.exists(file_path):
                print(f"❌ Archivo faltante: {perfil.foto.name}")
                missing_files += 1
    
    if missing_files == 0:
        print("✓ Todos los archivos de perfil existen localmente")
    else:
        print(f"\n❌ {missing_files} archivos faltantes")


def main():
    print("=" * 50)
    print("DIAGNÓSTICO DE MEDIA FILES")
    print("=" * 50)
    
    check_settings()
    local_file_count = check_local_files()
    check_database_references()
    check_azure_connectivity()
    check_file_integrity()
    
    print("\n" + "=" * 50)
    print("RECOMENDACIONES")
    print("=" * 50)
    
    if settings.DEBUG:
        print("✓ Estás en modo DESARROLLO (DEBUG=True)")
        if local_file_count == 0:
            print("  ⚠️  No hay archivos locales, sube algunas fotos para probar")
    else:
        print("✓ Estás en modo PRODUCCIÓN (DEBUG=False)")
        if not getattr(settings, 'AZURE_STORAGE_CONNECTION_STRING', ''):
            print("  ❌ Azure NO está configurado en producción!")
            print("     Las fotos NO se guardarán permanentemente")
        else:
            print("  ✓ Azure está configurado")
    
    print("\nPróximos pasos:")
    print("1. Si en Render no ves las fotos:")
    print("   - Verifica que AZURE_STORAGE_CONNECTION_STRING esté en Render")
    print("   - Ejecuta: python manage.py migrate_media_to_azure")
    print("2. Si en local no ves las fotos:")
    print("   - Verifica que MEDIA_ROOT sea accesible")
    print("   - Comprueba que el usuario de Django puede escribir allí")


if __name__ == '__main__':
    main()
