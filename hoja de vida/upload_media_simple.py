#!/usr/bin/env python
"""
Simple script to upload all media files to Azure Blob Storage
"""
import os
import sys
from pathlib import Path
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import AzureError

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Val.settings')
import django
django.setup()

from django.conf import settings

def upload_file(file_path, blob_name):
    """Upload a file to Azure Blob Storage"""
    try:
        conn_str = settings.AZURE_STORAGE_CONNECTION_STRING
        container_name = settings.AZURE_CONTAINER_NAME or 'cursos'
        
        client = BlobServiceClient.from_connection_string(conn_str)
        blob_client = client.get_blob_client(container=container_name, blob=blob_name)
        
        with open(file_path, 'rb') as data:
            blob_client.upload_blob(data, overwrite=True)
        
        print(f"✓ Uploaded: {blob_name}")
        return True
    except AzureError as e:
        print(f"✗ Error uploading {blob_name}: {e}")
        return False

def upload_media_files():
    """Upload all media files from local directory to Azure"""
    media_dir = Path(__file__).parent / 'media'
    
    if not media_dir.exists():
        print(f"Media directory not found: {media_dir}")
        return
    
    uploaded = 0
    failed = 0
    
    # Upload profile photos
    perfil_fotos_dir = media_dir / 'perfil_fotos'
    if perfil_fotos_dir.exists():
        print("\n=== Uploading Profile Photos ===")
        for file in perfil_fotos_dir.iterdir():
            if file.is_file():
                blob_name = f"perfil_fotos/{file.name}"
                if upload_file(str(file), blob_name):
                    uploaded += 1
                else:
                    failed += 1
    
    # Upload course certificates
    cert_cursos_dir = media_dir / 'certificados_cursos'
    if cert_cursos_dir.exists():
        print("\n=== Uploading Course Certificates ===")
        for file in cert_cursos_dir.iterdir():
            if file.is_file():
                blob_name = f"certificados_cursos/{file.name}"
                if upload_file(str(file), blob_name):
                    uploaded += 1
                else:
                    failed += 1
    
    # Upload perfiles
    perfiles_dir = media_dir / 'perfiles'
    if perfiles_dir.exists():
        print("\n=== Uploading Profiles ===")
        for file in perfiles_dir.iterdir():
            if file.is_file():
                blob_name = f"perfiles/{file.name}"
                if upload_file(str(file), blob_name):
                    uploaded += 1
                else:
                    failed += 1
    
    print(f"\n=== Summary ===")
    print(f"Uploaded: {uploaded}")
    print(f"Failed: {failed}")

if __name__ == '__main__':
    upload_media_files()
