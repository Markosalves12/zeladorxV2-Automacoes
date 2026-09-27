from django.contrib import admin

# Register your models here.
class ServicoJardinagemConfiguradoAdmin(admin.ModelAdmin):
    list_display = (
    'Areas', 'tempomedioplanejado', 'horario_1', 'horario_2', 'horario_3', 'horario_4', 'horario_5', 'horario_6',
    'horario_7', )
    list_display_links = (
    'Areas', 'tempomedioplanejado', 'horario_1', 'horario_2', 'horario_3', 'horario_4', 'horario_5', 'horario_6',
    'horario_7',)

    list_per_page = 20


class ServicoJardinagemAgendadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'DataDeInicio', 'DescricaoDoServico', 'Areas', 'status', 'foto_solicitacao',
                    'foto_entrega', 'DataDeConclusao', 'TipoServico', 'id_configuracao', )
    list_display_links = ('id', 'DataDeInicio', 'DescricaoDoServico', 'Areas', 'status', 'foto_solicitacao',
                          'foto_entrega', 'DataDeConclusao', 'TipoServico', 'id_configuracao', )
    search_fields = ('DataDeInicio', 'status', 'DataDeConclusao', 'TipoServico', )
    list_filter = ('status', 'TipoServico', )

    list_per_page = 20


class FatoServicoJardinagemAdmin(admin.ModelAdmin):
    list_display = ('id', 'Servico', 'data_hora_chegada_na_area', 'data_hora_retorno_area', 'Gerente',)
    list_display_links = ('id', 'Servico', 'data_hora_chegada_na_area',  'data_hora_retorno_area', 'Gerente',)
    search_fields = ('Servico', 'data_hora_chegada_na_area', 'data_hora_retorno_area', 'Colaborador',)
    list_filter = ('Gerente', )

    list_per_page = 20


