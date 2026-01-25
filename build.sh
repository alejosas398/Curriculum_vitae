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
    python manage.py shell << 'EOF'
import os
import sys
from django.conf import settings
from pagina_usuario.models import Perfil, Experiencia, Curso, Recomendacion
from django.core.files.base import ContentFile

migrated = 0
errors = 0

try:
    # Migrate Perfil photos
    for perfil in Perfil.objects.all():
        if not perfil.foto:
            continue
        try:
            # Check if file exists in filesystem
            foto_path = getattr(perfil.foto, 'path', None)
            if foto_path and os.path.exists(foto_path):
                with open(foto_path, 'rb') as f:
                    file_content = f.read()
                file_name = os.path.basename(perfil.foto.name)
                perfil.foto.save(file_name, ContentFile(file_content), save=True)
                migrated += 1
        except Exception as e:
            errors += 1

    # Migrate Experiencia certificates
    for exp in Experiencia.objects.all():
        if not exp.certificado:
            continue
        try:
            cert_path = getattr(exp.certificado, 'path', None)
            if cert_path and os.path.exists(cert_path):
                with open(cert_path, 'rb') as f:
                    file_content = f.read()
                file_name = os.path.basename(exp.certificado.name)
                exp.certificado.save(file_name, ContentFile(file_content), save=True)
                migrated += 1
        except Exception:
            errors += 1

    # Migrate Curso certificates
    for curso in Curso.objects.all():
        if not curso.certificado:
            continue
        try:
            cert_path = getattr(curso.certificado, 'path', None)
            if cert_path and os.path.exists(cert_path):
                with open(cert_path, 'rb') as f:
                    file_content = f.read()
                file_name = os.path.basename(curso.certificado.name)
                curso.certificado.save(file_name, ContentFile(file_content), save=True)
                migrated += 1
        except Exception:
            errors += 1

    # Migrate Recomendacion certificates
    for rec in Recomendacion.objects.all():
        if not rec.certificado:
            continue
        try:
            cert_path = getattr(rec.certificado, 'path', None)
            if cert_path and os.path.exists(cert_path):
                with open(cert_path, 'rb') as f:
                    file_content = f.read()
                file_name = os.path.basename(rec.certificado.name)
                rec.certificado.save(file_name, ContentFile(file_content), save=True)
                migrated += 1
        except Exception:
            errors += 1

    print(f"\n📊 Migración completada: {migrated} archivos migrados, {errors} errores")
except Exception as e:
    print(f"⚠️  Error en migración: {str(e)}", file=sys.stderr)
EOF
else
    echo "⚠️  Azure no configurado, saltando migración de archivos"
fi

echo "✅ Build completado exitosamente!"

