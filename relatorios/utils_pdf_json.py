"""
Dados dos relatórios PDF em JSON, para o PDF ser montado no navegador.

As views de PDF continuam as mesmas (mesmos filtros e permissões). Quando a
requisição chega com ?formato=json, a view devolve estes dados em vez de
desenhar o PDF no servidor. O arquivo é montado por
setup/static/dist/js/zeladorx-relatorio-pdf.js.
"""
from django.http import JsonResponse
from django.templatetags.static import static
from django.utils import timezone

from relatorios.utils_pdf import carregar_checklists


def _data(valor):
    if not valor:
        return None
    if timezone.is_aware(valor):
        valor = timezone.localtime(valor)
    return valor.strftime('%d/%m/%Y %H:%M')


def _url(arquivo):
    try:
        return arquivo.url if arquivo else None
    except Exception:
        return None


def _nome(objeto, campo='nome'):
    return str(getattr(objeto, campo, '') or '') if objeto else None


def relatorio_pdf_json(dados, execucoes_por_agendamento, permission_type, status,
                       checklist_model=None):
    status_list = status if isinstance(status, (list, tuple)) else str(status).split(',')
    jardinagem = permission_type == 'jardinagem'

    relacionados = ['Areas', 'Areas__localidade']
    if jardinagem:
        relacionados += ['Areas__Terreno', 'Areas__vegetacao']
    dados = dados.select_related(*relacionados)

    servicos = []
    vistos = set()
    for dado in dados:
        if dado.id in vistos:
            continue
        vistos.add(dado.id)
        area = dado.Areas

        execucoes = []
        for execucao in execucoes_por_agendamento.get(dado.id, []):
            execucoes.append({
                'colaborador': str(execucao.colaboradores_chamados or '-'),
                'chegada': _data(getattr(execucao, 'data_hora_chegada', None)),
                'retorno': _data(getattr(execucao, 'data_hora_retorno', None)),
                'tempo': str(execucao.tempo_na_area) if getattr(execucao, 'tempo_na_area', None) else None,
                'foto_entrega': None if jardinagem else _url(getattr(execucao, 'foto_entrega', None)),
            })

        checklists = []
        if checklist_model is not None:
            for checklist in carregar_checklists(dado, checklist_model):
                checklists.append({
                    'descricao': str(checklist.descricao or ''),
                    'status': str(checklist.status or ''),
                    'atualizado_em': _data(checklist.atualizado_em),
                    'foto': _url(checklist.foto_comprovacao),
                })

        servicos.append({
            'id': dado.id,
            'descricao': str(dado.DescricaoDoServico or ''),
            'status': str(dado.status or ''),
            'novo_status': str(getattr(dado, 'novo_status', '') or ''),
            'dias_diferenca': getattr(dado, 'dias_diferenca', None),
            'inicio': _data(dado.DataDeInicio),
            'conclusao': _data(dado.DataDeConclusao),
            'area': {
                'nome': _nome(area),
                'dimensao': float(area.dimensao or 0) if area and area.dimensao else 0,
                'localidade': _nome(getattr(area, 'localidade', None)),
                'terreno': _nome(getattr(area, 'Terreno', None)) if jardinagem else None,
                'vegetacao': _nome(getattr(area, 'vegetacao', None)) if jardinagem else None,
            },
            'servicos': [str(s.nome) for s in dado.ServicosEscalados.all()],
            'colaboradores': [str(c.username) for c in dado.ColaboradoresEscalados.all()] if jardinagem else [],
            'foto_solicitacao': _url(getattr(dado, 'foto_solicitacao', None)) if jardinagem else None,
            'foto_entrega': _url(getattr(dado, 'foto_entrega', None)) if jardinagem else None,
            'execucoes': execucoes,
            'checklists': checklists,
        })

    return JsonResponse({
        'setor': permission_type,
        'com_checklist': checklist_model is not None,
        'status': status_list,
        'gerado_em': _data(timezone.now()),
        'logo': static('dist/img/logo alt.png'),
        'imagem_padrao': static('dist/img/not found.png'),
        'servicos': servicos,
    }, json_dumps_params={'ensure_ascii': False})
