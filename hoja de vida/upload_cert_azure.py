import os
from pathlib import Path
os.environ.setdefault('DJANGO_SETTINGS_MODULE','Val.settings')
import django
django.setup()

from django.conf import settings
from django.contrib.auth.models import User
from pagina_usuario.models import Curso
from azure.storage.blob import BlobServiceClient

media_root = settings.MEDIA_ROOT
print(f"MEDIA_ROOT: {media_root}")

# Buscar el certificado
cert_name = "certificados_cursos/CERTIFICADO_FREDY_MORENO_eytYOIh.pdf"
local_path = os.path.join(media_root, cert_name)

print(f"\nBuscando: {local_path}")
if os.path.exists(local_path):
    print("✓ Archivo existe localmente")
    file_size = os.path.getsize(local_path)
    print(f"  Tamaño: {file_size} bytes")
    
    # Subir a Azure
    try:
        conn_str = settings.AZURE_STORAGE_CONNECTION_STRING
        container = settings.AZURE_CONTAINER_NAME
        
        svc = BlobServiceClient.from_connection_string(conn_str)
        blob_client = svc.get_blob_client(container=container, blob=cert_name)
        
        with open(local_path, 'rb') as f:
            blob_client.upload_blob(f, overwrite=True)
        print(f"✓ Subido a Azure en: {container}/{cert_name}")
    except Exception as e:
        print(f"✗ Error Azure: {e}")
else:
    print("✗ Archivo NO existe localmente")
    
# Ahora verificar si se puede descargar
print("\nVerificando descarga desde Azure...")
try:
    from pagina_usuario.azure_blob import download_blob_bytes
    content = download_blob_bytes(cert_name)
    if content:
        print(f"✓ Descargado desde Azure: {len(content)} bytes")
    else:
        print("✗ No se pudo descargar (None)")
except Exception as e:
    print(f"✗ Error: {e}")
