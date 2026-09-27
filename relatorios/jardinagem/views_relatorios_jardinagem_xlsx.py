from servicos.utils_jardinagem import query_servicos_jardinagem_agendados_anotados
from servicos.forms_jardinagem import ServicoJaridinagemAgendadoForms
from django.urls import reverse
from utils.views import generic_view
from permissionscontrol.utils import validate_permissions
from empresasecundario.utils import define_empresas
from django.shortcuts import redirect

# Create your views here.
def relatorios_de_servicos_jardinagem_xlsx_concluidos(request, userid):
    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['310: Pode extrair relatórios XLSX de jardinagem']
    )

    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'Areas', 'label': 'Área atendidada'},
        {'nome': 'DescricaoDoServico', 'label': 'Descrição'},
        {'nome': 'DataDeInicio', 'label': 'Data de inicio'},
        {'nome': 'DataDeConclusao', 'label': 'Data de conclusão'},
        {'nome': 'ServicosEscalados', 'label': 'Serivos planejados'},
        {'nome': 'ColaboradoresEscalados', 'label': 'Colaboradores escalados'},
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
                kwargs={'userid': userid}
            )
        })
    else:
        return redirect('relatorios_de_servicos_limpeza_predial_xlsx_concluidos', userid)

    if setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']:
        tipos.insert(2, {
            'nome': 'Serviços concluidos, Limpeza predial XLSX',
            'link': reverse(
                'relatorios_de_servicos_limpeza_predial_xlsx_concluidos',
                kwargs={'userid': userid}
            )
        })

    return generic_view(
        request=request,
        model=query_servicos_jardinagem_agendados_anotados(
            request,
            userid,
            status_list=['Concluido']
        ),
        form_class=ServicoJaridinagemAgendadoForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_servico_jardinagem_agendado',
        app_name='relatório de serviços jardinagem xlsx - Concluidos',
        form_search=ServicoJaridinagemAgendadoForms(request=request, userid=userid, type='search'),
        sform_search=True,
        filtro_mapeamento={
            'Areas': 'Areas__id',
            'TipoServico': 'TipoServico',
            'ServicosEscalados': 'ServicosEscalados__id',
            'ColaboradoresEscalados': 'ColaboradoresEscalados__id',
            'DataDeInicio': 'DataDeInicio',
            'DataDeConclusao': 'DataDeConclusao'
        },
        text_button_open_modal='Adicionar nova manutenção',
        text_button_save='Salvar manutenção',
        header_model='Nova manutenção',
        redirect_url='unidades',
        button_export_tittle='Exportar Excel',
        status=['Concluido'],
        button_export_link='exportar_relatorio_de_serivos_Jardinagem_excel',
        button_export_link_with_checklists='exportar_relatorio_de_serivos_Jardinagem_excel_with_checklist',
        link_tipos=tipos,
        modal_button=False,
        userid=userid,
        permission_view=permission_view
    )



def relatorios_de_servicos_jardinagem_xlsx_agendados(request, userid):
    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['310: Pode extrair relatórios XLSX de jardinagem']
    )

    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'Areas', 'label': 'Área atendidada'},
        {'nome': 'DescricaoDoServico', 'label': 'Descrição'},
        {'nome': 'DataDeInicio', 'label': 'Data de inicio'},
        {'nome': 'DataDeConclusao', 'label': 'Data de conclusão'},
        {'nome': 'ServicosEscalados', 'label': 'Serivos planejados'},
        {'nome': 'ColaboradoresEscalados', 'label': 'Colaboradores escalados'},
        {'nome': 'TipoServico', 'label': 'Tipo de agendamento'},
        {'nome': 'novo_status', 'label': 'Status'},
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
    else:
        return redirect('relatorios_de_servicos_limpeza_predial_xlsx_agendados', userid)

    if setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']:
        tipos.insert(2, {
            'nome': 'Serviços agendados, Limpeza predial XLSX',
            'link': reverse(
                'relatorios_de_servicos_limpeza_predial_xlsx_agendados',
                kwargs={'userid': userid}
            )
        })

    return generic_view(
        request=request,
        model=query_servicos_jardinagem_agendados_anotados(
            request,
            userid,
            status_list=['Agendado', 'Em andamento']
        ),
        form_class=ServicoJaridinagemAgendadoForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_servico_jardinagem_agendado',
        app_name='relatório de serviços jardinagem xlsx - Planejados',
        form_search=ServicoJaridinagemAgendadoForms(request=request, userid=userid, type='search'),
        sform_search=True,
        filtro_mapeamento={
            'Areas': 'Areas__id',
            'TipoServico': 'TipoServico',
            'ServicosEscalados': 'ServicosEscalados__id',
            'ColaboradoresEscalados': 'ColaboradoresEscalados__id',
            'DataDeInicio': 'DataDeInicio',
            'DataDeConclusao': 'DataDeConclusao'
        },
        text_button_open_modal='Adicionar nova manutenção',
        text_button_save='Salvar manutenção',
        header_model='Nova manutenção',
        redirect_url='unidades',
        button_export_tittle='Exportar Excel',
        status=['Agendado', 'Em andamento'],
        button_export_link='exportar_relatorio_de_serivos_Jardinagem_excel',
        button_export_link_with_checklists='exportar_relatorio_de_serivos_Jardinagem_excel_with_checklist',
        modal_button=False,
        link_tipos=tipos,
        userid=userid,
        permission_view=permission_view
    )
