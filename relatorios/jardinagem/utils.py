from utils.utils import define_range_time
from dashboards.data_visualization_jardinagem import data_visualization_jardinagem_graphs

def graphs_jardinagem_concluido_to_reports(request, userid, agendado):
    figs_concluidos_terreno = data_visualization_jardinagem_graphs(request, userid, agendado).create_fig_report(
        name_fig='fig_area_terreno_concluido',
        filters={'status': 'Concluido'},
        field_name='Areas__Terreno__nome',
        title='Área Total por Tipo de Terreno (Concluido)',
        label_type='Terreno',
        color='#020d3f',
        sum_by='Areas__dimensao',
        count_by='id',
    )

    figs_concluidos_vegetacao = data_visualization_jardinagem_graphs(request, userid, agendado).create_fig_report(
        name_fig='fig_area_vegetacao_concluido',
        filters={'status': 'Concluido'},
        field_name='Areas__vegetacao__nome',
        title='Área Total por Tipo de Vegeteção (Concluido)',
        label_type='Vegeteção',
        color='#020d3f',
        sum_by='Areas__dimensao',
        count_by='id',
    )

    figs_concluidos_localidade = data_visualization_jardinagem_graphs(request, userid, agendado).create_fig_report(
        name_fig='figs_concluidos_localidade',
        filters={'status': 'Concluido'},
        field_name='Areas__localidade__nome',
        title='Área Total por localidade (Concluido)',
        label_type='Localidade',
        color='#020d3f',
        sum_by='Areas__dimensao',
        count_by='id',
    )

    figs_concluidos_area = data_visualization_jardinagem_graphs(request, userid, agendado).create_fig_report(
        name_fig='figs_concluidos_area',
        filters={'status': 'Concluido'},
        field_name='Areas__nome',
        title='Área Total por área verde (Concluido)',
        label_type='Área',
        color='#020d3f',
        sum_by='Areas__dimensao',
        count_by='id',
    )

    figs_concluidos_colaborador = data_visualization_jardinagem_graphs(request, userid, agendado).create_fig_report(
        name_fig='figs_concluidos_colaborador',
        filters={'status': 'Concluido'},
        field_name='ColaboradoresEscalados__username',
        title='Área Total por colaborador (Concluido)',
        label_type='Colaborador',
        color='#020d3f',
        sum_by='Areas__dimensao',
        count_by='id',
    )

    figs_concluidos_servico = data_visualization_jardinagem_graphs(request, userid, agendado).create_fig_report(
        name_fig='figs_concluidos_servico',
        filters={'status': 'Concluido'},
        field_name='ServicosEscalados__nome',
        title='Área Total por serviço (Concluido)',
        label_type='Serviços',
        color='#020d3f',
        sum_by='Areas__dimensao',
        count_by='id',
    )

    return (figs_concluidos_terreno, figs_concluidos_vegetacao, figs_concluidos_localidade,
            figs_concluidos_area, figs_concluidos_colaborador, figs_concluidos_servico)

def graphs_jardinagem_proximo_to_reports(request, userid, agendado):
    one_day, seven_days = define_range_time()
    figs_proximo_terreno = data_visualization_jardinagem_graphs(request, userid, agendado).create_fig_report(
        name_fig='fig_area_terreno_concluido',
        filters={'status': 'Agendado'},
        field_name='Areas__Terreno__nome',
        title='Área Total por Tipo de Terreno (Próximo)',
        label_type='Terreno',
        color='#f6be04',
        sum_by='Areas__dimensao',
        count_by='id',
        filter_time={'DataDeInicio__gte': one_day, 'DataDeInicio__lte': seven_days},
    )

    figs_proximo_vegetacao = data_visualization_jardinagem_graphs(request, userid, agendado).create_fig_report(
        name_fig='fig_area_vegetacao_concluido',
        filters={'status': 'Agendado'},
        field_name='Areas__vegetacao__nome',
        title='Área Total por Tipo de Vegeteção (Próximo)',
        label_type='Vegeteção',
        color='#f6be04',
        sum_by='Areas__dimensao',
        count_by='id',
        filter_time={'DataDeInicio__gte': one_day, 'DataDeInicio__lte': seven_days},
    )

    figs_proximo_localidade = data_visualization_jardinagem_graphs(request, userid, agendado).create_fig_report(
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

    figs_proximo_area = data_visualization_jardinagem_graphs(request, userid, agendado).create_fig_report(
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

    figs_proximo_colaborador = data_visualization_jardinagem_graphs(request, userid, agendado).create_fig_report(
        name_fig='figs_concluidos_colaborador',
        filters={'status': 'Agendado'},
        field_name='ColaboradoresEscalados__username',
        title='Área Total por colaborador (Próximo)',
        label_type='Colaborador',
        color='#f6be04',
        sum_by='Areas__dimensao',
        count_by='id',
        filter_time={'DataDeInicio__gte': one_day, 'DataDeInicio__lte': seven_days},
    )

    figs_proximo_servico = data_visualization_jardinagem_graphs(request, userid, agendado).create_fig_report(
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

    return (figs_proximo_terreno, figs_proximo_vegetacao, figs_proximo_localidade,
            figs_proximo_area, figs_proximo_colaborador, figs_proximo_servico)


def graphs_jardinagem_atrasado_to_reports(request, userid, agendado):
    one_day, seven_days = define_range_time()
    figs_atrasado_terreno = data_visualization_jardinagem_graphs(request, userid, agendado).create_fig_report(
        name_fig='figs_atrasado_terreno',
        filters={'status': 'Agendado'},
        field_name='Areas__Terreno__nome',
        title='Área Total por Tipo de Terreno (Atrasados)',
        label_type='Terreno',
        color='#dc3444',
        sum_by='Areas__dimensao',
        count_by='id',
        filter_time={'DataDeInicio__lt': one_day},
    )

    figs_atrasado_vegetacao = data_visualization_jardinagem_graphs(request, userid, agendado).create_fig_report(
        name_fig='figs_atrasado_vegetacao',
        filters={'status': 'Agendado'},
        field_name='Areas__vegetacao__nome',
        title='Área Total por Tipo de Vegeteção (Atrasados)',
        label_type='Vegeteção',
        color='#dc3444',
        sum_by='Areas__dimensao',
        count_by='id',
        filter_time={'DataDeInicio__lt': one_day},
    )

    figs_atrasado_localidade = data_visualization_jardinagem_graphs(request, userid, agendado).create_fig_report(
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

    figs_atrasado_area = data_visualization_jardinagem_graphs(request, userid, agendado).create_fig_report(
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

    figs_atrasado_colaborador = data_visualization_jardinagem_graphs(request, userid, agendado).create_fig_report(
        name_fig='figs_atrasado_colaborador',
        filters={'status': 'Agendado'},
        field_name='ColaboradoresEscalados__username',
        title='Área Total por colaborador (Atrasados)',
        label_type='Colaborador',
        color='#dc3444',
        sum_by='Areas__dimensao',
        count_by='id',
        filter_time={'DataDeInicio__lt': one_day},
    )

    figs_atrasado_servico = data_visualization_jardinagem_graphs(request, userid, agendado).create_fig_report(
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

    return (figs_atrasado_terreno, figs_atrasado_vegetacao, figs_atrasado_localidade,
            figs_atrasado_area, figs_atrasado_colaborador, figs_atrasado_servico)


def graphs_jardinagem_agendado_to_reports(request, userid, agendado):
    one_day, seven_days = define_range_time()
    figs_agendado_terreno = data_visualization_jardinagem_graphs(request, userid, agendado).create_fig_report(
        name_fig='figs_agendado_terreno',
        filters={'status': 'Agendado'},
        field_name='Areas__Terreno__nome',
        title='Área Total por Tipo de Terreno (Agendados)',
        label_type='Terreno',
        color='#14a0b6',
        sum_by='Areas__dimensao',
        count_by='id',
        filter_time={'DataDeInicio__gte': seven_days},
    )

    figs_agendado_vegetacao = data_visualization_jardinagem_graphs(request, userid, agendado).create_fig_report(
        name_fig='figs_agendado_vegetacao',
        filters={'status': 'Agendado'},
        field_name='Areas__vegetacao__nome',
        title='Área Total por Tipo de Vegeteção (Agendados)',
        label_type='Vegeteção',
        color='#14a0b6',
        sum_by='Areas__dimensao',
        count_by='id',
        filter_time={'DataDeInicio__gte': seven_days},
    )

    figs_agendado_localidade = data_visualization_jardinagem_graphs(request, userid, agendado).create_fig_report(
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

    figs_agendado_area = data_visualization_jardinagem_graphs(request, userid, agendado).create_fig_report(
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

    figs_agendado_colaborador = data_visualization_jardinagem_graphs(request, userid, agendado).create_fig_report(
        name_fig='figs_agendado_colaborador',
        filters={'status': 'Agendado'},
        field_name='ColaboradoresEscalados__username',
        title='Área Total por colaborador (Agendados)',
        label_type='Colaborador',
        color='#14a0b6',
        sum_by='Areas__dimensao',
        count_by='id',
        filter_time={'DataDeInicio__gte': seven_days},
    )

    figs_agendado_servico = data_visualization_jardinagem_graphs(request, userid, agendado).create_fig_report(
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

    return (figs_agendado_terreno, figs_agendado_vegetacao, figs_agendado_localidade,
            figs_agendado_area, figs_agendado_colaborador, figs_agendado_servico)


def graphs_jardinagem_em_andamento_to_reports(request, userid, agendado):
    figs_em_andamento_terreno = data_visualization_jardinagem_graphs(request, userid, agendado).create_fig_report(
        name_fig='figs_em_andamento_terreno',
        filters={'status': 'Em andamento'},
        field_name='Areas__Terreno__nome',
        title='Área Total por Tipo de Terreno (Em andamento)',
        label_type='Terreno',
        color='#008000',
        sum_by='Areas__dimensao',
        count_by='id',
    )

    figs_em_andamento_vegetacao = data_visualization_jardinagem_graphs(request, userid, agendado).create_fig_report(
        name_fig='figs_em_andamento_vegetacao',
        filters={'status': 'Em andamento'},
        field_name='Areas__vegetacao__nome',
        title='Área Total por Tipo de Vegeteção (Em andamento)',
        label_type='Vegeteção',
        color='#008000',
        sum_by='Areas__dimensao',
        count_by='id',
    )

    figs_em_andamento_localidade = data_visualization_jardinagem_graphs(request, userid, agendado).create_fig_report(
        name_fig='figs_em_andamento_localidade',
        filters={'status': 'Em andamento'},
        field_name='Areas__localidade__nome',
        title='Área Total por localidade (Em andamento)',
        label_type='Localidade',
        color='#008000',
        sum_by='Areas__dimensao',
        count_by='id',
    )

    figs_em_andamento_area = data_visualization_jardinagem_graphs(request, userid, agendado).create_fig_report(
        name_fig='figs_em_andamento_area',
        filters={'status': 'Em andamento'},
        field_name='Areas__nome',
        title='Área Total por área verde (Em andamento)',
        label_type='Área',
        color='#008000',
        sum_by='Areas__dimensao',
        count_by='id',
    )

    figs_em_andamento_colaborador = data_visualization_jardinagem_graphs(request, userid, agendado).create_fig_report(
        name_fig='figs_em_andamento_colaborador',
        filters={'status': 'Em andamento'},
        field_name='ColaboradoresEscalados__username',
        title='Área Total por colaborador (Em andamento)',
        label_type='Colaborador',
        color='#008000',
        sum_by='Areas__dimensao',
        count_by='id',
    )

    figs_em_andamento_servico = data_visualization_jardinagem_graphs(request, userid, agendado).create_fig_report(
        name_fig='figs_em_andamento_servico',
        filters={'status': 'Em andamento'},
        field_name='ServicosEscalados__nome',
        title='Área Total por serviço (Em andamento)',
        label_type='Serviços',
        color='#008000',
        sum_by='Areas__dimensao',
        count_by='id',
    )

    return (figs_em_andamento_terreno, figs_em_andamento_vegetacao, figs_em_andamento_localidade,
            figs_em_andamento_area, figs_em_andamento_colaborador, figs_em_andamento_servico)