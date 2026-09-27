import openpyxl
from servicos.headers_report_jardinagem import headers_report_services, headers_report_schedules
from servicos.utils_jardinagem import colect_dados_fato_servico_jardinagem, colect_dados_agendamentos_jardinagem
from django.http import HttpResponse
from utils.utils import generate_id_random
from datetime import datetime
from permissionscontrol.utils import verify_login
from django.shortcuts import redirect
from relatorios.utils_xlsx import adicionar_cabecalhos, adicionar_dados

def exportar_relatorio_de_serivos_Jardinagem_excel(
    request, userid, status, DataDeInicio, DataDeConclusao, Areas,
    TipoServico, ServicosEscalados, ColaboradoresEscalados
    ):
    # Verifica login
    block = verify_login(request=request, userid=userid)
    if block:
        return redirect('logout')

    # Configuração inicial do workbook
    wb = openpyxl.Workbook()
    ws_agendadamentos = wb.active
    ws_agendadamentos.title = "Relatório de agendamentos jardinagem"
    ws_acompanhamento = wb.create_sheet(title="Relatório de acompanhamento")  # Cria a segunda aba

    # Converte os parâmetros de entrada
    DataDeInicio = datetime.strptime(DataDeInicio, '%Y-%m-%dT%H:%M').replace(tzinfo=None) if DataDeInicio and DataDeInicio != "None" else None
    DataDeConclusao = datetime.strptime(DataDeConclusao, '%Y-%m-%dT%H:%M').replace(tzinfo=None) if DataDeConclusao and DataDeConclusao != "None" else None
    ServicosEscalados = ServicosEscalados.split(',')
    ColaboradoresEscalados = ColaboradoresEscalados.split(',')

    # Dados de agendamento
    # Seleciona cabeçalhos e coleta dados
    dados = colect_dados_agendamentos_jardinagem(
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

    # Definindo as colunas com seus tipos, conforme o código original
    colunas = [
        ('tipodeempresa', None),
        ('empresaprestadora', None),
        ('id_agendamento', None),
        ('id_random_agendamento', None),
        ('id_config', None),
        ('tipo_agendamento', None),
        ('descricao_do_servico', None),
        ('colaboradores_chamados', None),
        ('colaboradores_chamados_id', None),
        ('colaboradores_chamados_id_random', None),
        ('servicos_solicitados', None),
        ('servicos_solicitados_id', None),
        ('servicos_solicitados_id_random', None),
        ('data_de_inicio', 'data'),  # Tratamento especial para data
        ('data_de_conclusao', 'data'),  # Tratamento especial para data
        ('antes', None),
        ('depois', None),
        ('status_servico', None),
        ('area_atendida', None),
        ('area_atendida_id', None),
        ('id_random_area', None),
        ('periodicidade_de_retorno', None),
        ('area_total', None),
        ('tipo_vegetacao', None),
        ('tipo_terreno', None),
        ('localidade', None),
        ('lat', None),
        ('long', None),
        ('unidade', None)
    ]

    # Chamando as funções
    adicionar_cabecalhos(ws_agendadamentos, headers_report_schedules)
    adicionar_dados(ws_agendadamentos, dados, colunas, headers_report_schedules)

    # Dados de acompanhamento
    dados = colect_dados_fato_servico_jardinagem(
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
    ]

    # Chamando as funções
    adicionar_cabecalhos(ws_acompanhamento, headers_report_services)
    adicionar_dados(ws_acompanhamento, dados_acompanhamento, colunas, headers_report_services)

    # Configura a resposta HTTP
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="relatorio_de_servicos_{status}_{generate_id_random()}.xlsx"'

    # Salva o Excel na resposta
    wb.save(response)

    return response