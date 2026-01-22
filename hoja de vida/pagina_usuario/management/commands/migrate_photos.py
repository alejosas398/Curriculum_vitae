from django.core.management.base import BaseCommand
from pagina_usuario.models import Perfil
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Migra automáticamente todas las fotos de perfil locales a Azure Blob Storage'

    def handle(self, *args, **options):
        self.stdout.write('🚀 Iniciando migración automática de fotos a Azure...\n')

        migrated = 0
        errors = 0
        skipped = 0

        perfiles = Perfil.objects.exclude(foto='').exclude(foto=None)

        if not perfiles.exists():
            self.stdout.write('ℹ️  No hay fotos de perfil para migrar')
            return

        self.stdout.write(f'📋 Procesando {perfiles.count()} perfiles con fotos...\n')

        for perfil in perfiles:
            try:
                foto_name = perfil.foto.name

                # Si ya está en Azure, saltar
                if perfil._is_azure_blob_name(foto_name):
                    skipped += 1
                    continue

                # Si no existe localmente, saltar (podría estar en otro servidor)
                if not hasattr(perfil.foto, 'path') or not perfil.foto.path or not hasattr(perfil.foto.storage, 'path'):
                    try:
                        # Verificar si existe en el sistema de archivos
                        with open(perfil.foto.path, 'rb') as f:
                            pass
                    except (FileNotFoundError, OSError):
                        skipped += 1
                        continue

                # Intentar migrar
                if perfil._migrate_foto_to_azure():
                    migrated += 1
                    self.stdout.write(f'✅ Migrada foto de {perfil.user.username}')
                else:
                    errors += 1
                    self.stdout.write(f'❌ Error migrando foto de {perfil.user.username}')

            except Exception as e:
                errors += 1
                self.stdout.write(f'❌ Error procesando foto de {perfil.user.username}: {str(e)}')

        # Resumen
        self.stdout.write(f'\n📊 Resumen de migración:')
        self.stdout.write(f'   ✅ Migradas: {migrated}')
        self.stdout.write(f'   ⏭️  Omitidas: {skipped}')
        self.stdout.write(f'   ❌ Errores: {errors}')

        if migrated > 0 or errors == 0:
            self.stdout.write('\n🎉 Migración completada exitosamente!')
        else:
            self.stdout.write('\n⚠️  Revisar errores en la migración')

