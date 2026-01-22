# CHECKLIST DE MIGRACIONES - FOTOS EN RENDER

## ✅ Archivos Creados/Modificados

- [x] `Val/azure_storage.py` - Backend personalizado para Azure Blob Storage
- [x] `Val/settings.py` - Actualizado con configuración para Azure
- [x] `pagina_usuario/management/commands/migrate_media_to_azure.py` - Comando para migrar archivos
- [x] `pagina_usuario/migrations/0010_azure_media_support.py` - Nueva migración Django
- [x] `diagnose_media.py` - Script de diagnóstico
- [x] `AZURE_MEDIA_MIGRATIONS_README.md` - Documentación técnica
- [x] `MIGRACIONES_RESUMEN.md` - Resumen ejecutivo

## 📋 Pasos a Seguir en Render

### 1. Agregar Variables de Entorno (URGENTE ⚠️)

En **Render Dashboard**:
```
1. Ir a Settings → Environment Variables
2. Agregar:
   
   AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointProtocol=https;AccountName=XXX;AccountKey=XXX;EndpointSuffix=core.windows.net
   AZURE_CONTAINER_NAME=media
   DEBUG=False
```

**Dónde obtener estos valores:**
- Ir a Azure Portal
- Buscar "Storage Accounts"
- Seleccionar tu cuenta de storage
- Copiar "Connection string" en Settings → Access keys

### 2. Hacer Push a Render

```bash
git add .
git commit -m "Feat: Agregar Azure Blob Storage para media files en producción"
git push origin main
```

Render ejecutará automáticamente:
```bash
python manage.py migrate
```

### 3. Verificar que Funciona

1. **En Render**: Subir una foto de perfil
2. **Verificar**: Que aparezca en el sitio
3. **Si no aparece**: Revisar pasos de troubleshooting abajo

## 🔧 Pasos a Seguir en Local

### 1. Crear Directorio Media (si no existe)

```bash
mkdir -p media/perfil_fotos media/certificados media/certificados_cursos media/certificados_recomendaciones
```

### 2. Ejecutar Migraciones

```bash
python manage.py migrate
```

### 3. Probar Localmente

```bash
python manage.py runserver
# Ir a http://localhost:8000/admin
# Subir foto de perfil
# Verificar que aparezca en /media/perfil_fotos/
```

### 4. Diagnosticar (si hay problemas)

```bash
python diagnose_media.py
```

## 🆘 Troubleshooting

### Las fotos no aparecen en Render

**Paso 1: Verificar que Azure está configurado**
```bash
# En Render, revisar logs:
# Dashboard → Logs → buscar "AZURE"
```

**Paso 2: Migrar fotos existentes (si las hay)**
```bash
python manage.py migrate_media_to_azure --dry-run
python manage.py migrate_media_to_azure
```

**Paso 3: Revisar la base de datos**
```bash
python manage.py shell
>>> from pagina_usuario.models import Perfil
>>> p = Perfil.objects.first()
>>> print(p.foto)  # Debe mostrar un archivo
>>> print(p.foto_url)  # Debe ser URL de Azure
```

### Error "AZURE_STORAGE_CONNECTION_STRING not configured"

- Verificar que está en Environment Variables de Render
- Asegurarse de no tener espacios extras
- Hacer redeploy después de agregar la variable

### Error "azure-storage-blob not installed"

```bash
# Ya debe estar en requirements.txt, pero si no:
pip install azure-storage-blob
```

### Fotos locales se pierden al hacer deploy

**ESTO ES NORMAL EN RENDER** - Render no persiste datos locales

**Solución**: 
- Migrar a Azure ANTES de deployar a Render
- O empezar a usar Azure desde el primer deploy

## 📊 Validación Pre-Deploy

Antes de hacer push a Render:

```bash
# 1. Verificar que no hay errores de migración
python manage.py makemigrations
python manage.py migrate

# 2. Diagnosticar sistema
python diagnose_media.py

# 3. Verificar configuración local
python manage.py shell
>>> from django.conf import settings
>>> print(f"DEBUG: {settings.DEBUG}")
>>> print(f"MEDIA_URL: {settings.MEDIA_URL}")
>>> print(f"DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', 'NOT SET')}")
```

## 🚀 Comandos Útiles

### Migrar solo fotos de perfil
```bash
python manage.py migrate_media_to_azure --filter=perfil
```

### Migrar solo certificados
```bash
python manage.py migrate_media_to_azure --filter=curso
```

### Ver lo que se va a migrar sin hacer cambios
```bash
python manage.py migrate_media_to_azure --dry-run
```

### Diagnosticar completamente
```bash
python diagnose_media.py
```

## 📝 Notas Importantes

1. **Azure es REQUERIDO en Render** - Sin él, las fotos no persisten
2. **Local funciona sin Azure** - Settings detecta DEBUG y usa filesystem
3. **Nombres únicos** - Azure genera UUIDs para cada archivo, no hay conflictos
4. **URLs directas** - Las fotos se sirven directamente desde Azure, no desde Django
5. **Migración gradual** - Puedes migrar archivos sin parar la aplicación

## 🔐 Seguridad

- [ ] No compartir `AZURE_STORAGE_CONNECTION_STRING` públicamente
- [ ] Usar solo en variables de entorno, nunca en código
- [ ] Rotar keys periódicamente en Azure
- [ ] Usar HTTPS (Render lo fuerza automáticamente)

## 📞 Si Sigue Sin Funcionar

1. Ejecutar: `python diagnose_media.py`
2. Revisar: `AZURE_MEDIA_MIGRATIONS_README.md`
3. Revisar logs de Render
4. Verificar que Azure Storage account existe y tiene permisos
5. Probar en local primero antes de Render

## ✨ Confirmación Final

Cuando las fotos aparezcan en Render:
- [ ] Subir foto de perfil
- [ ] Verificar que aparece en el sitio
- [ ] Verificar que persiste después de refresh
- [ ] Verificar que persiste después de que Render reinicia

¡ÉXITO! 🎉

---

**Última actualización**: 22 Enero 2026
**Responsable**: Sistema de Migraciones Django
