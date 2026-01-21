import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','Val.settings')
import django
django.setup()

from django.conf import settings
from azure.storage.blob import BlobServiceClient

conn_str = settings.AZURE_STORAGE_CONNECTION_STRING
container = settings.AZURE_CONTAINER_NAME

print(f"Conexión Azure:")
print(f"  Storage Account: {conn_str[conn_str.find('AccountName=')+12:conn_str.find('AccountKey=')-1]}")
print(f"  Container: {container}")

svc = BlobServiceClient.from_connection_string(conn_str)

# Crear el container
try:
    svc.create_container(name=container)
    print(f"✓ Container '{container}' creado")
except Exception as e:
    if "ContainerAlreadyExists" in str(e):
        print(f"✓ Container '{container}' ya existe")
    else:
        print(f"✗ Error: {e}")

# Ahora subir el certificado
media_root = settings.MEDIA_ROOT
cert_name = "certificados_cursos/CERTIFICADO_FREDY_MORENO_eytYOIh.pdf"
local_path = os.path.join(media_root, cert_name)

if os.path.exists(local_path):
    print(f"\nSubiendo certificado...")
    try:
        blob_client = svc.get_blob_client(container=container, blob=cert_name)
        with open(local_path, 'rb') as f:
            blob_client.upload_blob(f, overwrite=True)
        print(f"✓ Subido: {container}/{cert_name}")
    except Exception as e:
        print(f"✗ Error: {e}")
else:
    print(f"✗ Archivo no encontrado: {local_path}")
