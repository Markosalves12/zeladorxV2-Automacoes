from servicos.utils_limpeza_predial import query_servicos_limpeza_predial_agendados_anotados
from servicos.forms_limpeza_predial import ServicoLimpezaPredialAgendadoForms
from django.urls import reverse
from utils.views import generic_view
from permissionscontrol.utils import validate_permissions
from empresasecundario.utils import define_empresas
from django.shortcuts import redirect

# Create your views here.
def relatorios_de_servicos_limpeza_predial_xlsx_concluidos(request, userid):
    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['310: Pode extrair relatórios XLSX de limpeza predial']
    )

    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'Areas', 'label': 'Área atendidada'},
        {'nome': 'DescricaoDoServico', 'label': 'Descrição'},
        {'nome': 'DataDeInicio', 'label': 'Data de inicio'},
        {'nome': 'DataDeConclusao', 'label': 'Data de conclusão'},
        {'nome': 'ServicosEscalados', 'label': 'Serivos planejados'},
        {'nome': 'TipoServico', 'label': 'Tipo de agendamento'},
        {'nome': 'status', 'label': 'Status'},
    ]

    empresas = define_empresas(request=request, userid=userid)
    setores = empresas['setores']

    tipos = [
        {'nome': 'Relatório de serviços', 'link': ''},
    ]

    if setores['habilitar_jardinagem_secundaria'] and setores['habilitar_jardinagem']:
        tipos.insert(1, {
            'nome': 'Serviços concluidos, Jardinagem XLSX',
            'link': reverse(
                'relatorios_de_servicos_jardinagem_xlsx_concluidos',
                kwargs={
                    'userid': userid
                }
            )
        })

    if setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']:
        tipos.insert(2, {
            'nome': 'Serviços concluidos, Limpeza predial XLSX',
            'link': reverse(
                'relatorios_de_servicos_limpeza_predial_xlsx_concluidos',
                kwargs={
                    'userid': userid,
                }
            )
        })
    else:
        return redirect('relatorios_de_servicos_jardinagem_xlsx_concluidos', userid)

    return generic_view(
        request=request,
        model=query_servicos_limpeza_predial_agendados_anotados(
            request,
            userid,
            status_list=['Concluido']
        ),
        form_class=ServicoLimpezaPredialAgendadoForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_servico_limpeza_predial_agendado',
        app_name='relatório de serviços limpeza predial xlsx - Concluidos',
        form_search=ServicoLimpezaPredialAgendadoForms(request=request, userid=userid, type='search'),
        sform_search=True,
        filtro_mapeamento={
            'Areas': 'Areas__id',
            'TipoServico': 'TipoServico',
            'ServicosEscalados': 'ServicosEscalados__id',
            'DataDeInicio': 'DataDeInicio',
            'DataDeConclusao': 'DataDeConclusao'
        },
        text_button_open_modal='Adicionar nova manutenção',
        text_button_save='Salvar manutenção',
        header_model='Nova manutenção',
        redirect_url='unidades',
        button_export_tittle='Exportar Excel',
        button_export_link='exportar_relatorio_de_serivos_limpeza_predial_excel',
        button_export_link_with_checklists='exportar_relatorio_de_serivos_limpeza_predial_excel_with_checklist',
        status=['Concluido'],
        link_tipos=tipos,
        modal_button=False,
        userid=userid,
        permission_view=permission_view
    )



def relatorios_de_servicos_limpeza_predial_xlsx_agendados(request, userid):
    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['310: Pode extrair relatórios XLSX de limpeza predial']
    )

    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'Areas', 'label': 'Área atendidada'},
        {'nome': 'DescricaoDoServico', 'label': 'Descrição'},
        {'nome': 'DataDeInicio', 'label': 'Data de inicio'},
        {'nome': 'DataDeConclusao', 'label': 'Data de conclusão'},
        {'nome': 'Areas', 'label': 'Área atendida'},
        {'nome': 'ServicosEscalados', 'label': 'Serivos planejados'},
        {'nome': 'TipoServico', 'label': 'Tipo de agendamento'},
        {'nome': 'novo_status', 'label': 'Status'},
        {'nome': 'acoes', 'label': 'Ações'},
    ]

    empresas = define_empresas(request=request, userid=userid)
    setores = empresas['setores']

    tipos = [
        {'nome': 'Relatório de serviços', 'link': ''},
    ]

    if setores['habilitar_jardinagem_secundaria'] and setores['habilitar_jardinagem']:
        tipos.insert(1, {
            'nome': 'Serviços agendados, Jardinagem XLSX',
            'link': reverse(
                'relatorios_de_servicos_jardinagem_xlsx_agendados',
                kwargs={'userid': userid}
            )
        })

    if setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']:
        tipos.insert(2, {
            'nome': 'Serviços agendados, Limpeza predial XLSX',
            'link': reverse(
                'relatorios_de_servicos_limpeza_predial_xlsx_agendados',
                kwargs={'userid': userid}
            )
        })
    else:
        return redirect('relatorios_de_servicos_jardinagem_xlsx_agendados', userid)

    return generic_view(
        request=request,
        model=query_servicos_limpeza_predial_agendados_anotados(
            request,
            userid,
            status_list=['Agendado', 'Em andamento']
        ),
        form_class=ServicoLimpezaPredialAgendadoForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_servico_limpeza_predial_agendado',
        app_name='relatório de serviços limpeza predial xlsx - Planejados',
        form_search=ServicoLimpezaPredialAgendadoForms(request=request, userid=userid, type='search'),
        sform_search=True,
        filtro_mapeamento={
            'Areas': 'Areas__id',
            'TipoServico': 'TipoServico',
            'ServicosEscalados': 'ServicosEscalados__id',
            'DataDeInicio': 'DataDeInicio',
            'DataDeConclusao': 'DataDeConclusao'
        },
        text_button_open_modal='Adicionar nova manutenção',
        text_button_save='Salvar manutenção',
        header_model='Nova manutenção',
        redirect_url='unidades',
        button_export_tittle='Exportar Excel',
        button_export_link='exportar_relatorio_de_serivos_limpeza_predial_excel',
        button_export_link_with_checklists='exportar_relatorio_de_serivos_limpeza_predial_excel_with_checklist',
        status=['Agendado', 'Em andamento'],
        modal_button=False,
        link_tipos=tipos,
        userid=userid,
        permission_view=permission_view
    )
