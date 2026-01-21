import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','Val.settings')
import django
django.setup()
from django.test import Client
c=Client()
resp=c.get('/hoja-de-vida/', HTTP_HOST='127.0.0.1')
print('status', resp.status_code)
html=resp.content.decode('utf-8')
start=html.find('class="d-flex justify-content-between align-items-center mb-4 no-print"')
print('found header?', start!=-1)
if start!=-1:
    snippet=html[start:start+400]
    print(snippet)
else:
    print(html[:400])
