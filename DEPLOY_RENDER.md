# Hoja de Vida Digital - Guía de Deploy en Render

## Requisitos Previos
- Cuenta en [Render.com](https://render.com)
- Código en un repositorio Git (GitHub, GitLab, Bitbucket)
- Credenciales de Azure Blob Storage

---

## Paso 1: Preparar el Repositorio Git

```bash
cd c:\Users\HP\Downloads\prueba
git init
git add .
git commit -m "Initial commit - Hoja de Vida App"
git remote add origin https://github.com/tu-usuario/tu-repositorio.git
git push -u origin main
```

---

## Paso 2: Crear Service en Render

### 2.1 Crear Web Service
1. Ir a [Render Dashboard](https://dashboard.render.com)
2. Clic en **"New +"** → **"Web Service"**
3. Conectar tu repositorio de GitHub
4. Llenar los datos:
   - **Name**: `hoja-de-vida`
   - **Environment**: `Python 3`
   - **Build Command**: `chmod +x build.sh && ./build.sh`
   - **Start Command**: `gunicorn Val.wsgi --chdir "hoja de vida" --bind 0.0.0.0:$PORT`
   - **Plan**: Gratuito (Free) o Paid según necesites

### 2.2 Agregar Variables de Entorno
En Render Dashboard → Tu servicio → **Environment**:

```
SECRET_KEY=django-insecure-xxxxxxxxxxxxxxxxxxxxx
DEBUG=False
ALLOWED_HOSTS=tu-servicio.onrender.com

AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=hojavidaanthony;AccountKey=...;EndpointSuffix=core.windows.net
AZURE_CONTAINER_NAME=cursos
```

### 2.3 Crear Base de Datos PostgreSQL (Opcional pero Recomendado)
1. **"New +"** → **"PostgreSQL"**
2. Anotar la URL de conexión (se añade automáticamente como `DATABASE_URL`)

---

## Paso 3: Variables de Entorno en Render

En **Settings** del Web Service, copia estas variables:

| Variable | Valor |
|----------|-------|
| `SECRET_KEY` | Genera una con: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `tu-servicio.onrender.com` |
| `AZURE_STORAGE_CONNECTION_STRING` | Tu connection string de Azure |
| `AZURE_CONTAINER_NAME` | `cursos` |

---

## Paso 4: Verificar Deploy

1. Render comenzará el build automáticamente
2. Ver logs en **Logs** del servicio
3. Si hay errores, revisar:
   - `build.sh` permisos
   - `requirements.txt` versiones
   - Variables de entorno correctas

---

## Paso 5: Crear Super Usuario en Render

Una vez desplegado, ejecuta en Render Shell:

```bash
python "hoja de vida"/manage.py createsuperuser
```

O via SSH (si está disponible en tu plan):

```bash
ssh -i ~/.ssh/render_key render@tu-servicio.onrender.com
cd /etc/render/hoja-de-vida
python manage.py createsuperuser
```

---

## URLs Importantes

- **Aplicación**: `https://tu-servicio.onrender.com/`
- **Admin**: `https://tu-servicio.onrender.com/admin/`
- **Hoja de Vida**: `https://tu-servicio.onrender.com/hoja-de-vida/`

---

## Solución de Problemas

### Error: "No such file or directory: 'hoja de vida'"
Asegurar que `build.sh` y `Procfile` tengan la ruta correcta.

### Error: "ModuleNotFoundError: No module named 'weasyprint'"
Ejecutar en local y push nuevamente para que Render instale.

### Error: "Database connection failed"
Verificar que `DATABASE_URL` esté configurada en variables de entorno.

### Error: "Azure credentials not found"
Verificar `AZURE_STORAGE_CONNECTION_STRING` y `AZURE_CONTAINER_NAME`.

---

## Actualizar Código

Para actualizar la aplicación:

```bash
git add .
git commit -m "Update: descripción de cambios"
git push origin main
```

Render redesplegará automáticamente.

---

## Datos Iniciales

Para insertar usuarios de prueba en producción:

```bash
python manage.py shell
```

Luego ejecutar:
```python
from django.contrib.auth.models import User
User.objects.create_superuser('admin', 'admin@example.com', 'password123')
```

---

**¡Listo! Tu app está en Render.** 🚀
