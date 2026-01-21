import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Val.settings')
import django
django.setup()
from django.test import Client
from django.contrib.auth.models import User

u = User.objects.get(username='AnthonyTi')
print('Using user:', u.username)

c = Client()
c.force_login(u)
resp = c.get('/cv/descargar/', HTTP_HOST='127.0.0.1')
print('Status code:', resp.status_code)
if resp.status_code == 200:
    fname = f"combined_cv_{u.username}_test.pdf"
    with open(fname, 'wb') as f:
        f.write(resp.content)
    print(f'✓ Wrote {fname} ({len(resp.content)} bytes)')
else:
    print('✗ Response error:', resp.content[:200])
