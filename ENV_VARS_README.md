# Variables de Entorno para Render

## Variables Esenciales (Requeridas)

```bash
# Base de datos PostgreSQL (proporcionada automáticamente por Render)
DATABASE_URL=postgresql://...

# Configuración de Django
SECRET_KEY=tu_clave_secreta_muy_larga_y_segura
DEBUG=False
ALLOWED_HOSTS=curriculum-vitae-485k.onrender.com

# Azure Blob Storage (para fotos y archivos)
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=tu_cuenta;AccountKey=tu_clave;EndpointSuffix=core.windows.net
AZURE_CONTAINER_NAME=cursos
```

## Variables Opcionales de Control

```bash
# Control de migración automática de fotos
AUTO_MIGRATE_PHOTOS=True  # Por defecto: True

# Logging detallado durante build
VERBOSE_BUILD=False  # Por defecto: False

# Timeout para operaciones de Azure (segundos)
AZURE_TIMEOUT=30  # Por defecto: 30
```

## Variables de Producción Adicionales

```bash
# Seguridad HTTPS
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Configuración de email (opcional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_password_app
```

## Configuración en Render

1. Ve a tu **Render Dashboard**
2. Selecciona tu servicio web
3. Ve a **Environment**
4. Agrega las variables una por una

## Comandos de Build Automáticos

El script `build.sh` ejecuta automáticamente:

1. ✅ Instalación de dependencias
2. ✅ Migraciones de base de datos
3. ✅ Migración de fotos a Azure (si está configurado)
4. ✅ Recolección de archivos estáticos

## Verificación

Para verificar que todo funciona:

```bash
# Ver logs de build en Render Dashboard > Logs
# O conecta por SSH y ejecuta:
python manage.py check
python manage.py migrate_photos --help
```

