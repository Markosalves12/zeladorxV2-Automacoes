"""
E-mails operacionais da família ZeladorX.

Cada envio grava um NotificacaoEnviada com chave única, então reprocessar
um dia nunca manda o mesmo e-mail duas vezes. Falhas ficam registradas e
são tentadas de novo na próxima execução.

Senhas, convites e códigos de troca de senha continuam no app principal.
"""

import logging
from datetime import datetime, time, timedelta

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags

from automacoes.geradores import Resultado
from gerente.models import Gerente
from notificacoes_email.models import NotificacaoEnviada, PreferenciaNotificacao
from servicos.models_jardinagem import ServicoJardinagemAgendado
from servicos.models_limpeza_predial import ServicoLimpezaPredialAgendado

logger = logging.getLogger('notificacoes_email')

SETORES = (
    ('Jardinagem', ServicoJardinagemAgendado),
    ('Limpeza Predial', ServicoLimpezaPredialAgendado),
)
ABERTOS = ('Agendado', 'Em andamento')
JANELA_ATRASO = timedelta(days=7)  # não reenvia histórico antigo


def _janela_do_dia(data):
    fuso = timezone.get_current_timezone()
    inicio = timezone.make_aware(datetime.combine(data, time.min), fuso)
    return inicio, inicio + timedelta(days=1)


def _gerentes_ativos():
    return Gerente.objects.filter(is_active=True, status='Mobilizado').exclude(email='').distinct()


def _quer_receber(gerente, campo):
    pref = PreferenciaNotificacao.objects.filter(gerente=gerente).first()
    return getattr(pref, campo) if pref else True


def _servicos_do_gerente(gerente, modelo, filtro):
    empresas = gerente.empresasecundaria.all()
    qs = modelo.objects.filter(filtro).filter(Areas__localidade__unidade__empresasecundaria__in=empresas)
    if modelo is ServicoJardinagemAgendado:
        qs = modelo.objects.filter(filtro).filter(
            Q(Areas__localidade__unidade__empresasecundaria__in=empresas) | Q(ColaboradoresEscalados=gerente)
        )
    return qs.select_related('Areas', 'Areas__localidade').distinct().order_by('DataDeInicio')


def enviar(gerente, tipo, chave, assunto, template, contexto, referencia='', setor=''):
    """Envia (ou reenvia se falhou antes). Retorna True se enviou agora."""
    existente = NotificacaoEnviada.objects.filter(chave=chave).first()
    if existente and existente.status == 'enviado':
        return False

    contexto = {**contexto, 'gerente': gerente, 'zeladorx_url': settings.ZELADORX_URL, 'assunto': assunto}
    html = render_to_string(f'notificacoes_email/{template}.html', contexto)
    mensagem = EmailMultiAlternatives(assunto, strip_tags(html), settings.DEFAULT_FROM_EMAIL, [gerente.email])
    mensagem.attach_alternative(html, 'text/html')

    registro = existente or NotificacaoEnviada(
        chave=chave, tipo=tipo, destinatario=gerente if gerente.pk else None, email=gerente.email,
        referencia=referencia, setor=setor, tentativas=0,
    )
    registro.assunto = assunto[:200]
    registro.tentativas += 1
    try:
        mensagem.send(fail_silently=False)
        registro.status, registro.erro = 'enviado', ''
        enviado = True
    except Exception as exc:  # SMTP fora do ar, caixa inválida...
        registro.status, registro.erro = 'falhou', str(exc)[:2000]
        logger.warning('Falha ao enviar %s para %s: %s', chave, gerente.email, exc)
        enviado = False
    registro.save()
    return enviado


def _rodar(data, tipo, campo_pref, assunto_fn, template, filtro_fn):
    resultado = Resultado()
    for gerente in _gerentes_ativos():
        resultado.processados += 1
        if not _quer_receber(gerente, campo_pref):
            resultado.ignorados += 1
            continue
        blocos = []
        for setor, modelo in SETORES:
            itens = list(_servicos_do_gerente(gerente, modelo, filtro_fn(modelo))[:200])
            if itens:
                blocos.append({'setor': setor, 'servicos': itens})
        total = sum(len(b['servicos']) for b in blocos)
        if not total:
            resultado.ignorados += 1
            continue
        chave = f'{tipo}:{gerente.pk}:{data.isoformat()}'
        if enviar(gerente, tipo, chave, assunto_fn(total, data), template,
                  {'blocos': blocos, 'total': total, 'data': data}):
            resultado.criados += 1
            resultado.log(f'{gerente.email} · {total} serviço(s)')
        else:
            resultado.ignorados += 1
    return resultado


def enviar_resumo_diario(data):
    inicio, fim = _janela_do_dia(data)
    return _rodar(
        data, 'resumo_diario', 'receber_resumo_diario',
        lambda total, d: f'ZeladorX · {total} serviço(s) previstos para {d:%d/%m}',
        'resumo_diario',
        lambda modelo: Q(DataDeInicio__gte=inicio, DataDeInicio__lt=fim) & ~Q(status='Cancelado'),
    )


def enviar_atrasados(data):
    agora = timezone.now()
    limite = agora - JANELA_ATRASO
    return _rodar(
        data, 'atrasado', 'receber_atrasados',
        lambda total, d: f'ZeladorX · {total} serviço(s) atrasados',
        'atrasados',
        lambda modelo: Q(status__in=ABERTOS) & (
            Q(DataDeConclusao__lt=agora, DataDeConclusao__gte=limite)
            | Q(DataDeConclusao__isnull=True, DataDeInicio__lt=agora, DataDeInicio__gte=limite)
        ),
    )


def enviar_concluidos(data):
    inicio, fim = _janela_do_dia(data)
    return _rodar(
        data, 'concluido', 'receber_concluidos',
        lambda total, d: f'ZeladorX · {total} serviço(s) concluídos em {d:%d/%m}',
        'concluidos',
        lambda modelo: Q(status='Concluido', DataDeConclusao__gte=inicio, DataDeConclusao__lt=fim),
    )


def enviar_teste(email, usuario):
    class Destino:
        pk = None
        username = usuario
    destino = Destino()
    destino.email = email
    chave = f'teste:{email}:{timezone.now().timestamp()}'
    return enviar(destino, 'teste', chave, 'ZeladorX · e-mail de teste', 'teste', {})
