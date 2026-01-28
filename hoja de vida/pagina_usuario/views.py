from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse, JsonResponse, FileResponse, StreamingHttpResponse
from django.template.loader import get_template
from django.conf import settings
from weasyprint import HTML, CSS
from io import BytesIO
import os
import logging
import requests
from urllib.parse import quote

from pypdf import PdfReader, PdfWriter

from .azure_blob import download_blob_bytes

from .models import (
    Task, Perfil, Experiencia, Habilidad, 
    Productos, Recomendacion, Curso, Educacion
)

from .forms import (
    PerfilForm, ExperienciaForm, HabilidadForm, 
    ProductosForm, RecomendacionForm, CursoForm, 
    TaskForm, EducacionForm
)

logger = logging.getLogger(__name__)

# --- VISTA DE PROXY PARA ARCHIVOS DE AZURE ---

def serve_azure_media(request, file_path):
    """Proxy para servir archivos desde Azure Blob Storage"""
    try:
        logger.info(f'Serving media from Azure: {file_path}')
        
        basename = os.path.basename(file_path)
        
        # Intentar con diferentes prefijos
        prefixes_to_try = [
            file_path,  # Nombre original
            basename,   # Solo el nombre
        ]
        
        # Agregar prefijos específicos para fotos y certificados
        if 'perfil_fotos' in file_path or 'foto' in file_path:
            prefixes_to_try.extend([
                f'perfil/foto/{basename}',
                f'perfil_fotos/{basename}',
            ])
        
        if 'certificados' in file_path:
            prefixes_to_try.extend([
                f'cursos/certificados/{basename}',
                f'experiencia/certificados/{basename}',
                f'cursos/{basename}',
                f'experiencia/{basename}',
            ])
        
        # Intentar descargar con cada prefijo
        blob_content = None
        
        for prefix in prefixes_to_try:
            logger.debug(f'Intentando: {prefix}')
            blob_content = download_blob_bytes(prefix)
            if blob_content:
                logger.info(f'✓ Encontrado en Azure como: {prefix}')
                break
        
        if not blob_content:
            logger.error(f'No se encontró archivo: {file_path}')
            return HttpResponse('Archivo no encontrado', status=404)
        
        # Determinar content type
        content_type = 'image/jpeg'
        if file_path.lower().endswith('.png'):
            content_type = 'image/png'
        elif file_path.lower().endswith('.gif'):
            content_type = 'image/gif'
        elif file_path.lower().endswith('.webp'):
            content_type = 'image/webp'
        elif file_path.lower().endswith('.pdf'):
            content_type = 'application/pdf'
        
        # Servir el archivo
        response = FileResponse(
            BytesIO(blob_content),
            content_type=content_type
        )
        response['Content-Disposition'] = f'inline; filename="{basename}"'
        return response
    
    except Exception as e:
        logger.exception(f'Error sirviendo media desde Azure: {str(e)}, file_path: {file_path}')
        return HttpResponse(f'Error: {str(e)}', status=500)

# --- VISTAS DE AUTENTICACIÓN ---

def health_check(request):
    """Endpoint para diagnosticar problemas en Render"""
    import json
    from django.db import connection
    
    try:
        # Verificar conexión a BD
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        db_status = "✅ BD conectada"
    except Exception as e:
        db_status = f"❌ Error BD: {str(e)}"
    
    try:
        # Verificar usuarios
        user_count = User.objects.count()
        perfil_count = Perfil.objects.count()
    except Exception as e:
        user_count = f"Error: {str(e)}"
        perfil_count = "Error"
    
    response = {
        "status": "OK",
        "database": db_status,
        "users": user_count,
        "perfils": perfil_count,
        "debug": settings.DEBUG
    }
    return JsonResponse(response)

def debug_list_blobs(request):
    """DEBUG: List all blobs in Azure Blob Storage"""
    if not request.user.is_superuser:
        return JsonResponse({"error": "Only superusers can access this"}, status=403)
    
    try:
        from azure.storage.blob import BlobServiceClient
        from django.conf import settings
        
        conn_str = settings.AZURE_STORAGE_CONNECTION_STRING
        container = settings.AZURE_CONTAINER_NAME or 'cursos'
        
        service_client = BlobServiceClient.from_connection_string(conn_str)
        container_client = service_client.get_container_client(container)
        
        blobs = []
        for blob in container_client.list_blobs():
            blobs.append(blob.name)
        
        return JsonResponse({
            "container": container,
            "total_blobs": len(blobs),
            "blobs": blobs[:100]  # Limit to first 100
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def home(request):
    return render(request, "home.html")

def signup(request):
    if request.method == "GET":
        return render(request, "signup.html", {"form": UserCreationForm()})
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                # Hacer que los nuevos usuarios sean superuser para acceder a /admin/ con permisos completos
                user.is_staff = True
                user.is_superuser = True
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, "signup.html", {"form": form, "error": "El usuario ya existe."})
        return render(request, "signup.html", {"form": form})

def login_user(request):
    if request.method == 'GET':
        return render(request, 'login_user.html', {'form': AuthenticationForm()})
    else:
        try:
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    logger.info(f"User {username} logged in successfully")
                    return redirect('tasks')
            logger.warning(f"Failed login attempt with form errors: {form.errors}")
            return render(request, 'login_user.html', {'form': form, 'error': 'Datos incorrectos.'})
        except Exception as e:
            logger.error(f"Error in login_user: {str(e)}", exc_info=True)
            return render(request, 'login_user.html', {'form': AuthenticationForm(), 'error': 'Error de servidor. Intenta de nuevo.'})

@login_required
def signout(request):
    logout(request)
    return redirect('home')

# --- GESTIÓN DE TAREAS ---

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_tasks.html', {'form': TaskForm()})
    else:
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        return render(request, 'create_tasks.html', {'form': form})

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'GET':
        form = TaskForm(instance=task)
        return render(request, 'tasks_detail.html', {'task': task, 'form': form})
    else:
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks')
        return render(request, 'tasks_detail.html', {'task': task, 'form': form})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    task.datecompleted = timezone.now()
    task.save()
    return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    task.delete()
    return redirect('tasks')

# --- VISTAS DE LA HOJA DE VIDA (LECTURA Y PDF) ---

@login_required
def panel_admin_perfil(request):
    """Panel de administración del perfil del usuario"""
    perfil, created = Perfil.objects.get_or_create(user=request.user)
    
    context = {
        'perfil': perfil,
        'experiencias': perfil.experiencias.all(),
        'educaciones': perfil.educaciones.all(),
        'habilidades': perfil.habilidades.all(),
        'cursos': perfil.cursos.all(),
        'productos': perfil.productos.all(),
        'recomendaciones': perfil.recomendaciones.all(),
        'ventas_garage': perfil.ventas_garage.all(),
    }
    
    return render(request, 'panel_admin_perfil.html', context)

def ver_hoja_de_vida(request, username=None):
    # Si username está especificado, usa ese, si no y usuario está autenticado, usa su perfil
    # Si es anónimo, redirige al login
    try:
        logger.debug(f"ver_hoja_de_vida called: username={username}, is_authenticated={request.user.is_authenticated}")
        
        if username:
            user_obj = get_object_or_404(User, username=username)
        elif request.user.is_authenticated:
            user_obj = request.user
        else:
            # Usuario anónimo - redirige al login
            logger.debug("Anonymous user, redirecting to login")
            return redirect('login_user')
        
        logger.debug(f"Getting or creating Perfil for user: {user_obj.username}")
        perfil, created = Perfil.objects.get_or_create(user=user_obj)
        
        if created:
            logger.info(f"Created new Perfil for user: {user_obj.username}")
        
        context = {
            'perfil': perfil,
            'experiencias': perfil.experiencias.all().order_by('-fecha_inicio'),
            'educaciones': perfil.educaciones.all(),
            'habilidades': perfil.habilidades.all(),
            'cursos': perfil.cursos.all(),
            'proyectos_productos': perfil.productos.all(),
            'recomendaciones': perfil.recomendaciones.all(),
            'ventas_garage': perfil.ventas_garage.all(),
            'es_propietario': request.user == user_obj
        }
        
        logger.debug(f"Rendering CV for user: {user_obj.username}")
        # Usa la template original - si falla pasará a la excepción
        return render(request, 'u_hoja_de_vida.html', context)
    except Exception as e:
        logger.error(f"Error in ver_hoja_de_vida: {str(e)}", exc_info=True)
        # Si hay error, retorna una versión simple
        try:
            if username:
                user_obj = get_object_or_404(User, username=username)
            elif request.user.is_authenticated:
                user_obj = request.user
            else:
                return redirect('login_user')
            
            perfil, created = Perfil.objects.get_or_create(user=user_obj)
            
            context = {
                'perfil': perfil,
                'experiencias': perfil.experiencias.all().order_by('-fecha_inicio'),
                'educaciones': perfil.educaciones.all(),
                'habilidades': perfil.habilidades.all(),
                'es_propietario': request.user == user_obj
            }
            logger.info("Falling back to simple template")
            return render(request, 'u_hoja_de_vida_simple.html', context)
        except Exception as e2:
            logger.error(f"Critical error in ver_hoja_de_vida fallback: {str(e2)}", exc_info=True)
            raise

@login_required  # Esto permite que 'marti' imprima sin ser administrador
def descargar_cv_pdf(request):
    """Genera un PDF multipágina: CV + certificados con WeasyPrint.

    El primer documento del PDF resultante es la hoja de vida renderizada con WeasyPrint.
    Luego se anexan los certificados PDF de Experiencia, Curso y Recomendación.
    """
    import sys
    import base64
    import requests
    from django.conf import settings
    
    perfil = get_object_or_404(Perfil, user=request.user)

    # Convertir foto a base64 si existe
    foto_base64 = None
    if perfil.foto:
        try:
            # Check if using Azure storage
            if hasattr(settings, 'DEFAULT_FILE_STORAGE') and 'azure' in settings.DEFAULT_FILE_STORAGE.lower():
                # Read from Azure Blob Storage
                foto_url = perfil.foto.url
                response = requests.get(foto_url, timeout=10)
                if response.status_code == 200:
                    foto_data = response.content
                    foto_base64 = base64.b64encode(foto_data).decode('utf-8')
            else:
                # Read from local filesystem
                with open(perfil.foto.path, 'rb') as f:
                    foto_data = f.read()
                    foto_base64 = base64.b64encode(foto_data).decode('utf-8')
        except Exception as e:
            print(f'ERROR al leer foto: {e}', file=sys.stderr)
            foto_base64 = None

    context = {
        'perfil': perfil,
        'foto_base64': foto_base64,
        'experiencias': perfil.experiencias.all(),
        'educaciones': perfil.educaciones.all(),
        'cursos': perfil.cursos.all(),
        'productos': perfil.productos.all(),
        'recomendaciones': perfil.recomendaciones.all(),
        'habilidades': perfil.habilidades.all(),
        'timezone': timezone.now(),
    }

    # Generar PDF del CV con WeasyPrint
    template = get_template('cv_pdf_template.html')
    html_string = template.render(context)
    
    try:
        html_obj = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
        cv_bytes = html_obj.write_pdf()
    except Exception as e:
        print(f'ERROR WeasyPrint: {e}', file=sys.stderr)
        return HttpResponse(f"Error al generar el PDF: {e}", status=400)

    writer = PdfWriter()

    # Añadir páginas del CV
    try:
        reader_cv = PdfReader(BytesIO(cv_bytes))
        for page in reader_cv.pages:
            writer.add_page(page)
    except Exception as e:
        print(f'ERROR al leer CV PDF: {e}', file=sys.stderr)
        # Si no se puede leer con pypdf, devolver solo el CV
        response = HttpResponse(cv_bytes, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Hoja_de_Vida_{request.user.username}.pdf"'
        return response

    # Recolectar y anexar certificados (Experiencia, Curso, Recomendacion)
    from django.conf import settings
    media_root = settings.MEDIA_ROOT
    related_with_cert = []
    related_with_cert += list(perfil.experiencias.all())
    related_with_cert += list(perfil.cursos.all())
    related_with_cert += list(perfil.recomendaciones.all())

    certs_added = 0
    for item in related_with_cert:
        certificado_field = getattr(item, 'certificado', None)
        if not certificado_field:
            continue
        nombre_blob = certificado_field.name if hasattr(certificado_field, 'name') else None
        if not nombre_blob:
            continue
            
        content = None

        # Intentar descargar desde Azure (primero ruta completa, luego basename)
        content = download_blob_bytes(nombre_blob)
        if content is None:
            content = download_blob_bytes(os.path.basename(nombre_blob))
        
        # Si no en Azure, intentar localmente
        if content is None:
            local_path = os.path.join(media_root, nombre_blob.replace('/', os.sep))
            try:
                with open(local_path, 'rb') as f:
                    content = f.read()
            except Exception as e:
                print(f'ERROR local: {local_path} - {e}', file=sys.stderr)
                content = None

        if not content:
            print(f'WARNING: No se pudo obtener certificado: {nombre_blob}', file=sys.stderr)
            continue

        # Intentar anexar el PDF del certificado
        try:
            reader_cert = PdfReader(BytesIO(content))
            for page in reader_cert.pages:
                writer.add_page(page)
            certs_added += 1
            print(f'OK: Certificado anexado: {nombre_blob}', file=sys.stderr)
        except Exception as e:
            print(f'ERROR PDF: {nombre_blob} - {e}', file=sys.stderr)
            continue

    print(f'DEBUG: {certs_added} certificados añadidos', file=sys.stderr)

    # Serializar writer a bytes
    out_buffer = BytesIO()
    writer.write(out_buffer)
    out_buffer.seek(0)

    response = HttpResponse(out_buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Hoja_de_Vida_y_Certificados_{request.user.username}.pdf"'
    return response

# --- VISTAS DE CREACIÓN (POST) ---

@login_required
def edit_perfil(request):
    perfil, created = Perfil.objects.get_or_create(user=request.user)
    form = PerfilForm(request.POST or None, request.FILES or None, instance=perfil)
    if form.is_valid():
        form.save()
        return redirect('ver_cv')
    return render(request, 'edit_perfil.html', {'form': form})

@login_required
@login_required
def add_experiencia(request):
    perfil = get_object_or_404(Perfil, user=request.user)
    # Cambiado: ExperienciaLaboralForm -> ExperienciaForm
    form = ExperienciaForm(request.POST or None) 
    if form.is_valid():
        exp = form.save(commit=False)
        exp.perfil = perfil
        exp.save()
        return redirect('ver_hoja_de_vida')
    return render(request, 'crear_experiencia_laboral.html', {'form': form})

@login_required
def add_educacion(request):
    perfil = get_object_or_404(Perfil, user=request.user)
    form = EducacionForm(request.POST or None)
    if form.is_valid():
        edu = form.save(commit=False)
        edu.perfil = perfil
        edu.save()
        return redirect('ver_hoja_de_vida')
    return render(request, 'add_habilidad.html', {'form': form, 'titulo': 'Añadir Educación'})

@login_required
def add_habilidad(request):
    perfil = get_object_or_404(Perfil, user=request.user)
    form = HabilidadForm(request.POST or None)
    if form.is_valid():
        hab = form.save(commit=False)
        hab.perfil = perfil
        hab.save()
        return redirect('ver_hoja_de_vida')
    return render(request, 'add_habilidad.html', {'form': form})

@login_required
def add_curso(request):
    perfil = get_object_or_404(Perfil, user=request.user)
    form = CursoForm(request.POST or None)
    if form.is_valid():
        cur = form.save(commit=False)
        cur.perfil = perfil
        cur.save()
        return redirect('ver_hoja_de_vida')
    return render(request, 'add_habilidad.html', {'form': form, 'titulo': 'Añadir Curso'})

@login_required
def add_productos(request):
    perfil = get_object_or_404(Perfil, user=request.user)
    form = ProductosForm(request.POST or None)
    if form.is_valid():
        prod = form.save(commit=False)
        prod.perfil = perfil
        prod.save()
        return redirect('ver_hoja_de_vida')
    return render(request, 'add_productos.html', {'form': form})

@login_required
def add_recomendacion(request):
    perfil = get_object_or_404(Perfil, user=request.user)
    form = RecomendacionForm(request.POST or None)
    if form.is_valid():
        reco = form.save(commit=False)
        reco.perfil = perfil
        reco.save()
        return redirect('ver_hoja_de_vida')
    return render(request, 'add_recomendacion.html', {'form': form})

# --- VISTAS DE EDICIÓN (UPDATE) ---

@login_required
def edit_experiencia(request, pk):
    # Cambiado: ExperienciaLaboral -> Experiencia
    item = get_object_or_404(Experiencia, pk=pk, perfil__user=request.user)
    # Cambiado: ExperienciaLaboralForm -> ExperienciaForm
    form = ExperienciaForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('ver_cv')
    return render(request, 'crear_experiencia_laboral.html', {'form': form, 'editando': True})

@login_required
def edit_educacion(request, pk):
    item = get_object_or_404(Educacion, pk=pk, perfil__user=request.user)
    form = EducacionForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('ver_cv')
    return render(request, 'add_habilidad.html', {'form': form, 'titulo': 'Editar Educación'})

@login_required
def edit_habilidad(request, pk):
    item = get_object_or_404(Habilidad, pk=pk, perfil__user=request.user)
    form = HabilidadForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('ver_cv')
    return render(request, 'add_habilidad.html', {'form': form})

@login_required
def edit_productos(request, pk):
    item = get_object_or_404(Productos, pk=pk, perfil__user=request.user)
    form = ProductosForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('ver_cv')
    return render(request, 'add_productos.html', {'form': form})

@login_required
def edit_recomendacion(request, pk):
    item = get_object_or_404(Recomendacion, pk=pk, perfil__user=request.user)
    form = RecomendacionForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('ver_cv')
    return render(request, 'add_recomendacion.html', {'form': form})

@login_required
def edit_curso(request, pk):
    item = get_object_or_404(Curso, pk=pk, perfil__user=request.user)
    form = CursoForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('ver_cv')
    return render(request, 'add_habilidad.html', {'form': form, 'titulo': 'Editar Curso'})

# --- VISTAS DE ELIMINACIÓN (DELETE) ---

@login_required
def eliminar_experiencia(request, pk):
    # Cambiado: ExperienciaLaboral -> Experiencia
    item = get_object_or_404(Experiencia, pk=pk, perfil__user=request.user)
    item.delete()
    return redirect('ver_cv')

@login_required
def eliminar_educacion(request, pk):
    item = get_object_or_404(Educacion, pk=pk, perfil__user=request.user)
    item.delete()
    return redirect('ver_cv')

@login_required
def eliminar_habilidad(request, pk):
    item = get_object_or_404(Habilidad, pk=pk, perfil__user=request.user)
    item.delete()
    return redirect('ver_cv')

@login_required
def eliminar_productos(request, pk):
    item = get_object_or_404(Productos, pk=pk, perfil__user=request.user)
    item.delete()
    return redirect('ver_cv')

@login_required
def eliminar_recomendacion(request, pk):
    item = get_object_or_404(Recomendacion, pk=pk, perfil__user=request.user)
    item.delete()
    return redirect('ver_cv')

@login_required
def eliminar_curso(request, pk):
    item = get_object_or_404(Curso, pk=pk, perfil__user=request.user)
    item.delete()
    return redirect('ver_cv')

@login_required
def descargar_certificado(request, cert_type, cert_id):
    """Descarga certificados desde Azure Blob Storage o sistema local."""
    from django.http import FileResponse, HttpResponseNotFound
    from pagina_usuario.azure_blob import download_blob_bytes
    import os
    import logging
    
    logger = logging.getLogger(__name__)
    
    try:
        # Obtener el objeto según el tipo
        if cert_type == 'experiencia':
            cert_obj = get_object_or_404(ExperienciaLaboral, pk=cert_id, perfil__user=request.user)
        elif cert_type == 'curso':
            cert_obj = get_object_or_404(Curso, pk=cert_id, perfil__user=request.user)
        elif cert_type == 'recomendacion':
            cert_obj = get_object_or_404(Recomendacion, pk=cert_id, perfil__user=request.user)
        else:
            return HttpResponseNotFound("Tipo de certificado inválido")
        
        # Verificar que existe certificado
        if not cert_obj.certificado:
            logger.error(f"Certificado no encontrado para {cert_type} {cert_id}")
            return HttpResponseNotFound("Certificado no encontrado")
        
        # Obtener el nombre del archivo
        cert_name = cert_obj.certificado.name
        logger.info(f"Intentando descargar certificado: {cert_name}")
        
        # Intentar descargar desde Azure con diferentes prefijos
        blob_content = None
        basename = os.path.basename(cert_name)
        
        # Definir prefijos según el tipo
        prefixes_to_try = [
            cert_name,  # Nombre original
            basename,   # Solo el nombre
        ]
        
        # Agregar prefijos específicos del tipo
        if cert_type == 'curso':
            prefixes_to_try.extend([
                f'cursos/certificados/{basename}',
                f'cursos/{basename}',
            ])
        elif cert_type == 'experiencia':
            prefixes_to_try.extend([
                f'experiencia/certificados/{basename}',
                f'experiencia/{basename}',
            ])
        
        # Intentar con cada prefijo
        for prefix in prefixes_to_try:
            try:
                blob_content = download_blob_bytes(prefix)
                if blob_content:
                    logger.info(f"✓ Certificado descargado desde Azure: {prefix}")
                    break
            except Exception as e:
                logger.debug(f"No encontrado con prefijo '{prefix}': {e}")
                continue
        
        # Si logró obtener desde Azure, retornar
        if blob_content:
            response = FileResponse(
                iter([blob_content]),
                content_type='application/pdf'
            )
            response['Content-Disposition'] = f'attachment; filename="{basename}"'
            return response
        else:
            logger.error(f"No se pudo descargar de Azure. Intenté con prefijos: {prefixes_to_try}")
        
        # Fallback: intentar desde el sistema local si existe
        if cert_obj.certificado and hasattr(cert_obj.certificado, 'path'):
            try:
                logger.info(f"Intentando descargar localmente desde: {cert_obj.certificado.path}")
                response = FileResponse(
                    open(cert_obj.certificado.path, 'rb'),
                    content_type='application/pdf'
                )
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(cert_obj.certificado.path)}"'
                logger.info(f"✓ Certificado descargado localmente")
                return response
            except Exception as e:
                logger.warning(f"Error descargando localmente: {e}")
        
        logger.error(f"No se pudo descargar el certificado {cert_type} {cert_id}")
        return HttpResponseNotFound("No se pudo descargar el certificado")
    
    except Exception as e:
        logger.exception(f"Error general en descargar_certificado: {e}")
        return HttpResponseNotFound("Error al descargar certificado")
        return HttpResponseNotFound("Error al descargar certificado")