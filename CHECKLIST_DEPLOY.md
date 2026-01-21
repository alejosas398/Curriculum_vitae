# ✅ CHECKLIST DE DEPLOY - HOJA DE VIDA

## 1. Verificación Local
- [ ] El servidor Django corre sin errores: `python manage.py runserver`
- [ ] PDF se descarga correctamente con fotos
- [ ] Certificados se anexan al PDF
- [ ] Azure Blob Storage conectado
- [ ] Admin funciona correctamente
- [ ] Media files se sirven correctamente

## 2. Configuración de Archivos
- [x] `requirements.txt` actualizado con todas las dependencias
- [x] `Procfile` creado para Render
- [x] `build.sh` creado y con permisos de ejecución
- [x] `runtime.txt` especifica Python 3.13.3
- [x] `.env.example` creado con variables plantilla
- [x] `.gitignore` incluye `.env`, `db.sqlite3`, `venv/`, `media/`, `staticfiles/`

## 3. Django Settings (settings.py)
- [x] `ALLOWED_HOSTS` configurable via variables de entorno
- [x] `DEBUG = False` en producción
- [x] `SECRET_KEY` configurable via variables de entorno
- [x] HTTPS redirect habilitado en producción
- [x] WhiteNoise middleware agregado para archivos estáticos
- [x] PostgreSQL soportado (dj-database-url)
- [x] Azure Storage configurado

## 4. Git & Repositorio
- [ ] Repositorio inicializado: `git init`
- [ ] Todo commiteado: `git add . && git commit -m "Initial commit"`
- [ ] Remoto agregado: `git remote add origin <URL>`
- [ ] Push a GitHub/GitLab: `git push -u origin main`

## 5. Render Dashboard
- [ ] Crear Web Service desde repositorio
- [ ] Build Command: `chmod +x build.sh && ./build.sh`
- [ ] Start Command: `gunicorn Val.wsgi --chdir "hoja de vida" --bind 0.0.0.0:$PORT`
- [ ] Variables de entorno configuradas:
  - [ ] `SECRET_KEY` (generar nueva)
  - [ ] `DEBUG=False`
  - [ ] `ALLOWED_HOSTS=tu-dominio.onrender.com`
  - [ ] `AZURE_STORAGE_CONNECTION_STRING`
  - [ ] `AZURE_CONTAINER_NAME=cursos`
  - [ ] `DATABASE_URL` (si usas PostgreSQL de Render)

## 6. PostgreSQL en Render (Opcional)
- [ ] Crear PostgreSQL en Render
- [ ] Variable `DATABASE_URL` se añade automáticamente
- [ ] URL de conexión anotada

## 7. Verificación Post-Deploy
- [ ] Build completado sin errores
- [ ] Sitio accesible en `https://tu-servicio.onrender.com/`
- [ ] Admin accesible en `/admin/`
- [ ] Hoja de vida se carga en `/hoja-de-vida/`
- [ ] PDF descarga funciona
- [ ] Certificados anexados correctamente
- [ ] Fotos de perfil se muestran en PDF
- [ ] Azure storage accesible

## 8. Datos Iniciales
- [ ] Super usuario creado en Render
- [ ] Usuarios de prueba creados
- [ ] Certificados cargados en Azure

## 9. Monitoreo
- [ ] Logs habilitados en Render
- [ ] Errores 500 monitoreados
- [ ] Performance de PDF generation aceptable

---

## Variables de Entorno Requeridas en Render

```
SECRET_KEY=django-insecure-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
DEBUG=False
ALLOWED_HOSTS=hoja-de-vida.onrender.com

AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=hojavidaanthony;AccountKey=xxxxx;EndpointSuffix=core.windows.net
AZURE_CONTAINER_NAME=cursos

# Si usas PostgreSQL en Render (se genera automáticamente)
DATABASE_URL=postgresql://usuario:contraseña@host:5432/nombre_db
```

---

## Comandos Útiles Post-Deploy

```bash
# Ver logs
render logs -s hoja-de-vida

# Crear superusuario (en Render Shell)
python manage.py createsuperuser

# Ejecutar migraciones (si no se hacen automáticamente)
python manage.py migrate

# Recolectar archivos estáticos
python manage.py collectstatic --noinput
```

---

**Estado**: ✅ LISTO PARA DEPLOY
**Fecha**: 20/01/2026
