import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','Val.settings')
import django
django.setup()

from django.contrib.auth.models import User
from pagina_usuario.models import Perfil

user = User.objects.get(username='AnthonyTi')
print(f"Usuario: {user.username}")
perfil = Perfil.objects.get(user=user)

from pagina_usuario.models import Experiencia, Curso, Recomendacion

print("\n=== EXPERIENCIAS CON CERTIFICADO ===")
for exp in perfil.experiencias.all():
    if exp.certificado:
        print(f"ID: {exp.id}, Empresa: {exp.empresa}, Certificado: {exp.certificado.name}")

print("\n=== CURSOS CON CERTIFICADO ===")
for curso in perfil.cursos.all():
    if curso.certificado:
        print(f"ID: {curso.id}, Curso: {curso.nombre or curso.nombre_curso}, Certificado: {curso.certificado.name}")

print("\n=== RECOMENDACIONES CON CERTIFICADO ===")
for reco in perfil.recomendaciones.all():
    if reco.certificado:
        print(f"ID: {reco.id}, Contacto: {reco.nombre_contacto}, Certificado: {reco.certificado.name}")

print("\n=== TOTALES ===")
print(f"Experiencias: {perfil.experiencias.count()}")
print(f"Cursos: {perfil.cursos.count()}")
print(f"Recomendaciones: {perfil.recomendaciones.count()}")
