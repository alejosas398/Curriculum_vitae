#!/bin/bash

# Script de build para Render - se ejecuta automáticamente en cada deploy

echo "🚀 Iniciando build personalizado..."

# Cambiar al directorio correcto
cd "hoja de vida" || exit 1

echo "📦 Instalando dependencias..."
pip install -r ../requirements.txt

echo "🗄️  Aplicando migraciones..."
python manage.py migrate

echo "📸 Migrando fotos a Azure (si están configuradas las variables)..."
if [ -n "$AZURE_STORAGE_CONNECTION_STRING" ] && [ -n "$AZURE_CONTAINER_NAME" ]; then
    echo "Azure configurado, ejecutando migración de fotos..."
    python manage.py migrate_photos
else
    echo "Azure no configurado, omitiendo migración de fotos"
fi

echo "🎨 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput --clear

echo "✅ Build completado exitosamente!"