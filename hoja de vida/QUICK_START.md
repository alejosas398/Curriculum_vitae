# GUÍA RÁPIDA - Fotos en Render

## Problema
Las fotos de perfil desaparecen en Render porque el filesystem es efímero.

## Solución
Usar Azure Blob Storage para guardar archivos.

## PASOS RÁPIDOS (5 minutos)

### 1. En Azure Portal
```
Storage Accounts → Tu cuenta → Settings → Access Keys
Copiar: Connection String
```

### 2. En Render Dashboard
```
Settings → Environment Variables → Agregar:
AZURE_STORAGE_CONNECTION_STRING=<pegar valor de arriba>
AZURE_CONTAINER_NAME=media
DEBUG=False
```

### 3. En Terminal (Local)
```bash
cd "ruta/al/proyecto"
python manage.py migrate
git add .
git commit -m "Fix: Azure Blob Storage para media files"
git push origin main
```

### 4. Esperar a que Render haga deploy
```
Render → Logs → Ver "Build completed successfully"
```

### 5. Probar
```
Ir a https://tudominio.onrender.com/
Subir foto de perfil
Verificar que aparezca
```

## Si No Funciona

```bash
# En local
python diagnose_media.py

# Ver qué dice y corregir
```

## Archivos Nuevos

- `Val/azure_storage.py` - Backend Azure
- `diagnose_media.py` - Script diagnóstico
- `CHECKLIST_DEPLOYMENT.md` - Checklist completo

Lee ese si tienes problemas.

## Más Info

Ver: `AZURE_MEDIA_MIGRATIONS_README.md`

---
¡Listo! Las fotos ahora persistirán en Render. 🎉
