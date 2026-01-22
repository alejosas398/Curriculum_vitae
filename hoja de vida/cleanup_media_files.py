import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Val.settings')
import django
django.setup()

from django.core.files.storage import default_storage
from pagina_usuario.models import Perfil, Experiencia, Curso, Recomendacion
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_file_exists(file_field):
    """Verifica si un archivo existe en el storage"""
    if not file_field:
        return True  # No hay archivo, está bien

    try:
        # Intentar acceder al archivo
        if hasattr(file_field, 'url'):
            # Para Azure Blob Storage, verificar si existe
            return default_storage.exists(file_field.name)
        return False
    except Exception as e:
        logger.warning(f"Error checking file {file_field}: {e}")
        return False

def cleanup_missing_media():
    """Limpia referencias a archivos de media que no existen"""
    logger.info("Iniciando limpieza de archivos de media faltantes...")

    # Verificar fotos de perfil
    perfiles_with_missing_photos = []
    for perfil in Perfil.objects.exclude(foto__isnull=True).exclude(foto=''):
        if not check_file_exists(perfil.foto):
            logger.warning(f"Foto faltante para perfil {perfil}: {perfil.foto.name}")
            perfiles_with_missing_photos.append(perfil)
            # Opcional: limpiar la referencia
            # perfil.foto = None
            # perfil.save()

    # Verificar certificados de experiencia
    experiencias_with_missing_certs = []
    for exp in Experiencia.objects.exclude(certificado__isnull=True).exclude(certificado=''):
        if not check_file_exists(exp.certificado):
            logger.warning(f"Certificado faltante para experiencia {exp}: {exp.certificado.name}")
            experiencias_with_missing_certs.append(exp)

    # Verificar certificados de cursos
    cursos_with_missing_certs = []
    for curso in Curso.objects.exclude(certificado__isnull=True).exclude(certificado=''):
        if not check_file_exists(curso.certificado):
            logger.warning(f"Certificado faltante para curso {curso}: {curso.certificado.name}")
            cursos_with_missing_certs.append(curso)

    # Verificar certificados de recomendaciones
    recomendaciones_with_missing_certs = []
    for reco in Recomendacion.objects.exclude(certificado__isnull=True).exclude(certificado=''):
        if not check_file_exists(reco.certificado):
            logger.warning(f"Certificado faltante para recomendación {reco}: {reco.certificado.name}")
            recomendaciones_with_missing_certs.append(reco)

    # Resumen
    logger.info("=== RESUMEN DE ARCHIVOS FALTANTES ===")
    logger.info(f"Perfiles con fotos faltantes: {len(perfiles_with_missing_photos)}")
    logger.info(f"Experiencias con certificados faltantes: {len(experiencias_with_missing_certs)}")
    logger.info(f"Cursos con certificados faltantes: {len(cursos_with_missing_certs)}")
    logger.info(f"Recomendaciones con certificados faltantes: {len(recomendaciones_with_missing_certs)}")

    total_missing = (
        len(perfiles_with_missing_photos) +
        len(experiencias_with_missing_certs) +
        len(cursos_with_missing_certs) +
        len(recomendaciones_with_missing_certs)
    )

    if total_missing > 0:
        logger.warning(f"Total de archivos faltantes: {total_missing}")
        logger.info("Los archivos faltantes pueden causar errores 404 en producción.")
        logger.info("Recomendación: Subir los archivos faltantes a Azure Blob Storage.")
    else:
        logger.info("✅ No se encontraron archivos faltantes.")

if __name__ == "__main__":
    cleanup_missing_media()
