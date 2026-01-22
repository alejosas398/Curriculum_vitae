# Solución: Migraciones para Fotos de Perfil en Render

## Problema
Las fotos de perfil no aparecen en Render (producción) porque:
1. Render tiene un sistema de archivos efímero que se limpia después de cada deploy
2. Los archivos media guardados localmente se pierden con cada reinicio
3. No había configuración para usar Azure Blob Storage automáticamente en producción

## Solución Implementada

### 1. **Nuevo Backend de Almacenamiento Azure** (`Val/azure_storage.py`)
- Clase `AzureBlobStorage` que implementa la interfaz de Django Storage
- Compatible con ImageField y FileField de Django
- Maneja automáticamente:
  - Upload de archivos a Azure Blob Storage
  - Generación de URLs directas desde Azure
  - Tipos MIME automáticos
  - Nombres únicos para evitar conflictos

### 2. **Actualización de Settings** (`Val/settings.py`)
```python
# En producción (DEBUG=False):
if not DEBUG and AZURE_STORAGE_CONNECTION_STRING:
    DEFAULT_FILE_STORAGE = 'Val.azure_storage.AzureBlobStorage'

# En local (DEBUG=True):
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
```

### 3. **Comando de Migración** (`pagina_usuario/management/commands/migrate_media_to_azure.py`)
Ayuda a migrar archivos existentes a Azure:
```bash
# Ver qué se migvaría (sin hacer cambios)
python manage.py migrate_media_to_azure --dry-run

# Migrar solo fotos de perfil
python manage.py migrate_media_to_azure --filter=perfil

# Migrar todos los archivos media
python manage.py migrate_media_to_azure
```

### 4. **Nueva Migración Django** (`0010_azure_media_support.py`)
Marca el punto en el que Azure storage está soportado

## Pasos para Activar

### En Render (Producción):

1. **Configurar variables de entorno en Render Dashboard**:
   ```
   AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointProtocol=https;AccountName=...
   AZURE_CONTAINER_NAME=media
   DEBUG=False
   ```

2. **Ejecutar las migraciones** (Render lo hace automáticamente en el build):
   ```bash
   python manage.py migrate
   ```

3. **Opcionalmente, migrar archivos existentes a Azure** (antes del primer deploy):
   ```bash
   python manage.py migrate_media_to_azure
   ```

### En Local (Desarrollo):

1. No se requiere Azure configurado
2. Las fotos se guardan en `media/perfil_fotos/`
3. Se sirven a través de `/media/...` URL

## Ventajas

✅ **Persistencia**: Los archivos se guardan en Azure, no en el sistema de archivos efímero de Render
✅ **Escalabilidad**: Azure Blob Storage es escalable y rápido
✅ **Compatible**: Funciona con Django's ImageField sin cambios en modelos
✅ **Fallback**: En local sigue usando sistema de archivos normal
✅ **Migración gradual**: Puedes migrar archivos existentes sin parar la aplicación

## Posibles Problemas y Soluciones

### Las fotos aún no aparecen después del deploy

1. **Verificar que Azure está configurado**:
   ```bash
   python manage.py shell
   >>> from django.conf import settings
   >>> print(settings.AZURE_STORAGE_CONNECTION_STRING)  # Debe tener valor
   >>> print(settings.DEFAULT_FILE_STORAGE)  # Debe ser 'Val.azure_storage.AzureBlobStorage'
   ```

2. **Migrar archivos existentes**:
   ```bash
   python manage.py migrate_media_to_azure
   ```

3. **Verificar logs en Render**:
   ```bash
   # En Render dashboard -> Logs
   # Buscar errores de Azure
   ```

### Errores de Azure
- `AZURE_STORAGE_CONNECTION_STRING must be configured`: Agregar la variable de entorno
- `Blob not found`: El archivo no existe en Azure, correr migrate_media_to_azure

## Flujo Automático de Fotos

1. **Usuario sube foto** → ImageField guarda directamente en Azure (en prod)
2. **Vista renderiza perfil** → foto_url usa la URL de Azure automáticamente
3. **Template muestra imagen** → Se carga desde Azure directly

## URLs de Fotos

- **En local**: `http://localhost:8000/media/perfil_fotos/nombre.jpg`
- **En Render**: `https://tuaccount.blob.core.windows.net/media/perfil_fotos/uuid.jpg`

## Próximos Pasos (Opcional)

1. Implementar compresión de imágenes en Azure
2. Usar CDN (Azure CDN) para servir imágenes más rápido
3. Limpiar archivos huérfanos en Azure
4. Implementar versionado de archivos

## Referencias

- [Django Storage API](https://docs.djangoproject.com/en/6.0/ref/files/storage/)
- [Azure Blob Storage SDK](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/storage/azure-storage-blob)
- [Render Environment Variables](https://render.com/docs/environment-variables)
