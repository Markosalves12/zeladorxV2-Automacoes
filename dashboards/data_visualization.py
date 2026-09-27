import calendar
import json
from collections import OrderedDict

from django.db.models import Sum, Count, F
from django.db.models.functions import TruncMonth
from django.utils.html import escape

from utils.utils import filtrar_unicos

# Os gráficos são desenhados no navegador (dist/js/zeladorx-charts.js, com
# plotly.js carregado uma única vez). O servidor só agrega os dados no banco e
# envia a especificação da figura em JSON — sem plotly/pandas no request.
#
# Tiles do OpenStreetMap/CARTO bloqueiam requisições sem Referer (Django usa
# SECURE_REFERRER_POLICY="same-origin"). Usamos o fundo gratuito da Esri,
# sem token, aplicado como camada raster sobre o estilo "white-bg".
MAP_STYLE = "white-bg"
MAP_TILES = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}"
MAP_CENTER = {"lat": -15.797483, "lon": -47.935315}


class ClientFigure(dict):
    """Figura no formato do plotly.js ({'data': [...], 'layout': {...}}).

    - to_html(): devolve só um <div> com o JSON; o navegador desenha.
    - Continua sendo um dict válido para plotly.io.to_image, usado no
      fallback do PDF gerado no servidor.
    """

    def __init__(self, data=None, layout=None):
        super().__init__(data=data or [], layout=layout or {})

    def update_layout(self, **kwargs):
        self['layout'].update(kwargs)
        return self

    def to_json(self):
        return json.dumps(self, default=_json_default, ensure_ascii=False)

    def to_html(self, full_html=False, **kwargs):
        height = self['layout'].get('height', 300)
        return (
            f'<div class="zx-plotly" style="min-height:{int(height)}px" '
            f'data-figure="{escape(self.to_json())}"></div>'
        )


def _json_default(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return str(value)


def _num(value):
    return float(value) if value is not None else 0.0


def _com_mapa_base(fig):
    fig['layout']['mapbox'] = {
        **fig['layout'].get('mapbox', {}),
        'style': MAP_STYLE,
        'layers': [{
            "below": "traces",
            "sourcetype": "raster",
            "sourceattribution": "Tiles &copy; Esri",
            "source": [MAP_TILES],
        }],
    }
    return fig


def _mapa_vazio():
    fig = ClientFigure(
        data=[{
            'type': 'scattermapbox',
            'lat': [MAP_CENTER["lat"]], 'lon': [MAP_CENTER["lon"]],
            'mode': 'markers+text',
            'marker': {'size': 10, 'color': 'gray'},
            'text': ["Nenhum dado disponível"],
            'textposition': 'top center',
        }],
        layout={
            'mapbox': {'center': MAP_CENTER, 'zoom': 5},
            'margin': dict(l=0, r=0, t=50, b=0),
            'height': 700,
            'title': {'text': "<b>Nenhum dado disponível</b>"},
        },
    )
    return _com_mapa_base(fig)


def get_total_area(queryset, area_field='Areas__dimensao'):
    aggregate_result = queryset.aggregate(total_area=Sum(area_field))
    return aggregate_result['total_area'] if aggregate_result['total_area'] else 0


def calculate_areas_and_counts(dados_servicos, status, date_filter=None):
    """
    Calcula a soma das áreas e as contagens de itens para um conjunto de dados filtrados.
    """
    queryset = dados_servicos.filter(status=status)
    if date_filter:
        queryset = queryset.filter(date_filter)
    return get_total_area(queryset)


def get_total_area_by_category(queryset, category_field, sum_by, count_by):
    """
    Calcula a soma das áreas e as contagens de itens para cada categoria.

    Args:
        queryset: A consulta do Django ORM.
        category_field: O campo da categoria a ser agrupado.

    Returns:
        Um dicionário com a categoria como chave e a soma das áreas como valor.
        Um dicionário com a categoria como chave e a contagem de itens como valor.
    """
    data = queryset.values(category_field).annotate(
        total_area=Sum(sum_by),
        count=Count(count_by)
    ).order_by()

    total_area_by_category = {item[category_field]: item['total_area'] for item in data}
    counts_by_category = {item[category_field]: item['count'] for item in data}

    return total_area_by_category, counts_by_category


def plot_horizontal_bar_chart(data, title, x_axis_title, y_axis_title, counts, marker_color='#000080'):
    """Especificação de barras horizontais (desenhada no navegador)."""
    categories = [str(c) for c in data.keys()]
    values = [_num(v) for v in data.values()]
    hovertexts = [f'Área Total: {v}<br>Servicos: {counts[c]}' for c, v in data.items()]
    height = 300 + 20 * len(categories)

    return ClientFigure(
        data=[{
            'type': 'bar', 'orientation': 'h',
            'x': values, 'y': categories,
            'marker': {'color': marker_color},
            'width': 0.3,
            'text': hovertexts, 'textposition': 'auto',
            'hovertext': hovertexts, 'hoverinfo': 'text',
        }],
        layout={
            'title': {'text': title},
            'xaxis': {'title': {'text': x_axis_title}},
            'yaxis': {'title': {'text': y_axis_title}},
            'margin': dict(l=0, r=0, t=27, b=0),
            'bargap': 0.1,
            'height': height,
        },
    )


def get_total_area_and_counts_by_month(queryset, field_name, sum_by, count_by, date_column):
    """
    Calcula a soma das áreas e as contagens de itens para cada mês e campo especificado.

    Args:
        queryset: A consulta do Django ORM.
        field_name: O nome do campo para agrupamento (e.g., 'area__vegetacao', 'area__terreno').

    Returns:
        Um dicionário com o mês como chave e a soma das áreas como valor.
        Um dicionário com o mês como chave e a contagem de itens como valor.
        Um dicionário com o mês como chave e a categoria como valor.
    """
    data = queryset.annotate(
        month=TruncMonth(date_column),
        category=F(field_name)
    ).values('month', 'category').annotate(
        total_area=Sum(sum_by),
        count=Count(count_by)
    ).order_by('month', 'category')

    total_area_by_month = {}
    counts_by_month = {}
    categories_by_month = {}

    for item in data:
        month = item['month']
        category = item['category']
        month_str = f"{calendar.month_abbr[month.month]}/{month.year}"

        if month_str not in total_area_by_month:
            total_area_by_month[month_str] = {}
            counts_by_month[month_str] = {}
            categories_by_month[month_str] = {}

        total_area_by_month[month_str][category] = item['total_area']
        counts_by_month[month_str][category] = item['count']
        categories_by_month[month_str][category] = category

    return total_area_by_month, counts_by_month, categories_by_month


def plot_grouped_bar_chart(data, title, x_axis_title, y_axis_title, counts, categories, label_type, marker_colors=None):
    """Especificação de barras agrupadas por mês (desenhada no navegador)."""
    months = list(data.keys())
    categories_list = list(OrderedDict.fromkeys(cat for month in data.values() for cat in month.keys()))
    traces = []

    for i, category in enumerate(categories_list):
        values = [_num(data[month].get(category, 0)) for month in months]
        hovertexts = [
            f'{label_type.capitalize()}: {categories[month].get(category, "N/A")}<br>Mês: {month}<br>Área Total: {data[month].get(category, 0)}<br>Serviços: {counts[month].get(category, 0)}'
            for month in months
        ]
        trace = {
            'type': 'bar', 'x': months, 'y': values, 'name': str(category),
            'width': 0.3, 'text': hovertexts, 'textposition': 'auto',
            'hovertext': hovertexts, 'hoverinfo': 'text',
        }
        if marker_colors:
            trace['marker'] = {'color': marker_colors[i]}
        traces.append(trace)

    return ClientFigure(
        data=traces,
        layout={
            'title': {'text': title},
            'xaxis': {'title': {'text': x_axis_title}},
            'yaxis': {'title': {'text': y_axis_title}},
            'barmode': 'group',
            'margin': dict(l=0, r=0, t=27, b=0),
            'height': 300,
        },
    )


def generate_grouped_chart(dados_servicos, filters, field_name, title, label_type, sum_by, count_by, date_column):
    """
    Gera um gráfico de barras agrupadas para um conjunto de dados filtrados.
    """
    area, counts, categories = get_total_area_and_counts_by_month(
        filtrar_unicos(dados_servicos, **filters),
        field_name,
        sum_by,
        count_by,
        date_column
    )

    return plot_grouped_bar_chart(area, title, 'Mês', 'Área Total', counts, categories, label_type)


def generate_chart(dados_servicos, filters, field_name, title, label_type, color, sum_by, count_by):
    """
    Gera um gráfico de barras horizontais para um conjunto de dados filtrados.
    """
    area, counts = get_total_area_by_category(filtrar_unicos(dados_servicos, **filters), field_name, sum_by, count_by)
    return plot_horizontal_bar_chart(area, title, 'Área Total', label_type, counts, color)


def _linhas_paginadas(paginated_queryset):
    for page in paginated_queryset.paginator.page_range:
        for obj in paginated_queryset.paginator.page(page).object_list:
            yield obj


def plot_map(paginated_queryset, color="#FF0000", scale_factor=2):
    """Mapa de bolhas proporcionais à área total de cada localidade."""
    grupos = OrderedDict()
    for obj in _linhas_paginadas(paginated_queryset):
        try:
            key = (float(obj['lat_localidade']), float(obj['long_localidade']),
                   obj['unidade_nome'], obj['localidade_nome'])
            area = float(obj['area_total'])
        except (TypeError, ValueError, KeyError):
            continue
        grupos.setdefault(key, []).append(area)

    if not grupos:
        return _mapa_vazio()

    linhas = []
    for (lat, lon, unidade, localidade), areas in grupos.items():
        total = sum(areas)
        linhas.append((lat, lon, unidade, localidade, total, total / len(areas), len(areas)))

    max_total = max(l[4] for l in linhas) or 1
    fig = ClientFigure(
        data=[{
            'type': 'scattermapbox',
            'lat': [l[0] for l in linhas],
            'lon': [l[1] for l in linhas],
            'mode': 'markers+text',
            'marker': {
                'size': [min(max(l[4] / max_total * 30 * scale_factor, 5), 25) for l in linhas],
                'color': color, 'opacity': 0.7, 'sizemin': 5,
            },
            'text': [
                f"{l[3]}<br>Unidade: {l[2]}<br>Total de Áreas: {l[6]}"
                f"<br>Área Média: {l[5]:.2f} m²<br>Área Total: {l[4]:.2f} m²"
                for l in linhas
            ],
            'hovertext': [
                f"<b>{l[2]}</b><br>Área total: {l[4]:.2f} m²<br>Área média: {l[5]:.2f} m²<br>Áreas: {l[6]}"
                for l in linhas
            ],
            'hoverinfo': 'text',
            'showlegend': False,
        }],
        layout={
            'mapbox': {'center': MAP_CENTER, 'zoom': 5},
            'margin': dict(l=0, r=0, t=50, b=0),
            'height': 700,
            'font': {'size': 18},
        },
    )
    return _com_mapa_base(fig)


def plot_map_distribution_services_by_status(paginated_queryset, scale_factor=5):
    import math

    color_mapping = {
        'Em andamento': '#008000',
        'Atrasado': '#FF0000',
        'Agendado': '#14A0B6',
        'Próximo': '#FFFF00',
    }

    grupos = OrderedDict()
    for obj in _linhas_paginadas(paginated_queryset):
        try:
            localidade = obj.Areas.localidade
            key = (float(localidade.lat_med), float(localidade.long_med),
                   localidade.unidade.nome, localidade.nome, obj.novo_status)
            area = float(obj.Areas.dimensao)
        except (AttributeError, TypeError, ValueError) as e:
            print(f"Erro ao processar objeto: {e}")
            continue
        grupo = grupos.setdefault(key, {'area_total': 0.0, 'ids': set()})
        grupo['area_total'] += area
        grupo['ids'].add(getattr(obj, 'id_random', None) or id(obj))

    if not grupos:
        return _mapa_vazio()

    # Desloca em círculo os pontos que caem na mesma coordenada.
    por_coordenada = OrderedDict()
    for key in grupos:
        por_coordenada.setdefault((key[0], key[1]), []).append(key)

    linhas = []
    for (lat, lon), keys in por_coordenada.items():
        n = len(keys)
        for i, key in enumerate(keys):
            dlat = dlon = 0.0
            if n > 1:
                angle = 10 * math.pi * i / n
                dlat, dlon = 0.002 * math.sin(angle), 0.002 * math.cos(angle)
            g = grupos[key]
            linhas.append({
                'lat': lat + dlat, 'lon': lon + dlon,
                'unidade': key[2], 'localidade': key[3], 'status': key[4],
                'area_total': g['area_total'], 'num': len(g['ids']),
            })

    max_area = max(l['area_total'] for l in linhas)
    for l in linhas:
        size = l['area_total'] / max_area * 30 * scale_factor if max_area > 0 else 10 * scale_factor
        l['size'] = min(max(size, 10), 30)

    traces = []
    for status, color in color_mapping.items():
        rows = [l for l in linhas if l['status'] == status]
        if not rows:
            continue
        traces.append({
            'type': 'scattermapbox',
            'lat': [r['lat'] for r in rows],
            'lon': [r['lon'] for r in rows],
            'mode': 'markers+text',
            'marker': {'size': [r['size'] for r in rows], 'color': color,
                       'opacity': 0.8, 'sizemode': 'diameter'},
            'text': [
                f"Localidade: {r['localidade']} \nUnidade: {r['unidade']} \nStatus: {r['status']} \n"
                f"Agendamentos: {r['num']}\nÁrea total: {r['area_total']} m²" for r in rows
            ],
            'textposition': 'top center',
            'textfont': {'size': 18, 'color': 'black'},
            'name': status,
            'hovertext': [
                f"<b>Localidade:</b> {r['localidade']}<br><b>Unidade:</b> {r['unidade']}<br>"
                f"<b>Status:</b> {r['status']}<br><b>Agendamentos:</b> {r['num']}<br>"
                f"<b>Área total:</b> {r['area_total']:.2f} m²" for r in rows
            ],
            'hoverinfo': 'text',
            'showlegend': True,
        })

    fig = ClientFigure(
        data=traces,
        layout={
            'mapbox': {'center': MAP_CENTER, 'zoom': 5},
            'margin': dict(l=0, r=0, t=50, b=0),
            'height': 700,
            'legend': dict(title={'text': "<b>Status dos Serviços</b>"}, orientation="h",
                           yanchor="top", y=1.1, xanchor="left", x=0,
                           bgcolor='rgba(255,255,255,0.5)'),
            'hovermode': 'closest',
            'hoverlabel': dict(bgcolor="white", font={'size': 18, 'family': "Arial"}),
        },
    )
    return _com_mapa_base(fig)
