from servicos.models_limpeza_predial import ServicoLimpezaPredialAgendado
from django.db.models import F, ExpressionWrapper, IntegerField
from django.db.models.functions import Now
from empresasecundario.utils import define_empresas
from utils.utils import define_range_time
from dashboards.data_visualization_limpeza_predial import data_visualization_limpeza_predial_graphs

def colect_dados_limpeza_predial(request, userid):
    empresas = define_empresas(request=request, userid=userid)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    dados = ServicoLimpezaPredialAgendado.objects.all().annotate(
        data_atual=Now(),
        status_agendamento=ExpressionWrapper(
            F('DataDeInicio') - F('data_atual'),
            output_field=IntegerField()
        ) / (3600 * 24 * 1000000)
    ).distinct().filter(
        Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
        Areas__localidade__unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
        status__in=['Agendado', 'Em andamento']
    )

    return dados

def graphs_limpeza_predial_to_html(request, userid, agendado):
    one_day, seven_days = define_range_time()

    fig_area_area_atrasado = data_visualization_limpeza_predial_graphs(request, userid, agendado).create_fig(
        name_fig='fig_area_area_atrasado',
        filters={'status': 'Agendado'},
        field_name='Areas__nome',
        title='Área Total por área verde (Atrasados)',
        label_type='Área',
        color='#dc3444',
        filter_time={'DataDeInicio__lt': one_day},
        sum_by='Areas__dimensao',
        count_by='id',
    )

    fig_area_localidade_atrasado = data_visualization_limpeza_predial_graphs(request, userid, agendado).create_fig(
        name_fig='fig_area_localidade_atrasado',
        filters={'status': 'Agendado'},
        field_name='Areas__localidade__nome',
        title='Área Total por localidade (Atrasados)',
        label_type='Área',
        color='#dc3444',
        filter_time={'DataDeInicio__lt': one_day},
        sum_by='Areas__dimensao',
        count_by='id',
    )

    fig_area_localidade_proximo = data_visualization_limpeza_predial_graphs(request, userid, agendado).create_fig(
        name_fig='fig_area_localidade_proximo',
        filters={'status': 'Agendado'},
        field_name='Areas__localidade__nome',
        title='Área Total por localidade (Próximos)',
        label_type='Localidade',
        color='#f6be04',
        filter_time={'DataDeInicio__gte': one_day, 'DataDeInicio__lte': seven_days},
        sum_by='Areas__dimensao',
        count_by='id',
    )

    fig_area_area_proximo = data_visualization_limpeza_predial_graphs(request, userid, agendado).create_fig(
        name_fig='fig_area_area_proximo',
        filters={'status': 'Agendado'},
        field_name='Areas__nome',
        title='Área Total por área verde (Próximos)',
        label_type='Área',
        color='#f6be04',
        filter_time={'DataDeInicio__gte': one_day, 'DataDeInicio__lte': seven_days},
        sum_by='Areas__dimensao',
        count_by='id',
    )

    fig_area_localidade_agendados = data_visualization_limpeza_predial_graphs(request, userid, agendado).create_fig(
        name_fig='fig_area_localidade_agendados',
        filters={'status': 'Agendado'},
        field_name='Areas__localidade__nome',
        title='Área Total por localidade (agendados)',
        label_type='Localidade',
        color='#14a0b6',
        filter_time={'DataDeInicio__gte': seven_days},
        sum_by='Areas__dimensao',
        count_by='id',
    )

    fig_area_area_agendados = data_visualization_limpeza_predial_graphs(request, userid, agendado).create_fig(
        name_fig='fig_area_area_agendados',
        filters={'status': 'Agendado'},
        field_name='Areas__nome',
        title='Área Total por área linmpeza predial (agendados)',
        label_type='Área',
        color='#14a0b6',
        filter_time={'DataDeInicio__gte': seven_days},
        sum_by='Areas__dimensao',
        count_by='id',
    )

    fig_area_localidade_em_andamento = data_visualization_limpeza_predial_graphs(request, userid, agendado).create_fig(
        name_fig='fig_area_localidade_em_andamento',
        filters={'status': 'Em andamento'},
        field_name='Areas__localidade__nome',
        title='Área Total por localidade (em andamento)',
        label_type='Localidade',
        color='#2aa042',
        sum_by='Areas__dimensao',
        count_by='id',
    )

    fig_area_area_em_andamento = data_visualization_limpeza_predial_graphs(request, userid, agendado).create_fig(
        name_fig='fig_area_area_em_andamento',
        filters={'status': 'Em andamento'},
        field_name='Areas__nome',
        title='Área Total por área verde (em andamento)',
        label_type='Área',
        color='#2aa042',
        sum_by='Areas__dimensao',
        count_by='id',
    )

    fig_mes_html = data_visualization_limpeza_predial_graphs(request, userid, agendado).define_figs_by_months(
        name_fig='fig_mes_html',
        filters={'status': 'Agendado'},
        field_name='Areas__localidade__nome',
        title='Serviços por Mês/localidade (Agendado)',
        label_type='Localidades',
        color='#2aa042',
        sum_by='Areas__dimensao',
        count_by='id',
        date_column='DataDeInicio'
    )

    return (fig_area_area_atrasado, fig_area_localidade_atrasado, fig_area_localidade_proximo,
            fig_area_area_proximo, fig_area_localidade_agendados, fig_area_area_agendados,
            fig_area_localidade_em_andamento, fig_area_area_em_andamento, fig_mes_html)