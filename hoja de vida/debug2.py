import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Val.settings')
import django
django.setup()

from django.contrib.auth.models import User, AnonymousUser
from django.test import RequestFactory
from pagina_usuario.views import ver_hoja_de_vida
from pagina_usuario.models import Perfil

# Simular un request anónimo
factory = RequestFactory()
request = factory.get('/hoja-de-vida/')
request.user = AnonymousUser()

# Llamar la vista
print("=== PRUEBA DE VISTA ===")
print(f"Usuario en request: {request.user}")
print(f"¿Es autenticado? {request.user.is_authenticated}")

# Obtener contexto sin renderizar
from django.template.response import TemplateResponse
response = ver_hoja_de_vida(request)
context = response.context_data if hasattr(response, 'context_data') else response.context

print(f"\nContexto pasado a template:")
print(f"  perfil: {context.get('perfil')}")
print(f"  proyectos_productos count: {len(context.get('proyectos_productos', []))}")
print(f"  ventas_garage count: {len(context.get('ventas_garage', []))}")
print(f"  es_propietario: {context.get('es_propietario')}")

if context.get('proyectos_productos'):
    print(f"\n  Proyectos:")
    for p in context.get('proyectos_productos'):
        print(f"    - {p.titulo} (activo={p.activo})")
