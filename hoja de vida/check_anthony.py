import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Val.settings')
import django
django.setup()

from django.contrib.auth.models import User
from pagina_usuario.models import Perfil

user = User.objects.get(username='AnthonyTi')
perfil = Perfil.objects.get(user=user)
print(f'Usuario: {user.username}')
print(f'Productos: {perfil.productos.count()}')
print(f'Ventas Garage: {perfil.ventas_garage.count()}')
print(f'Experiencias: {perfil.experiencias.count()}')
print(f'Educaciones: {perfil.educaciones.count()}')
