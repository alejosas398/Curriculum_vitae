# 🚀 PASOS PARA RESOLVER EL PROBLEMA DE FOTOS EN RENDER

## El Problema
Las fotos en `https://curriculum-vitae-485k.onrender.com/hoja-de-vida/` aparecen en blanco (no se visualizan).

## ¿Qué fue el Problema?
1. En Render, el filesystem es **efímero** (se borra entre deployments)
2. Las fotos se guardaban localmente pero no persistían
3. No había configurado Azure Blob Storage como almacenamiento por defecto

## ✅ Cambios Implementados

He actualizado tu proyecto para usar **Azure Blob Storage** para todas las fotos. Los archivos modificados son:

### 1. `Val/settings.py`
- ✅ Añadido `DEFAULT_FILE_STORAGE` que usa Azure si está configurado
- ✅ Mejorada configuración de variables de Azure

### 2. `Val/azure_storage.py`
- ✅ Hecha más robusta la clase para manejar errors
- ✅ Verificado que el método `url()` funciona correctamente

### 3. `pagina_usuario/views.py`
- ✅ Actualizada función `descargar_cv_pdf()` para leer fotos desde Azure

### 4. `build.sh`
- ✅ Añadida migración automática de fotos a Azure durante el build

### 5. Archivo Nuevo: `migrate_local_photos_to_azure.py`
- ✅ Script para migrar fotos del filesystem a Azure manualmente

### 6. `Val/urls.py`
- ✅ Documentación mejorada

## 🔧 PRÓXIMOS PASOS (En Render)

### IMPORTANTE: Verifica tu Configuración de Azure ⚠️

Antes de hacer el deploy, asegúrate que en **Render → Environment Variables** tienes:

```
AZURE_STORAGE_CONNECTION_STRING = DefaultEndpointsProtocol=https;AccountName=xxx;AccountKey=yyy;EndpointSuffix=core.windows.net
AZURE_CONTAINER_NAME = media
```

O si prefieres simplemente:
```
AZURE_CONTAINER_NAME = media
AZURE_STORAGE_CONNECTION_STRING = <tu-connection-string>
```

### Paso 1: Push de Cambios a GitHub
```bash
git add .
git commit -m "Fix: Usar Azure Blob Storage para fotos - soluciona problema de visualización en Render"
git push origin main
```

### Paso 2: Redeployar en Render
1. Ve a https://dashboard.render.com
2. Selecciona tu servicio "curriculum-vitae"
3. Click en "Manual Deploy" o "Deploy latest"
4. Espera a que termine

### Paso 3: Verificar en los Logs
En Render, en la pestaña "Logs", busca mensajes como:
```
📊 Migración completada: X archivos migrados
```

### Paso 4: Verificar en la Web
Abre https://curriculum-vitae-485k.onrender.com/hoja-de-vida/

**La foto DEBE aparecer ahora** ✅

## 🔍 Si aún no aparecen las fotos...

### Problema Potencial 1: Azure no está configurado
**Solución**: Verifica que `AZURE_STORAGE_CONNECTION_STRING` está en Render

### Problema Potencial 2: Container de Azure no tiene acceso público
**Solución**: En Azure Portal:
1. Storage Account → Containers
2. Click en el container
3. Access Level → "Blob (anonymous read access)"

### Problema Potencial 3: Las fotos nunca se subieron
**Solución**: Sube una foto nueva en el panel:
1. https://curriculum-vitae-485k.onrender.com/perfil/editar/
2. Click en "Subir Foto"
3. Selecciona una foto
4. Guarda

## 📝 Resumen de Cambios Técnicos

| Archivo | Cambio |
|---------|--------|
| `Val/settings.py` | Añadido `DEFAULT_FILE_STORAGE` condicional |
| `Val/azure_storage.py` | Mejorada robustez |
| `pagina_usuario/views.py` | Detecta Azure y descarga fotos correctamente |
| `build.sh` | Migración automática de fotos |
| `Val/urls.py` | Mejorada documentación |

## ✨ Beneficios de esta Solución

✅ Las fotos persisten entre deployments
✅ Compatible con el filesystem local (modo desarrollo)
✅ Funciona automáticamente en Render
✅ Las fotos se sirven desde URLs de Azure (confiable)
✅ Fácil de escalar a múltiples usuarios

## 🆘 ¿Necesitas Ayuda?

Si algo sigue sin funcionar:
1. Revisa los logs en Render
2. Verifica las variables de entorno de Azure
3. Intenta subir una foto nueva manualmente
4. Contacta con soporte de Render o Azure

---

**¡Tu proyecto está listo!** 🎉
