import openpyxl
from servicos.headers_report_limpeza_predial import headers_report_services, headers_report_schedules
from servicos.utils_limpeza_predial import (colect_dados_fato_servico_limpeza_predial,
                                            colect_dados_agendamentos_limpeza_predial)
from checklists.models import CheckListLimpezaPredial  # Import do modelo de checklist
from django.http import HttpResponse
from utils.utils import generate_id_random
from datetime import datetime
from permissionscontrol.utils import verify_login
from django.shortcuts import redirect
from relatorios.utils_xlsx import adicionar_cabecalhos, adicionar_dados

def exportar_relatorio_de_serivos_limpeza_predial_excel_with_checklist(
    request, userid, status, DataDeInicio, DataDeConclusao, Areas,
    TipoServico, ServicosEscalados, ColaboradoresEscalados
):
    # Verifica login
    block = verify_login(request=request, userid=userid)
    if block:
        return redirect('logout')

    # Cria o workbook e as planilhas
    wb = openpyxl.Workbook()
    ws_agendadamentos = wb.active
    ws_agendadamentos.title = "Relatório de agendamentos jardinagem"
    ws_acompanhamento = wb.create_sheet(title="Relatório de acompanhamento")  # Cria a segunda aba
    ws_checklists = wb.create_sheet(title="Dados do Checklist")  # Cria a terceira aba

    # Converte os parâmetros de entrada
    DataDeInicio = datetime.strptime(DataDeInicio, '%Y-%m-%dT%H:%M').replace(tzinfo=None)if DataDeInicio and DataDeInicio != "None" else None
    DataDeConclusao = datetime.strptime(DataDeConclusao, '%Y-%m-%dT%H:%M').replace(tzinfo=None)if DataDeConclusao and DataDeConclusao != "None" else None
    ServicosEscalados = ServicosEscalados.split(',')
    ColaboradoresEscalados = ColaboradoresEscalados.split(',')
    status_list = status.split(',')

    # Seleciona cabeçalhos e coleta dados para a aba de serviços
    dados = colect_dados_agendamentos_limpeza_predial(
        request=request,
        userid=userid,
        DataDeInicio=DataDeInicio,
        DataDeConclusao=DataDeConclusao,
        ServicosEscalados=ServicosEscalados,
        Areas=Areas,
        TipoServico=TipoServico,
        ColaboradoresEscalados=ColaboradoresEscalados,
        status=status_list
    )

    # Definindo as colunas com seus tipos, conforme o código original
    colunas = [
        ('tipodeempresa', None),
        ('empresaprestadora', None),
        ('id_agendamento', None),
        ('id_random_agendamento', None),
        ('id_config', None),
        ('tipo_agendamento', None),
        ('descricao_do_servico', None),
        ('servicos_solicitados', None),
        ('servicos_solicitados_id', None),
        ('servicos_solicitados_id_random', None),
        ('data_de_inicio', 'data'),  # Tratamento especial para data
        ('data_de_conclusao', 'data'),  # Tratamento especial para data
        ('status_servico', None),
        ('area_atendida', None),
        ('area_atendida_id', None),
        ('id_random_area', None),
        ('area_total', None),
        ('localidade', None),
        ('lat', None),
        ('long', None),
        ('unidade', None)
    ]

    # Chamando as funções
    adicionar_cabecalhos(ws_agendadamentos, headers_report_schedules)
    adicionar_dados(ws_agendadamentos, dados, colunas, headers_report_schedules)

    # Dados de acompanhamento
    dados = colect_dados_fato_servico_limpeza_predial(
        request=request,
        userid=userid,
        DataDeInicio=DataDeInicio,
        DataDeConclusao=DataDeConclusao,
        ServicosEscalados=ServicosEscalados,
        ColaboradoresEscalados=ColaboradoresEscalados,
        TipoServico=TipoServico,
        Areas=Areas,
        status=status.split(',')
    )

    # Obter todos os IDs únicos de uma vez
    ids_random_agendamentos = {dado.id_random_agendamento for dado in dados}

    # Filtrar todos os dados de uma vez
    dados_acompanhamento = dados.filter(id_random_agendamento__in=ids_random_agendamentos)

    # Definindo as colunas com seus tipos, conforme o código original
    colunas = [
        ('id_acompanhamento', None),
        ('id_random_acompanhamento', None),
        ('id_agendamento', None),
        ('id_random_agendamento', None),
        ('colaboradores_chamados_id', None),
        ('colaboradores_chamados_id_random', None),
        ('colaboradores_chamados', None),
        ('data_hora_chegada', 'data'),  # Tratamento especial para data
        ('data_hora_retorno', 'data'),  # Tratamento especial para data
        ('tempo_na_area', None),
        ('depois', None),
    ]

    # Chamando as funções
    adicionar_cabecalhos(ws_acompanhamento, headers_report_services)
    adicionar_dados(ws_acompanhamento, dados_acompanhamento, colunas, headers_report_services)

    # Define cabeçalhos para a aba de checklists
    checklist_headers = [
        "Agendamento.ID", "Agendamento.Descrição", "Checklist.Descrição",
        "Checklist.Foto", "Checklist.AtualizadoEm", "Checklist.Status"
    ]

    dados_checklist = CheckListLimpezaPredial.objects.filter(servico_agendado__id_random__in=ids_random_agendamentos)

    colunas_checklist = [
        ('servico_agendado.id', 'nested'),  # Atributo aninhado
        ('servico_agendado.DescricaoDoServico', 'nested'),  # Atributo aninhado
        ('descricao', None),
        ('foto_comprovacao', 'url'),  # URL ou "N/A"
        ('atualizado_em', 'datetime_str'),  # Formato de data/hora
        ('status', None)
    ]

    adicionar_cabecalhos(ws_checklists, checklist_headers)
    adicionar_dados(ws_checklists, dados_checklist, colunas_checklist, checklist_headers)

    for col in range(1, len(checklist_headers) + 1):
        ws_checklists.column_dimensions[ws_checklists.cell(row=1, column=col).column_letter].width = 25

    # Configura a resposta HTTP
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="relatorio_de_servicos_{status}_{generate_id_random()}.xlsx"'

    # Salva o arquivo Excel na resposta
    wb.save(response)

    return response