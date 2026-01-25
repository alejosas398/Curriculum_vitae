# 🔍 Guía de Verificación: Configuración de Azure para Fotos

## Pre-requisitos
✅ Tienes acceso a Azure Portal
✅ Ya configuraste `AZURE_STORAGE_CONNECTION_STRING` en Render

## Verificación en Render

### 1. Revisar Variables de Entorno en Render
1. Ve a https://dashboard.render.com/services
2. Selecciona tu servicio "curriculum-vitae-485k"
3. Click en "Environment" en el menú izquierdo
4. Busca `AZURE_STORAGE_CONNECTION_STRING`
5. Debería tener un valor como: `DefaultEndpointsProtocol=https;AccountName=...`

✅ Si existe → Perfecto
❌ Si no existe → Necesitas agregarla

### 2. Ver los Logs durante el Deploy
1. En Render, ve a "Logs" (pestaña azul)
2. Haz un nuevo deploy: click en "Deploy latest"
3. Espera y busca en los logs:
   - `🚀 Iniciando migración de fotos a Azure...` (si está configurado)
   - `📊 Migración completada` (si la migración funcionó)
   - `⚠️  Azure no configurado, saltando migración` (si Azure no está en env vars)

## Verificación en Azure Portal

### 1. Verificar la Conexión Correcta
1. Ve a https://portal.azure.com
2. Busca tu Storage Account
3. Click en "Containers"
4. Busca un container llamado "media"

✅ Si existe el container → Bien configurado
❌ Si no existe → Necesitas crearlo o usar otro nombre

### 2. Verificar Permisos de Acceso
1. Click en el container "media"
2. Click en "Access Level" (o "Cambiar nivel de acceso")
3. Selecciona "Blob (anonymous read access for blobs only)"
4. Esto permite que las imágenes se vean públicamente

⚠️ IMPORTANTE: Sin esto, las fotos no se verán en la web

### 3. Verificar que hay archivos
1. En el mismo container "media"
2. Debería ver carpetas como:
   - `perfil_fotos/`
   - `certificados_cursos/`
   - `certificados_recomendaciones/`
   - etc.

✅ Si ves archivos → La migración funcionó
❌ Si está vacío → Los archivos aún no se migraron

## Verificación Local (Desarrollo)

Si quieres probar localmente con Azure:

### 1. Configura Variables de Entorno
En tu `.env` local:
```env
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=youraccount;AccountKey=yourkey;EndpointSuffix=core.windows.net
AZURE_CONTAINER_NAME=media
```

### 2. Prueba que Django detecta Azure
```bash
cd "hoja de vida"
python manage.py shell
```

En la shell de Django:
```python
from django.conf import settings
print(f"Storage: {settings.DEFAULT_FILE_STORAGE}")
print(f"Connection String: {settings.AZURE_STORAGE_CONNECTION_STRING[:50]}...")
print(f"Container: {settings.AZURE_CONTAINER_NAME}")
```

Deberías ver:
```
Storage: Val.azure_storage.AzureBlobStorage
Connection String: DefaultEndpointsProtocol=https;AccountName=...
Container: media
```

### 3. Prueba Subir un Archivo
```python
from pagina_usuario.models import Perfil
from django.core.files.base import ContentFile

perfil = Perfil.objects.first()  # o tu perfil
with open('test.jpg', 'rb') as f:
    perfil.foto.save('test.jpg', ContentFile(f.read()))

print(perfil.foto.url)  # Debería mostrar URL de Azure
```

## Solución de Problemas

### Problema: "No se puede conectar a Azure"
**Síntomas**: 
- Error en logs: `AZURE_STORAGE_CONNECTION_STRING not configured`
- Las fotos no aparecen

**Soluciones**:
1. ✅ Verifica que `AZURE_STORAGE_CONNECTION_STRING` está en Render (no `.env`)
2. ✅ Verifica que la connection string es válida (comienza con `DefaultEndpointsProtocol`)
3. ✅ Verifica que el Storage Account es el correcto en Azure

### Problema: "Container no existe"
**Síntomas**:
- Error en logs: `Container media not found`

**Soluciones**:
1. ✅ Ve a Azure Portal → Storage Account → Containers
2. ✅ Si no existe "media", créalo
3. ✅ O usa otro nombre y configura `AZURE_CONTAINER_NAME` en Render

### Problema: "Las imágenes no se ven pero están en Azure"
**Síntomas**:
- En Azure Portal ves los archivos
- Pero en la web aparecen en blanco/no cargan

**Soluciones**:
1. ✅ Verifica el nivel de acceso: debe ser "Blob (anonymous read access)"
2. ✅ Abre la URL directamente en el navegador:
   `https://youraccountname.blob.core.windows.net/media/perfil_fotos/...`
   Si no se carga, es un problema de permisos
3. ✅ Verifica CORS si necesitas acceso desde múltiples dominios

### Problema: "Migración de archivos no funcionó"
**Síntomas**:
- En logs: `0 archivos migrados`

**Soluciones**:
1. ✅ Verifica que hay fotos locales (en `hoja de vida/media/perfil_fotos/`)
2. ✅ Ejecuta la migración manual:
   ```bash
   cd "hoja de vida"
   python manage.py shell < migrate_local_photos_to_azure.py
   ```
3. ✅ Revisa los logs de error para mensajes específicos

## Checklist Final

Antes de decir que está listo:

- [ ] `AZURE_STORAGE_CONNECTION_STRING` está en Render (Environment)
- [ ] `AZURE_CONTAINER_NAME` está en Render (opcional, pero recomendado)
- [ ] El container existe en Azure Portal
- [ ] El container tiene acceso "Blob (anonymous read access)"
- [ ] Los logs muestran "Migración completada"
- [ ] Abres https://curriculum-vitae-485k.onrender.com/hoja-de-vida/
- [ ] La foto aparece correctamente
- [ ] Descargas el PDF y la foto aparece

Si todos los puntos están ✅ → ¡Problema resuelto! 🎉

## Links Útiles

- 🔗 [Azure Storage Containers](https://portal.azure.com/#blade/Microsoft_Azure_Storage/ContainersBlade)
- 🔗 [Render Dashboard](https://dashboard.render.com)
- 🔗 [Django Storage Backends](https://docs.djangoproject.com/en/6.0/topics/files/storage/)

---

**Recuerda**: Si necesitas ayuda, los logs de Render te dirán exactamente qué está pasando.
