"""
Geração dos serviços automáticos a partir das configurações.

Mesma regra de negócio de schedules/management/comands/run_scheduled_task_*.py
do app principal, com duas garantias extras:
  * idempotência — nunca cria duas vezes o mesmo serviço (configuração + horário);
  * data de referência explícita — permite reprocessar um dia que falhou.
"""

from datetime import datetime, timedelta

from django.db import transaction
from django.utils import timezone

from gerente.models import Gerente
from servicos.models_jardinagem import ServicoJardinagemAgendado, ServicoJardinagemConfigurado
from servicos.models_limpeza_predial import ServicoLimpezaPredialAgendado, ServicoLimpezaPredialConfigurado

DIAS_SEMANA = {
    0: 'Segunda-Feira',
    1: 'Terça-Feira',
    2: 'Quarta-Feira',
    3: 'Quinta-Feira',
    4: 'Sexta-Feira',
    5: 'Sábado',
    6: 'Domingo',
}

# Mesmo gerente padrão usado pelo app principal na Jardinagem
GERENTE_PADRAO_JARDINAGEM = 'MuUe1D3pvT3v'
DURACAO_PADRAO = timedelta(minutes=30)


class Resultado:
    def __init__(self):
        self.processados = 0
        self.criados = 0
        self.ignorados = 0
        self.linhas = []

    def log(self, texto):
        self.linhas.append(texto)


def _horarios(config):
    return [h for h in (
        config.horario_1, config.horario_2, config.horario_3, config.horario_4,
        config.horario_5, config.horario_6, config.horario_7,
    ) if h]


def _configuracoes(modelo, data):
    return modelo.objects.filter(
        status='Mobilizado',
        Areas__status='Mobilizado',
        Areas__localidade__status='Mobilizado',
        Areas__localidade__unidade__status='Mobilizado',
        ServicosEscalados__status='Mobilizado',
        diasaseremrealizado__diasdasemana=DIAS_SEMANA[data.weekday()],
    ).select_related('Areas').prefetch_related('ServicosEscalados').distinct()


def _gerar(config_model, agendado_model, data, resultado, gerente_padrao=None):
    fuso = timezone.get_current_timezone()
    for config in _configuracoes(config_model, data):
        resultado.processados += 1
        servicos = list(config.ServicosEscalados.filter(status='Mobilizado').distinct())
        horarios = _horarios(config)
        if not servicos or not horarios:
            resultado.ignorados += 1
            continue

        duracao = config.tempomedioplanejado or DURACAO_PADRAO
        descricao = ', '.join(s.nome for s in servicos)[:199]

        for horario in horarios:
            inicio = timezone.make_aware(datetime.combine(data, horario), fuso)
            ja_existe = agendado_model.objects.filter(
                id_configuracao=config.id_random, DataDeInicio=inicio,
            ).exists()
            if ja_existe:
                resultado.ignorados += 1
                continue

            with transaction.atomic():
                novo = agendado_model.objects.create(
                    id_configuracao=config.id_random,
                    DescricaoDoServico=descricao,
                    Areas=config.Areas,
                    DataDeInicio=inicio,
                    DataDeConclusao=inicio + duracao,
                    TipoServico='Automático',
                )
                novo.ServicosEscalados.set(servicos)
                if gerente_padrao is not None:
                    novo.ColaboradoresEscalados.set([gerente_padrao])
            resultado.criados += 1
            resultado.log(f'{novo.id_random} · {config.Areas} · {inicio:%d/%m %H:%M}')
    return resultado


def gerar_jardinagem(data):
    resultado = Resultado()
    gerente = Gerente.objects.filter(id_random=GERENTE_PADRAO_JARDINAGEM).first()
    if gerente is None:
        resultado.log(f'Aviso: gerente padrão {GERENTE_PADRAO_JARDINAGEM} não encontrado; serviços sem colaborador.')
    return _gerar(ServicoJardinagemConfigurado, ServicoJardinagemAgendado, data, resultado, gerente)


def gerar_limpeza_predial(data):
    return _gerar(ServicoLimpezaPredialConfigurado, ServicoLimpezaPredialAgendado, data, Resultado())
