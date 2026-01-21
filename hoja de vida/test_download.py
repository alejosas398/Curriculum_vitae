import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Val.settings')
import django
django.setup()
from django.test import Client
from django.contrib.auth.models import User

try:
    u = User.objects.get(username='marti')
except Exception:
    u = User.objects.first()
print('Using user:', u.username)

c = Client()
# Force login avoids needing password
c.force_login(u)
# Use a valid Host header to satisfy ALLOWED_HOSTS
resp = c.get('/cv/descargar/', HTTP_HOST='127.0.0.1')
print('Status code:', resp.status_code)
if resp.status_code == 200:
    fname = f"combined_cv_{u.username}.pdf"
    with open(fname, 'wb') as f:
        f.write(resp.content)
    print('Wrote', fname)
else:
    print('Response length:', len(resp.content))
    print(resp.content[:200])
