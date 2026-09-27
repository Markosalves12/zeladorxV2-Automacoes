from django.shortcuts import render, reverse, redirect
from areas.models_jardinagem import AreasJardins
from empresasecundario.utils import define_empresas
from permissionscontrol.utils import verify_login, validate_permissions
from utils.utils import aplicar_filtros_dinamicos
from areas.forms_jardinagem import AreasJardinsForms
from areas.utils_jardinagem import graphs_jardinagem_to_html, data_visualization_jardinagem_indicadores

def dashboard_administrativo_jardinagem(request, userid):
    block = verify_login(request=request, userid=userid)

    if block == True:
        return redirect('logout')

    empresas = define_empresas(request=request, userid=userid)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']
    setores = empresas['setores']

    tipos = [
        {'nome': 'Dashboards Administrativos', 'link': ''},
    ]

    if setores['habilitar_jardinagem_secundaria'] and setores['habilitar_jardinagem']:
        tipos.insert(1, {'nome': 'Jardinagem',
                         'link': reverse('dashboard_administrativo_jardinagem', kwargs={'userid': userid})}, )
    else:
        return redirect('dashboard_administrativo_limpeza_predial', userid)

    if setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']:
        tipos.insert(2, {'nome': 'Limpeza predial',
                         'link': reverse('dashboard_administrativo_limpeza_predial', kwargs={'userid': userid})}, )


    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['381: Pode visualizar o dashboard administrativo']
    )

    dados = AreasJardins.objects.distinct().filter(
        localidade__unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
        localidade__unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
    )

    filtro_mapeamento = {
        'Terreno': 'Terreno__id',
        'vegetacao': 'vegetacao__id',
        'servico': 'servico__id',
        'localidade': 'localidade__id'
    }

    if request.method == 'GET':
        get_data = request.GET.dict()
        dados = aplicar_filtros_dinamicos(dados, get_data, filtro_mapeamento)

    (unidades, area_total_mobilizada, area_total_desmobilizada, localidades) = data_visualization_jardinagem_indicadores(request, userid, dados)

    (fig_area_unidades_mobilizadas, fig_area_unidades_desmobilizadas,
     fig_area_localidades_mobilizadas, fig_area_localidades_desmobilizadas,
     fig_area_terrenos_mobilizados, fig_area_terrenos_desmobilizados,
     fig_area_vegetacao_mobilizadas, fig_area_vegetacao_desmobilizadas,
     fig_area_periodicidade) = graphs_jardinagem_to_html(request, userid, dados)

    return render(
        request=request,
        template_name='dashboards/dashboard_administrativo.html',
        context={
            'permission_view': permission_view,
            'app_name': 'Dashboard administrativo jardinagem',
            'link_tipos': tipos,
            'unidades': unidades,
            'area_total_mobilizada': area_total_mobilizada,
            'area_total_desmobilizada': area_total_desmobilizada,
            'localidades': localidades,
            'por_terreno': True,
            'por_colaborador': True,
            'form_search': AreasJardinsForms(request=request, userid=userid, type='search'),
            'sform_search': True,
            'allowed_fields': list(filtro_mapeamento.keys()),
            **fig_area_unidades_mobilizadas,
            **fig_area_unidades_desmobilizadas,
            **fig_area_localidades_mobilizadas,
            **fig_area_localidades_desmobilizadas,
            **fig_area_terrenos_mobilizados,
            **fig_area_terrenos_desmobilizados,
            **fig_area_vegetacao_mobilizadas,
            **fig_area_vegetacao_desmobilizadas,
            **fig_area_periodicidade
        }
    )