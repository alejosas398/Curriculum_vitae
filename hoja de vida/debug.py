import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Val.settings')
import django
django.setup()

from pagina_usuario.models import Perfil
from django.contrib.auth.models import User

print('=== USUARIOS ===')
for u in User.objects.all():
    print(f'  {u.id}: {u.username}')

print('\n=== PERFILES ===')
for p in Perfil.objects.all():
    username = p.user.username if p.user else 'NULL'
    print(f'  {p.id}: user_id={p.user_id} ({username}) - productos={p.productos.count()}')
