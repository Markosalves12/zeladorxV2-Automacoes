from django.contrib import admin



class ServicoLimpezaPredialConfiguradoAdmin(admin.ModelAdmin):
    list_display = (
    'Areas', 'tempomedioplanejado', 'horario_1', 'horario_2', 'horario_3', 'horario_4', 'horario_5', 'horario_6',
    'horario_7',)
    list_display_links = (
    'Areas', 'tempomedioplanejado', 'horario_1', 'horario_2', 'horario_3', 'horario_4', 'horario_5', 'horario_6',
    'horario_7',)
    # search_fields = ('ServicosEscalados', )
    # list_filter = ('ServicosEscalados', )

    list_per_page = 20


class ServicoLimpezaPredialAgendadoAdmin(admin.ModelAdmin):
    list_display = ('Areas', 'TipoServico', 'DataDeInicio', 'DataDeConclusao', 'status', 'id_configuracao', )
    list_display_links = ('Areas', 'TipoServico', 'DataDeInicio', 'DataDeConclusao', 'status', 'id_configuracao', )
    # search_fields = ('ServicosEscalados', )
    # list_filter = ('ServicosEscalados', )

    list_per_page = 20


class FatoServicoLimpezaPredialAdmin(admin.ModelAdmin):
    list_display = ('Servico', 'data_hora_chegada_na_area', 'data_hora_retorno_area', 'Gerente', 'foto_entrega', )
    list_display_links = ('Servico', 'data_hora_chegada_na_area', 'data_hora_retorno_area', 'Gerente', 'foto_entrega',)
    search_fields = ('Servico', )
    list_filter = ('Servico', )

    list_per_page = 20

