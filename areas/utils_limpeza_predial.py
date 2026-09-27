from dashboards.data_visualization_limpeza_predial import data_visualization_limpeza_predial_graphs
from django.db.models import Sum


def data_visualization_limpeza_predial_indicadores(request, userid, dados):
    # Obter as unidades distintas
    unidades = dados.values_list('localidade__unidade__nome', flat=True).distinct().count()

    # Calcular a área total mobilizada
    area_total_mobilizada = dados.filter(status='Mobilizado').aggregate(
        total_mobilizada=Sum('dimensao')
    )['total_mobilizada'] or 0

    # Calcular a área total desmobilizada
    area_total_desmobilizada = dados.filter(status='Desmobilizado').aggregate(
        total_desmobilizada=Sum('dimensao')
    )['total_desmobilizada'] or 0

    # Obter as localidades distintas
    localidades = dados.values_list('localidade__nome', flat=True).distinct().count()

    return (unidades, area_total_mobilizada, area_total_desmobilizada, localidades)


def graphs_limpeza_predial_to_html(request, userid, dados):
    fig_area_unidades_mobilizadas = data_visualization_limpeza_predial_graphs(request, userid, dados).create_fig(
        name_fig='fig_area_unidades_mobilizadas',
        filters={'localidade__unidade__status': 'Mobilizado'},
        field_name='localidade__unidade__nome',
        title='Área Total por unidade (Mobilizadas)',
        label_type='Unidade',
        color='#30a444',
        filter_time=False,
        sum_by='dimensao',
        count_by='id',
    )

    fig_area_unidades_desmobilizadas = data_visualization_limpeza_predial_graphs(request, userid, dados).create_fig(
        name_fig='fig_area_unidades_desmobilizadas',
        filters={'localidade__unidade__status': 'Desmobilizado'},
        field_name='localidade__unidade__nome',
        title='Área Total por unidade (Desmobilizado)',
        label_type='Unidade',
        color='#f6be04',
        filter_time=False,
        sum_by='dimensao',
        count_by='id',
    )

    fig_area_localidades_mobilizadas = data_visualization_limpeza_predial_graphs(request, userid, dados).create_fig(
        name_fig='fig_area_localidades_mobilizadas',
        filters={'localidade__status': 'Mobilizado'},
        field_name='localidade__nome',
        title='Área Total por localidade (Mobilizadas)',
        label_type='Localidade',
        color='#30a444',
        filter_time=False,
        sum_by='dimensao',
        count_by='id',
    )

    fig_area_localidades_desmobilizadas = data_visualization_limpeza_predial_graphs(request, userid, dados).create_fig(
        name_fig='fig_area_localidades_desmobilizadas',
        filters={'localidade__status': 'Desmobilizado'},
        field_name='localidade__nome',
        title='Área Total por localidade (Desmobilzadas)',
        label_type='Localidade',
        color='#f6be04',
        filter_time=False,
        sum_by='dimensao',
        count_by='id',
    )


    return (fig_area_unidades_mobilizadas, fig_area_unidades_desmobilizadas,
            fig_area_localidades_mobilizadas, fig_area_localidades_desmobilizadas)