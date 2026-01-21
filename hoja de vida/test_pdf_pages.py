import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Val.settings')
import django
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from pypdf import PdfReader
from io import BytesIO

u = User.objects.get(username='AnthonyTi')
print(f'Testing with user: {u.username}\n')

# Verificar qué certificados tiene
from pagina_usuario.models import Perfil
perfil = Perfil.objects.get(user=u)
print('=== CERTIFICADOS EN BD ===')
certs_count = 0
for exp in perfil.experiencias.all():
    if exp.certificado:
        print(f'Experiencia: {exp.empresa} - {exp.certificado.name}')
        certs_count += 1
for curso in perfil.cursos.all():
    if curso.certificado:
        print(f'Curso: {curso.nombre} - {curso.certificado.name}')
        certs_count += 1
for reco in perfil.recomendaciones.all():
    if reco.certificado:
        print(f'Recomendación: {reco.nombre_contacto} - {reco.certificado.name}')
        certs_count += 1
print(f'Total certificados: {certs_count}\n')

# Descargar PDF
c = Client()
c.force_login(u)
resp = c.get('/cv/descargar/', HTTP_HOST='127.0.0.1')
print(f'HTTP Status: {resp.status_code}')

if resp.status_code == 200:
    # Analizar el PDF
    try:
        reader = PdfReader(BytesIO(resp.content))
        num_pages = len(reader.pages)
        print(f'Páginas en PDF: {num_pages}')
        print(f'Tamaño: {len(resp.content) / 1024:.1f} KB')
        
        if num_pages > 1:
            print('✓ PDF contiene múltiples páginas (CV + certificados)')
        else:
            print('✗ PDF tiene solo 1 página (sin certificados)')
    except Exception as e:
        print(f'Error al leer PDF: {e}')
        
    # Guardar para inspección manual
    with open('test_download_debug.pdf', 'wb') as f:
        f.write(resp.content)
    print('\nGuardado como: test_download_debug.pdf')
else:
    print(f'Error: {resp.status_code}')
    print(resp.content[:500])
