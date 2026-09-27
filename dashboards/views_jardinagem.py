from django.shortcuts import render, reverse, redirect
from dashboards.data_visualization_jardinagem import data_visualization_jardinagem_indicadores
from servicos.forms_jardinagem import ServicoJaridinagemAgendadoForms
from utils.utils import aplicar_filtros_dinamicos
from dashboards.utils_jardinagem import colect_dados_jardinagem
from dashboards.utils_jardinagem import graphs_jardinagem_to_html
from empresasecundario.utils import define_empresas
from permissionscontrol.utils import verify_login, validate_permissions


# Create your views here.
def dashboard_produtividade_jardinagem(request, userid):
    block = verify_login(request=request, userid=userid)

    if block == True:
        return redirect('logout')

    empresas = define_empresas(request=request, userid=userid)
    setores = empresas['setores']

    tipos = [
        {'nome': 'Dashboards', 'link': ''},
    ]

    if setores['habilitar_jardinagem_secundaria'] and setores['habilitar_jardinagem']:
        tipos.insert(1, {'nome': 'Jardinagem', 'link': reverse('dashboard_produtividade_jardinagem', kwargs={'userid': userid})},)
    else:
        return redirect('dashboard_produtividade_limpeza_predial', userid)

    if setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']:
        tipos.insert(2, {'nome': 'Limpeza predial', 'link': reverse('dashboard_produtividade_limpeza_predial', kwargs={'userid': userid})},)

    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['380: Pode visualizar o dashboard gerencial']
    )

    agendado = colect_dados_jardinagem(
        request=request,
        userid=userid
    )

    filtro_mapeamento = {
        'Areas': 'Areas__id',
        'TipoServico': 'TipoServico',
        'ServicosEscalados': 'ServicosEscalados__id',
        'ColaboradoresEscalados': 'ColaboradoresEscalados__id',
        'DataDeInicio': 'DataDeInicio',
        'DataDeConclusao': 'DataDeConclusao'
    }

    if request.method == 'GET':
        get_data = request.GET.dict()
        agendado = aplicar_filtros_dinamicos(agendado, get_data, filtro_mapeamento)

    (em_andamento, atrasados, proximos, agendamentos) = data_visualization_jardinagem_indicadores(request, userid, agendado)

    (fig_area_terreno_atrasado, fig_area_area_atrasado, fig_area_localidade_atrasado,
     fig_area_colaborador_atrasado, fig_area_terreno_proximo, fig_area_localidade_proximo,
     fig_area_area_proximo, fig_area_colaborador_proximo, fig_area_terreno_agendados,
     fig_area_localidade_agendados, fig_area_area_agendados, fig_area_colaborador_agendados,
     fig_area_terreno_em_andamento, fig_area_localidade_em_andamento,
     fig_area_area_em_andamento,fig_area_colaborador_em_andamento, fig_mes_html) = graphs_jardinagem_to_html(request, userid, agendado)

    return render(
        request=request,
        template_name='dashboards/dashboard_produtividade.html',
        context={
            'permission_view': permission_view,
            'app_name': 'Dashboard gerencial jardinagem',
            'link_tipos': tipos,
            'agendamentos': agendamentos,
            'proximos': proximos,
            'atrasados': atrasados,
            'em_andamento': em_andamento,
            'por_terreno': True,
            'por_colaborador': True,
            'form_search': ServicoJaridinagemAgendadoForms(request=request, userid=userid, type='search'),
            'sform_search': True,
            'allowed_fields': list(filtro_mapeamento.keys()),
            **fig_area_terreno_atrasado,
            **fig_area_area_atrasado,
            **fig_area_localidade_atrasado,
            **fig_area_colaborador_atrasado,
            **fig_area_terreno_proximo,
            **fig_area_localidade_proximo,
            **fig_area_area_proximo,
            **fig_area_colaborador_proximo,
            **fig_area_terreno_agendados,
            **fig_area_localidade_agendados,
            **fig_area_area_agendados,
            **fig_area_colaborador_agendados,
            **fig_area_terreno_em_andamento,
            **fig_area_localidade_em_andamento,
            **fig_area_area_em_andamento,
            **fig_area_colaborador_em_andamento,
            **fig_mes_html
        }
    )