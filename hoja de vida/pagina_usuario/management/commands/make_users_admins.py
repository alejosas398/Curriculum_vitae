from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Convertir todos los usuarios en superusuarios independientes'

    def handle(self, *args, **options):
        self.stdout.write('Convirtiendo usuarios a superusuarios...')

        users = User.objects.all()
        updated_count = 0

        self.stdout.write(f'Encontrados {users.count()} usuarios')

        for user in users:
            if not user.is_staff or not user.is_superuser:
                user.is_staff = True
                user.is_superuser = True
                user.save()
                self.stdout.write(f'✅ Usuario {user.username} convertido en superusuario')
                updated_count += 1
            else:
                self.stdout.write(f'ℹ️ Usuario {user.username} ya es superusuario')

        self.stdout.write(
            self.style.SUCCESS(
                f'Completado. {updated_count} usuarios convertidos a admin'
            )
        )

