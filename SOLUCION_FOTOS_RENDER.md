# 📸 Solución: Fotos No Visibles en Render

## Problema
Las fotos de perfil no se visualizan en https://curriculum-vitae-485k.onrender.com/hoja-de-vida/ en Render (producción).

### Raíces del Problema
1. **Sistema de archivos efímero en Render**: Los archivos locales se pierden entre deployments
2. **DEBUG=False en producción**: Las URLs de media (`/media/`) no se sirven cuando DEBUG es False
3. **Falta de configuración de Azure Storage**: El `DEFAULT_FILE_STORAGE` no estaba configurado para usar Azure Blob Storage

## Solución Implementada

### 1️⃣ Configuración de DEFAULT_FILE_STORAGE
**Archivo**: `Val/settings.py`

```python
# Usar Azure storage si las credenciales están disponibles
if AZURE_STORAGE_CONNECTION_STRING:
    DEFAULT_FILE_STORAGE = 'Val.azure_storage.AzureBlobStorage'
else:
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
```

### 2️⃣ Clase de Storage Mejorada
**Archivo**: `Val/azure_storage.py`

- ✅ Método `url()` implementado correctamente
- ✅ Manejo robusto cuando Azure no está configurado
- ✅ Soporta lectura y escritura de archivos en Azure Blob

### 3️⃣ Actualización de Vistas
**Archivo**: `pagina_usuario/views.py` - Función `descargar_cv_pdf()`

```python
# Ahora detecta si está usando Azure y descarga la foto apropiadamente
if 'azure' in settings.DEFAULT_FILE_STORAGE.lower():
    # Lee desde Azure Blob Storage via URL
    response = requests.get(foto_url, timeout=10)
    foto_data = response.content
else:
    # Lee desde filesystem local
    with open(perfil.foto.path, 'rb') as f:
        foto_data = f.read()
```

### 4️⃣ Scripts de Migración
**Archivo**: `migrate_local_photos_to_azure.py`

Script para migrar todos los archivos locales a Azure:
```bash
python manage.py shell < migrate_local_photos_to_azure.py
```

### 5️⃣ Build Script Automático
**Archivo**: `build.sh`

Ahora el build automaticamente migra archivos a Azure si está configurado:
```bash
if [ -n "$AZURE_STORAGE_CONNECTION_STRING" ]; then
    # Ejecuta migración...
fi
```

## ¿Qué hacer Ahora?

### Opción A: Redeployar en Render (Recomendado)
1. Asegúrate que estas variables de entorno están configuradas en Render:
   - `AZURE_STORAGE_CONNECTION_STRING` ✅
   - `AZURE_CONTAINER_NAME` (opcional, default: 'media')

2. Haz un push de los cambios a GitHub
3. Trigger un nuevo deploy en Render

El build script automáticamente migrará las fotos a Azure.

### Opción B: Migración Manual
Si necesitas migrar archivos sin redeployar:

```bash
cd "hoja de vida"
python manage.py shell
```

Luego en la shell:
```python
exec(open('migrate_local_photos_to_azure.py').read())
```

## Verificación ✅

Después del deploy, verifica:

1. **En la web**: https://curriculum-vitae-485k.onrender.com/hoja-de-vida/
   - La foto debería aparecer

2. **En los logs de Render**:
   - Busca `📊 Migración completada` para confirmar que funcionó

3. **Descargar CV PDF**:
   - La foto debería aparecer en el PDF descargado

## Detalles Técnicos

### URL de Azure Blob Storage
Las fotos ahora se sirven desde URLs como:
```
https://<account_name>.blob.core.windows.net/media/perfil_fotos/photo_xxxxx.jpg
```

### Compatibilidad Backwards
- ✅ Si Azure no está configurado, sigue usando filesystem local
- ✅ El código detecta automáticamente qué storage está en uso
- ✅ Los templates existentes funcionan sin cambios

### Seguridad
⚠️ Importante: Asegurate que el container de Azure tiene acceso público (Anonymous) para que las imágenes se muestren. Si necesitas privacidad, usa SAS tokens.

Para hacer el container público:
1. Azure Portal → Storage Account → Containers
2. Click en el container → Access Level
3. Selecciona "Blob (anonymous read access for blobs only)"

## Archivos Modificados
- ✅ `Val/settings.py` - DEFAULT_FILE_STORAGE
- ✅ `Val/azure_storage.py` - Clase mejorada
- ✅ `Val/urls.py` - Claridad en comentarios
- ✅ `pagina_usuario/views.py` - descargar_cv_pdf mejorado
- ✅ `build.sh` - Migración automática
- ✅ `migrate_local_photos_to_azure.py` - Script de migración (nuevo)
