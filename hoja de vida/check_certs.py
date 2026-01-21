import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','Val.settings')
import django
django.setup()

from django.contrib.auth.models import User
from pagina_usuario.models import Perfil, Experiencia, Curso, Recomendacion
from pagina_usuario.azure_blob import download_blob_bytes
from django.conf import settings

user = User.objects.first()
print(f"Usuario: {user.username}")
perfil = Perfil.objects.get(user=user)

# Verificar certificados
print("\n=== EXPERIENCIAS CON CERTIFICADO ===")
for exp in perfil.experiencias.all():
    if exp.certificado:
        print(f"ID: {exp.id}, Empresa: {exp.empresa}")
        print(f"  certificado.name: {exp.certificado.name}")
        print(f"  certificado.url: {exp.certificado.url}")
        print(f"  Archivo existe local: {os.path.exists(os.path.join(settings.MEDIA_ROOT, exp.certificado.name))}")
        # Intentar descargar desde Azure
        try:
            blob_content = download_blob_bytes(exp.certificado.name)
            print(f"  Descarga Azure (full path): {'Éxito' if blob_content else 'Falló'}")
        except Exception as e:
            print(f"  Error Azure: {e}")
        try:
            blob_content = download_blob_bytes(os.path.basename(exp.certificado.name))
            print(f"  Descarga Azure (basename): {'Éxito' if blob_content else 'Falló'}")
        except Exception as e:
            print(f"  Error Azure: {e}")

print("\n=== CURSOS CON CERTIFICADO ===")
for curso in perfil.cursos.all():
    if curso.certificado:
        print(f"ID: {curso.id}, Curso: {curso.nombre or curso.nombre_curso}")
        print(f"  certificado.name: {curso.certificado.name}")
        print(f"  certificado.url: {curso.certificado.url}")
        print(f"  Archivo existe local: {os.path.exists(os.path.join(settings.MEDIA_ROOT, curso.certificado.name))}")
        try:
            blob_content = download_blob_bytes(curso.certificado.name)
            print(f"  Descarga Azure (full path): {'Éxito' if blob_content else 'Falló'}")
        except Exception as e:
            print(f"  Error Azure: {e}")

print("\n=== RECOMENDACIONES CON CERTIFICADO ===")
for reco in perfil.recomendaciones.all():
    if reco.certificado:
        print(f"ID: {reco.id}, Contacto: {reco.nombre_contacto}")
        print(f"  certificado.name: {reco.certificado.name}")
        print(f"  certificado.url: {reco.certificado.url}")
        print(f"  Archivo existe local: {os.path.exists(os.path.join(settings.MEDIA_ROOT, reco.certificado.name))}")
        try:
            blob_content = download_blob_bytes(reco.certificado.name)
            print(f"  Descarga Azure (full path): {'Éxito' if blob_content else 'Falló'}")
        except Exception as e:
            print(f"  Error Azure: {e}")

print("\n=== CONEXIÓN AZURE ===")
print(f"Connection String: {settings.AZURE_STORAGE_CONNECTION_STRING[:50]}...")
print(f"Container: {settings.AZURE_CONTAINER_NAME}")
