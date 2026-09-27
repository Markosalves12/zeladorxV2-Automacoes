from datetime import date

from django.core.management.base import BaseCommand, CommandError

from automacoes.executor import executar, executar_pendentes
from automacoes.models import Rotina


class Command(BaseCommand):
    help = (
        'Executa as rotinas pendentes (use no Heroku Scheduler a cada 10 minutos). '
        'Com --rotina força uma rotina específica, opcionalmente para outra --data.'
    )

    def add_arguments(self, parser):
        parser.add_argument('--rotina', help='Código da rotina, ex.: gerar_jardinagem')
        parser.add_argument('--data', help='Data de referência AAAA-MM-DD (padrão: hoje)')
        parser.add_argument('--listar', action='store_true', help='Lista as rotinas cadastradas')

    def handle(self, *args, **opts):
        if opts['listar']:
            for r in Rotina.objects.all():
                self.stdout.write(f'{r.codigo:25} {"ativa" if r.ativa else "pausada":8} {r.horario:%H:%M} {r.nome}')
            return

        if opts['rotina']:
            rotina = Rotina.objects.filter(codigo=opts['rotina']).first()
            if not rotina:
                raise CommandError(f'Rotina {opts["rotina"]} não existe. Use --listar.')
            data = date.fromisoformat(opts['data']) if opts['data'] else None
            execucoes = [e for e in [executar(rotina, data=data, origem='terminal')] if e]
        else:
            execucoes = executar_pendentes()

        if not execucoes:
            self.stdout.write('Nenhuma rotina pendente agora.')
        for e in execucoes:
            estilo = self.style.SUCCESS if e.status == 'sucesso' else self.style.ERROR
            self.stdout.write(estilo(
                f'{e.rotina.codigo}: {e.get_status_display()} · {e.itens_criados} criados · {e.itens_ignorados} ignorados'
            ))
