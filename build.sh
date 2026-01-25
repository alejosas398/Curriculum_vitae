#!/bin/bash
set -o errexit

# Determinar el directorio base
if [ -d "hoja de vida" ]; then
    cd "hoja de vida"
    REQ_PATH="../requirements.txt"
else
    REQ_PATH="requirements.txt"
fi

# Install Python dependencies
pip install -r $REQ_PATH

# Run database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Migrate media files to Azure if configured
if [ -n "$AZURE_STORAGE_CONNECTION_STRING" ]; then
    echo "🗄️  Migrando archivos a Azure Blob Storage..."
    python manage.py shell << EOF
import os
from django.conf import settings
from pagina_usuario.models import Perfil, Experiencia, Curso, Recomendacion
from django.core.files.base import ContentFile

migrated = 0
errors = 0

# Migrate Perfil photos
for perfil in Perfil.objects.all():
    if perfil.foto and hasattr(perfil.foto, 'path') and os.path.exists(perfil.foto.path):
        try:
            with open(perfil.foto.path, 'rb') as f:
                file_content = f.read()
            file_name = os.path.basename(perfil.foto.name)
            perfil.foto.save(file_name, ContentFile(file_content), save=True)
            migrated += 1
            print(f"✅ Migrada foto de {perfil.user.username}")
        except Exception as e:
            errors += 1
            print(f"❌ Error migrando {perfil.user.username}: {str(e)}")

# Migrate certificates
for exp in Experiencia.objects.filter(certificado__isnull=False):
    if hasattr(exp.certificado, 'path') and os.path.exists(exp.certificado.path):
        try:
            with open(exp.certificado.path, 'rb') as f:
                file_content = f.read()
            file_name = os.path.basename(exp.certificado.name)
            exp.certificado.save(file_name, ContentFile(file_content), save=True)
            migrated += 1
        except: errors += 1

for curso in Curso.objects.filter(certificado__isnull=False):
    if hasattr(curso.certificado, 'path') and os.path.exists(curso.certificado.path):
        try:
            with open(curso.certificado.path, 'rb') as f:
                file_content = f.read()
            file_name = os.path.basename(curso.certificado.name)
            curso.certificado.save(file_name, ContentFile(file_content), save=True)
            migrated += 1
        except: errors += 1

for rec in Recomendacion.objects.filter(certificado__isnull=False):
    if hasattr(rec.certificado, 'path') and os.path.exists(rec.certificado.path):
        try:
            with open(rec.certificado.path, 'rb') as f:
                file_content = f.read()
            file_name = os.path.basename(rec.certificado.name)
            rec.certificado.save(file_name, ContentFile(file_content), save=True)
            migrated += 1
        except: errors += 1

print(f"\n📊 Migración completada: {migrated} archivos migrados, {errors} errores")
EOF
else
    echo "⚠️  Azure no configurado, saltando migración de archivos"
fi

echo "✅ Build completado exitosamente!"

