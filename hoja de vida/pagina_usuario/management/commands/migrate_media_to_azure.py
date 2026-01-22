"""
Management command to migrate media files to Azure Blob Storage
Usage: python manage.py migrate_media_to_azure
"""

from django.core.management.base import BaseCommand
from django.conf import settings
from pagina_usuario.models import Perfil, Experiencia, Educacion, Curso, Recomendacion
import os
from pathlib import Path


class Command(BaseCommand):
    help = 'Migra archivos de media existentes a Azure Blob Storage'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Mostrar qué se migvaría sin hacerlo realmente',
        )
        parser.add_argument(
            '--filter',
            type=str,
            help='Filtrar solo cierto tipo de modelo (perfil, experiencia, curso, recomendacion)',
        )

    def handle(self, *args, **options):
        dry_run = options.get('dry_run', False)
        filter_type = options.get('filter', None)

        self.stdout.write(
            self.style.SUCCESS(
                '=== Iniciando migración de archivos media a Azure ==='
            )
        )

        if dry_run:
            self.stdout.write(self.style.WARNING('MODO DRY-RUN ACTIVADO - No se harán cambios'))

        migrated_count = 0
        error_count = 0

        # Migrar fotos de perfil
        if not filter_type or filter_type == 'perfil':
            self.stdout.write('\nMigrando fotos de perfil...')
            perfiles = Perfil.objects.filter(foto__isnull=False).exclude(foto='')
            self.stdout.write(f'  Encontradas {perfiles.count()} fotos de perfil')

            for perfil in perfiles:
                try:
                    if self._should_migrate(perfil.foto.name):
                        if dry_run:
                            self.stdout.write(
                                f'  [DRY-RUN] Migvaría: {perfil.user.username} - {perfil.foto.name}'
                            )
                        else:
                            if perfil._migrate_foto_to_azure():
                                self.stdout.write(
                                    self.style.SUCCESS(
                                        f'  ✓ Migrado: {perfil.user.username} - {perfil.foto.name}'
                                    )
                                )
                                migrated_count += 1
                            else:
                                error_count += 1
                                self.stdout.write(
                                    self.style.ERROR(
                                        f'  ✗ Error: No se pudo migrar {perfil.user.username}'
                                    )
                                )
                except Exception as e:
                    error_count += 1
                    self.stdout.write(
                        self.style.ERROR(
                            f'  ✗ Error al procesar perfil: {str(e)}'
                        )
                    )

        # Migrar certificados de experiencia
        if not filter_type or filter_type == 'experiencia':
            self.stdout.write('\nMigrando certificados de experiencia...')
            experiencias = Experiencia.objects.filter(certificado__isnull=False).exclude(
                certificado=''
            )
            self.stdout.write(f'  Encontrados {experiencias.count()} certificados de experiencia')

            for exp in experiencias:
                try:
                    if self._should_migrate(exp.certificado.name):
                        if dry_run:
                            self.stdout.write(
                                f'  [DRY-RUN] Migvaría: {exp.empresa} - {exp.certificado.name}'
                            )
                        else:
                            migrated = self._migrate_file_to_azure(exp, 'certificado')
                            if migrated:
                                self.stdout.write(
                                    self.style.SUCCESS(
                                        f'  ✓ Migrado: {exp.empresa} - {exp.certificado.name}'
                                    )
                                )
                                migrated_count += 1
                            else:
                                error_count += 1
                except Exception as e:
                    error_count += 1
                    self.stdout.write(
                        self.style.ERROR(f'  ✗ Error: {str(e)}')
                    )

        # Migrar certificados de cursos
        if not filter_type or filter_type == 'curso':
            self.stdout.write('\nMigrando certificados de cursos...')
            cursos = Curso.objects.filter(certificado__isnull=False).exclude(certificado='')
            self.stdout.write(f'  Encontrados {cursos.count()} certificados de cursos')

            for curso in cursos:
                try:
                    if self._should_migrate(curso.certificado.name):
                        if dry_run:
                            self.stdout.write(
                                f'  [DRY-RUN] Migvaría: {curso.nombre} - {curso.certificado.name}'
                            )
                        else:
                            migrated = self._migrate_file_to_azure(curso, 'certificado')
                            if migrated:
                                self.stdout.write(
                                    self.style.SUCCESS(
                                        f'  ✓ Migrado: {curso.nombre} - {curso.certificado.name}'
                                    )
                                )
                                migrated_count += 1
                            else:
                                error_count += 1
                except Exception as e:
                    error_count += 1
                    self.stdout.write(
                        self.style.ERROR(f'  ✗ Error: {str(e)}')
                    )

        # Migrar certificados de recomendación
        if not filter_type or filter_type == 'recomendacion':
            self.stdout.write('\nMigrando certificados de recomendación...')
            recomendaciones = Recomendacion.objects.filter(certificado__isnull=False).exclude(
                certificado=''
            )
            self.stdout.write(f'  Encontrados {recomendaciones.count()} certificados de recomendación')

            for rec in recomendaciones:
                try:
                    if self._should_migrate(rec.certificado.name):
                        if dry_run:
                            self.stdout.write(
                                f'  [DRY-RUN] Migvaría: {rec.nombre_contacto} - {rec.certificado.name}'
                            )
                        else:
                            migrated = self._migrate_file_to_azure(rec, 'certificado')
                            if migrated:
                                self.stdout.write(
                                    self.style.SUCCESS(
                                        f'  ✓ Migrado: {rec.nombre_contacto} - {rec.certificado.name}'
                                    )
                                )
                                migrated_count += 1
                            else:
                                error_count += 1
                except Exception as e:
                    error_count += 1
                    self.stdout.write(
                        self.style.ERROR(f'  ✗ Error: {str(e)}')
                    )

        # Resumen
        self.stdout.write('\n' + self.style.SUCCESS('=== Resumen de migración ==='))
        self.stdout.write(self.style.SUCCESS(f'Archivos migrados: {migrated_count}'))
        self.stdout.write(self.style.ERROR(f'Errores: {error_count}'))

    def _should_migrate(self, file_name):
        """Determina si un archivo debe ser migrado a Azure"""
        if not file_name:
            return False
        
        # No migrar si ya está en Azure (contiene UUID)
        import re
        if re.search(r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}', file_name):
            return False
        
        return True

    def _migrate_file_to_azure(self, obj, field_name):
        """Migra un archivo de un modelo a Azure"""
        try:
            from Val.azure_storage import AzureBlobStorage
            import uuid
            import os

            field = getattr(obj, field_name)
            if not field:
                return False

            file_path = field.path
            if not os.path.exists(file_path):
                return False

            # Crear nuevo nombre único
            file_extension = os.path.splitext(file_path)[1]
            blob_name = f"{field_name}s/{uuid.uuid4()}{file_extension}"

            # Subir a Azure
            storage = AzureBlobStorage()
            with open(file_path, 'rb') as f:
                blob_name = storage._save(blob_name, f)

            # Actualizar el registro
            setattr(obj, field_name, blob_name)
            obj.save(update_fields=[field_name])

            return True
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error al migrar: {str(e)}'))
            return False
