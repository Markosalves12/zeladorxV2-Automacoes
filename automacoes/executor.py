"""
Executor central das rotinas.

Chamado pelo comando `python manage.py executar_automacoes` (Heroku Scheduler
a cada 10 minutos) e pelo botão "Executar agora" do painel.

Regras:
  * rotina diária roda uma única vez por dia, depois do horário configurado;
  * se uma rodada falhar ou o agendador atrasar, a próxima rodada recupera;
  * trava por linha no banco impede duas execuções simultâneas da mesma rotina.
"""

import logging
import traceback

from django.db import transaction
from django.utils import timezone

from automacoes import geradores
from automacoes.models import Execucao, Rotina

logger = logging.getLogger('automacoes')


def _tarefas():
    from notificacoes_email import envios
    return {
        'gerar_jardinagem': geradores.gerar_jardinagem,
        'gerar_limpeza_predial': geradores.gerar_limpeza_predial,
        'email_resumo_diario': envios.enviar_resumo_diario,
        'email_atrasados': envios.enviar_atrasados,
        'email_concluidos': envios.enviar_concluidos,
    }


def esta_pendente(rotina, agora=None):
    agora = timezone.localtime(agora or timezone.now())
    if not rotina.ativa:
        return False
    if rotina.frequencia == 'continua':
        return True
    if agora.time() < rotina.horario:
        return False
    return not rotina.execucoes.filter(data_referencia=agora.date(), status='sucesso').exists()


def executar(rotina, data=None, origem='agendador', usuario=''):
    data = data or timezone.localdate()
    tarefa = _tarefas()[rotina.codigo]

    with transaction.atomic():
        # Trava a rotina: outra rodada simultânea espera ou desiste
        travada = Rotina.objects.select_for_update(skip_locked=True).filter(pk=rotina.pk).first()
        if travada is None:
            logger.info('Rotina %s já está em execução; pulando.', rotina.codigo)
            return None

        execucao = Execucao.objects.create(
            rotina=travada, data_referencia=data, origem=origem, executado_por=usuario,
        )
        try:
            resultado = tarefa(data)
            execucao.status = 'sucesso'
            execucao.itens_processados = resultado.processados
            execucao.itens_criados = resultado.criados
            execucao.itens_ignorados = resultado.ignorados
            execucao.detalhes = '\n'.join(resultado.linhas[-300:])
        except Exception:
            execucao.status = 'erro'
            execucao.detalhes = traceback.format_exc()[-8000:]
            logger.exception('Falha na rotina %s', rotina.codigo)
        execucao.finalizada_em = timezone.now()
        execucao.save()

    logger.info('%s → %s (%s criados)', rotina.codigo, execucao.status, execucao.itens_criados)
    return execucao


def executar_pendentes(origem='agendador'):
    execucoes = []
    for rotina in Rotina.objects.filter(ativa=True):
        if esta_pendente(rotina):
            execucoes.append(executar(rotina, origem=origem))
    return [e for e in execucoes if e]
