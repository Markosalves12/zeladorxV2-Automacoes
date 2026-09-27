from django.utils import timezone
from dashboards.data_visualization import generate_chart, generate_grouped_chart, plot_map
from utils.utils import define_range_time

def data_visualization_limpeza_predial_indicadores(request, userid, agendado):
    em_andamento = agendado.filter(status='Em andamento').count()
    atrasados = agendado.filter(DataDeInicio__lt=timezone.now().date()).exclude(status="Em andamento").count()

    one_day, seven_days = define_range_time()

    proximos = agendado.filter(
        DataDeInicio__gte=one_day,
        DataDeInicio__lte=seven_days
    ).exclude(
        status="Em andamento",
        DataDeInicio__lte=seven_days
    ).count()

    agendamentos = agendado.filter(
        status='Agendado',
        DataDeInicio__gte=seven_days,
    ).count()

    return (em_andamento, atrasados, proximos, agendamentos)



class data_visualization_limpeza_predial_graphs:
    def __init__(self, request, userid, agendado, filter_time=False):
        self.request = request
        self.userid = userid
        self.agendados = agendado

    one_day, seven_days = define_range_time()

    def create_fig(self, name_fig, filters, field_name, title, label_type, color, sum_by, count_by,
                   filter_time=False):
        if filter_time:
            self.agendados  = self.agendados.filter(
                **filter_time
            )

        fig_charts = {
            f'{name_fig}': generate_chart(
                dados_servicos=self.agendados,
                filters=filters,
                field_name=field_name,
                title=title,
                label_type=label_type,
                color=color,
                sum_by=sum_by,
                count_by=count_by
            ).to_html(full_html=True),
        }

        return fig_charts

    def define_figs_by_months(self, name_fig, filters, field_name, title, label_type, color,
                              sum_by, count_by, date_column, filter_time=False):
        if filter_time:
            self.agendados  = self.agendados.filter(
                **filter_time
            )

        fig_charts = {
            f'{name_fig}': generate_grouped_chart(
                self.agendados,
                filters=filters,
                field_name=field_name,
                title=title,
                label_type=label_type,
                sum_by=sum_by,
                count_by=count_by,
                date_column=date_column
            ).to_html(full_html=False),
        }

        return fig_charts

    def create_fig_report(self, name_fig, filters, field_name, title, label_type, color, sum_by, count_by,
                   filter_time=False):
        if filter_time:
            self.agendados  = self.agendados.filter(
                **filter_time
            )

        fig_charts = {
            f'{name_fig}': generate_chart(
                dados_servicos=self.agendados,
                filters=filters,
                field_name=field_name,
                title=title,
                label_type=label_type,
                color=color,
                sum_by=sum_by,
                count_by=count_by
            ),
        }

        return fig_charts

    def create_fig_maps(self, name_fig, color):
        fig_charts = {
            f'{name_fig}': plot_map(
                paginated_queryset=self.agendado,
                color=color,
            ).to_html(full_html=True),
        }

        return fig_charts