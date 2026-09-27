"""
Cria (sem duplicar) as permissões declaradas em permissions_CRUD
de PermissionsJardinagem, PermissionsLimpezaPredial e PermissionsEspecials.

Uso:
    python manage.py criar_permissoes
    python manage.py criar_permissoes --dry-run
    heroku run python manage.py criar_permissoes -a <app>
"""
from django.core.management.base import BaseCommand
from django.db import transaction

from permissionscontrol.models import (
    PermissionsJardinagem,
    PermissionsLimpezaPredial,
    PermissionsEspecials,
)

MODELOS = [
    PermissionsJardinagem,
    PermissionsLimpezaPredial,
    PermissionsEspecials,
]


class Command(BaseCommand):
    help = 'Cria as permissões de permissions_CRUD nos modelos de permissionscontrol'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Apenas mostra o que seria criado')

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        total_criadas = 0

        with transaction.atomic():
            for modelo in MODELOS:
                criadas = 0
                existentes = set(modelo.objects.values_list('Permissions', flat=True))

                for valor, _rotulo in modelo.permissions_CRUD:
                    if valor in existentes:
                        continue
                    if not dry_run:
                        modelo.objects.create(Permissions=valor)
                    criadas += 1
                    self.stdout.write(f'  + {modelo.__name__}: {valor}')

                total_criadas += criadas
                self.stdout.write(self.style.SUCCESS(
                    f'{modelo.__name__}: {criadas} nova(s), '
                    f'{len(modelo.permissions_CRUD) - criadas} já existente(s)'
                ))

            if dry_run:
                transaction.set_rollback(True)

        prefixo = '[dry-run] ' if dry_run else ''
        self.stdout.write(self.style.SUCCESS(f'{prefixo}Total criado: {total_criadas}'))
