from utils.utils import define_range_time
from dashboards.data_visualization_limpeza_predial import data_visualization_limpeza_predial_graphs


def graphs_limpeza_predial_concluido_to_reports(request, userid, agendado):
    figs_concluidos_localidade = data_visualization_limpeza_predial_graphs(request, userid, agendado).create_fig_report(
        name_fig='figs_concluidos_localidade',
        filters={'status': 'Concluido'},
        field_name='Areas__localidade__nome',
        title='Área Total por localidade (Concluido)',
        label_type='Localidade',
        color='#020d3f',
        sum_by='Areas__dimensao',
        count_by='id',
    )

    figs_concluidos_area = data_visualization_limpeza_predial_graphs(request, userid, agendado).create_fig_report(
        name_fig='figs_concluidos_area',
        filters={'status': 'Concluido'},
        field_name='Areas__nome',
        title='Área Total por área verde (Concluido)',
        label_type='Área',
        color='#020d3f',
        sum_by='Areas__dimensao',
        count_by='id',
    )


    figs_concluidos_servico = data_visualization_limpeza_predial_graphs(request, userid, agendado).create_fig_report(
        name_fig='figs_concluidos_servico',
        filters={'status': 'Concluido'},
        field_name='ServicosEscalados__nome',
        title='Área Total por serviço (Concluido)',
        label_type='Serviços',
        color='#020d3f',
        sum_by='Areas__dimensao',
        count_by='id',
    )

    return figs_concluidos_localidade, figs_concluidos_area, figs_concluidos_servico

def graphs_limpeza_predial__proximo_to_reports(request, userid, agendado):
    one_day, seven_days = define_range_time()
    figs_proximo_localidade = data_visualization_limpeza_predial_graphs(request, userid, agendado).create_fig_report(
        name_fig='figs_concluidos_localidade',
        filters={'status': 'Agendado'},
        field_name='Areas__localidade__nome',
        title='Área Total por localidade (Próximo)',
        label_type='Localidade',
        color='#f6be04',
        sum_by='Areas__dimensao',
        count_by='id',
        filter_time={'DataDeInicio__gte': one_day, 'DataDeInicio__lte': seven_days},
    )

    figs_proximo_area = data_visualization_limpeza_predial_graphs(request, userid, agendado).create_fig_report(
        name_fig='figs_concluidos_area',
        filters={'status': 'Agendado'},
        field_name='Areas__nome',
        title='Área Total por área verde (Próximo)',
        label_type='Área',
        color='#f6be04',
        sum_by='Areas__dimensao',
        count_by='id',
        filter_time={'DataDeInicio__gte': one_day, 'DataDeInicio__lte': seven_days},
    )

    figs_proximo_servico = data_visualization_limpeza_predial_graphs(request, userid, agendado).create_fig_report(
        name_fig='figs_concluidos_servico',
        filters={'status': 'Agendado'},
        field_name='ServicosEscalados__nome',
        title='Área Total por serviço (Próximo)',
        label_type='Serviços',
        color='#f6be04',
        sum_by='Areas__dimensao',
        count_by='id',
        filter_time={'DataDeInicio__gte': one_day, 'DataDeInicio__lte': seven_days},
    )

    return figs_proximo_localidade, figs_proximo_area, figs_proximo_servico


def graphs_limpeza_predial_atrasado_to_reports(request, userid, agendado):
    one_day, seven_days = define_range_time()
    figs_atrasado_localidade = data_visualization_limpeza_predial_graphs(request, userid, agendado).create_fig_report(
        name_fig='figs_atrasado_localidade',
        filters={'status': 'Agendado'},
        field_name='Areas__localidade__nome',
        title='Área Total por localidade (Atrasados)',
        label_type='Localidade',
        color='#dc3444',
        sum_by='Areas__dimensao',
        count_by='id',
        filter_time={'DataDeInicio__lt': one_day},
    )

    figs_atrasado_area = data_visualization_limpeza_predial_graphs(request, userid, agendado).create_fig_report(
        name_fig='figs_atrasado_area',
        filters={'status': 'Agendado'},
        field_name='Areas__nome',
        title='Área Total por área verde (Atrasados)',
        label_type='Área',
        color='#dc3444',
        sum_by='Areas__dimensao',
        count_by='id',
        filter_time={'DataDeInicio__lt': one_day},
    )

    figs_atrasado_servico = data_visualization_limpeza_predial_graphs(request, userid, agendado).create_fig_report(
        name_fig='figs_atrasado_servico',
        filters={'status': 'Agendado'},
        field_name='ServicosEscalados__nome',
        title='Área Total por serviço (Atrasados)',
        label_type='Serviços',
        color='#dc3444',
        sum_by='Areas__dimensao',
        count_by='id',
        filter_time={'DataDeInicio__lt': one_day},
    )

    return figs_atrasado_localidade, figs_atrasado_area, figs_atrasado_servico


def graphs_limpeza_predial_agendado_to_reports(request, userid, agendado):
    one_day, seven_days = define_range_time()
    figs_agendado_localidade = data_visualization_limpeza_predial_graphs(request, userid, agendado).create_fig_report(
        name_fig='figs_agendado_localidade',
        filters={'status': 'Agendado'},
        field_name='Areas__localidade__nome',
        title='Área Total por localidade (Agendados)',
        label_type='Localidade',
        color='#14a0b6',
        sum_by='Areas__dimensao',
        count_by='id',
        filter_time={'DataDeInicio__gte': seven_days},
    )

    figs_agendado_area = data_visualization_limpeza_predial_graphs(request, userid, agendado).create_fig_report(
        name_fig='figs_agendado_area',
        filters={'status': 'Agendado'},
        field_name='Areas__nome',
        title='Área Total por área verde (Agendados)',
        label_type='Área',
        color='#14a0b6',
        sum_by='Areas__dimensao',
        count_by='id',
        filter_time={'DataDeInicio__gte': seven_days},
    )

    figs_agendado_servico = data_visualization_limpeza_predial_graphs(request, userid, agendado).create_fig_report(
        name_fig='figs_agendado_servico',
        filters={'status': 'Agendado'},
        field_name='ServicosEscalados__nome',
        title='Área Total por serviço (Agendados)',
        label_type='Serviços',
        color='#14a0b6',
        sum_by='Areas__dimensao',
        count_by='id',
        filter_time={'DataDeInicio__gte': seven_days},
    )

    return figs_agendado_localidade, figs_agendado_area, figs_agendado_servico


def graphs_limpeza_predial_em_andamento_to_reports(request, userid, agendado):
    figs_em_andamento_localidade = data_visualization_limpeza_predial_graphs(request, userid, agendado).create_fig_report(
        name_fig='figs_em_andamento_localidade',
        filters={'status': 'Em andamento'},
        field_name='Areas__localidade__nome',
        title='Área Total por localidade (Em andamento)',
        label_type='Localidade',
        color='#008000',
        sum_by='Areas__dimensao',
        count_by='id',
    )

    figs_em_andamento_area = data_visualization_limpeza_predial_graphs(request, userid, agendado).create_fig_report(
        name_fig='figs_em_andamento_area',
        filters={'status': 'Em andamento'},
        field_name='Areas__nome',
        title='Área Total por área verde (Em andamento)',
        label_type='Área',
        color='#008000',
        sum_by='Areas__dimensao',
        count_by='id',
    )

    figs_em_andamento_servico = data_visualization_limpeza_predial_graphs(request, userid, agendado).create_fig_report(
        name_fig='figs_em_andamento_servico',
        filters={'status': 'Em andamento'},
        field_name='ServicosEscalados__nome',
        title='Área Total por serviço (Em andamento)',
        label_type='Serviços',
        color='#008000',
        sum_by='Areas__dimensao',
        count_by='id',
    )

    return figs_em_andamento_localidade, figs_em_andamento_area, figs_em_andamento_servico